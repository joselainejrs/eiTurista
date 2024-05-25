import os
import requests
import unicodedata
from flask_cors import CORS
from datetime import datetime
from flask import Flask, jsonify, request
from contrato import Localidade, Depoimento, db

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///eiTurista.db'
db.init_app(app)


api_key = os.environ['api_key_previsao_tempo']


def formulaCelsius(Kelvin: int) -> int:
    celsius = Kelvin - 273.15
    return f'{int(celsius)}'

def avaliacao_texto(texto: str) -> str:
    texto = texto.lower()
    texto = unicodedata.normalize('NFKD', texto).encode('ASCII', 'ignore').decode('ASCII')
    return texto

def padronizar_tipo_depoimento(tipoDepoimento: str) -> str:
    tipoDepoimento_normalizado = avaliacao_texto(tipoDepoimento)
    if tipoDepoimento_normalizado == 'transito':
        return 'Trânsito'
    if tipoDepoimento_normalizado == 'restaurante':
        return 'Restaurante'
    if tipoDepoimento_normalizado == 'lazer':
        return 'Lazer'
    if tipoDepoimento_normalizado == 'tempo':
        return 'Tempo'
    return tipoDepoimento

@app.route('/localidade/<nome>', methods=["GET"])
def getLocalidade(nome: str):
    url = f'https://api.openweathermap.org/data/2.5/weather?q={nome}&appid={api_key}'
    resp = requests.get(url)

    if resp.status_code == 200:
        dados = resp.json()
        id = dados['id']
        local = dados['name']
        pais = dados['sys']['country']
        descricao = dados['weather'][0]['description']
        temp_max = dados['main']['temp_max']
        temp_min = dados['main']['temp_min']
        sensacao_termica = dados['main']['feels_like']

        localidade = Localidade.query.filter_by(local=local).first()
        if not localidade:
            localidade = Localidade(
                id=id,
                local=local,
                pais=pais,
                descricao=descricao,
                temp_max=formulaCelsius(temp_max),
                temp_min=formulaCelsius(temp_min),
                sensacao_termica=formulaCelsius(sensacao_termica)
            )
            db.session.add(localidade)
        else:
            localidade.descricao = descricao
            localidade.temp_max = formulaCelsius(temp_max)
            localidade.temp_min = formulaCelsius(temp_min)
            localidade.sensacao_termica = formulaCelsius(sensacao_termica)
        
        db.session.commit()

        depoimentos = Depoimento.query.filter_by(localidade_id=localidade.id).all()
        depoimentos_list = [depoimento.to_dict() for depoimento in depoimentos]

        response = {
            'localidade': localidade.to_dict(),
            'depoimentos': depoimentos_list
        }
        
        return jsonify(response)
    elif resp.status_code == 404:
        return jsonify({'error': 'não encontrado'}), 404


@app.route('/depoimento', methods=["POST"])
def postDepoimento():
    dados = request.get_json()

    localidade_id = dados.get('localidade_id')
    tipoDepoimento = dados.get('tipoDepoimento')
    detalhes = dados.get('detalhes')

    if not localidade_id or not tipoDepoimento or not detalhes:
        return jsonify({"error": "Todos os campos são necessários"}), 400
    
    depoimento_existente = Depoimento.query.filter(Depoimento.localidade_id == localidade_id) \
                                           .filter(Depoimento.tipoDepoimento == tipoDepoimento) \
                                           .filter(Depoimento.detalhes == detalhes) \
                                           .first()
    if depoimento_existente:
        return jsonify({"error": "Este depoimento já foi registrado"}), 409 
    
    localidade = Localidade.query.get(localidade_id)
    if not localidade:
        return jsonify({"error": "Localidade não encontrada"}), 404
       
    depoimento = Depoimento(
        localidade_id = localidade.id,
        tipoDepoimento = padronizar_tipo_depoimento(tipoDepoimento),
        detalhes = detalhes,
        data = datetime.now().date(),
        hora = datetime.now().time()
    )
    
    db.session.add(depoimento)
    db.session.commit()
    
    return jsonify(depoimento.to_dict()), 201

@app.route('/depoimento/<int:idDepoimento>', methods=["PATCH"])
def patchDepoimento(idDepoimento):
    dados = request.get_json()
    
    depoimento = Depoimento.query.get(idDepoimento)
    
    if not depoimento:
        return jsonify({"error": "Depoimento não encontrado"}), 404
        
    if 'tipoDepoimento' in dados:
        depoimento.tipoDepoimento = padronizar_tipo_depoimento(dados['tipoDepoimento'])
    if 'detalhes' in dados:
        depoimento.detalhes = dados['detalhes']

    depoimento.data = datetime.now().date()
    depoimento.hora = datetime.now().time()
    
    db.session.commit()

    localidade = Localidade.query.get(depoimento.localidade_id)
    if localidade:
        nome_localidade = localidade.local
        getLocalidade(nome_localidade)
    
    return jsonify(depoimento.to_dict()), 200


@app.route('/depoimento/<int:idDepoimento>', methods=["DELETE"])
def deleteDepoimento(idDepoimento):
    depoimento = Depoimento.query.get(idDepoimento)
    
    if not depoimento:
        return jsonify({"error": "Depoimento não encontrado"}), 404
    
    db.session.delete(depoimento)
    db.session.commit()
    
    return jsonify({"message": "Depoimento excluído com sucesso"}), 200

@app.route('/depoimento/tipo/<string:tipoDepoimento>/localidade/<int:localidade_id>', methods=["GET"])
def getFiltrarPorTipoDepoimentoPorLocalidade(tipoDepoimento, localidade_id):
    depoimentos_filtrados = Depoimento.query.filter_by(tipoDepoimento=tipoDepoimento, localidade_id=localidade_id).all()
    
    if not depoimentos_filtrados:
        return jsonify({"message": "Nenhum depoimento encontrado para este tipo e localidade"}), 404
    
    depoimentos_dict = [depoimento.to_dict() for depoimento in depoimentos_filtrados]
    
    return jsonify(depoimentos_dict), 200

@app.route('/depoimento/localidade/<int:localidade_id>', methods=["GET"])
def getFiltrarTodosDepoimentosPorLocalidade(localidade_id):
    depoimentos_filtrados = Depoimento.query.filter_by(localidade_id=localidade_id).all()
    
    if not depoimentos_filtrados:
        return jsonify({"message": "Nenhum depoimento encontrado para esta localidade"}), 404
    
    depoimentos_dict = [depoimento.to_dict() for depoimento in depoimentos_filtrados]
    
    return jsonify(depoimentos_dict), 200


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host='localhost', debug=True)

