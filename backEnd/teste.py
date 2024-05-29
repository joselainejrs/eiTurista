import os
import requests
import unicodedata
from flask_cors import CORS
from datetime import datetime
from flask_migrate import Migrate
from flask import Flask, jsonify, request
from contrato import Localidade, Depoimento, db

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///eiTurista.db'
db.init_app(app)
migrate = Migrate(app, db)

api_key = os.environ['api_key_previsao_tempo']

def formulaCelsius(Kelvin: int) -> int:
    celsius = Kelvin - 273.15
    return f'{int(celsius)}'

def avaliacao_texto(texto: str) -> str:
    texto = texto.lower()
    texto = unicodedata.normalize('NFKD', texto).encode('ASCII', 'ignore').decode('ASCII')
    return texto

def padronizar_tipo_depoimento(tipo_depoimento: str) -> str:
    tipoDepoimento_normalizado = avaliacao_texto(tipo_depoimento)
    if tipoDepoimento_normalizado == 'transito':
        return 'Trânsito'
    if tipoDepoimento_normalizado == 'restaurante':
        return 'Restaurante'
    if tipoDepoimento_normalizado == 'lazer':
        return 'Lazer'
    if tipoDepoimento_normalizado == 'tempo':
        return 'Tempo'
    return tipo_depoimento

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

        depoimentos = Depoimento.query.filter_by(id_localidade=localidade.id).all()
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

    id_localidade = dados.get('id_localidade')
    tipo_depoimento = dados.get('tipo_depoimento')
    detalhes = dados.get('detalhes')

    if not id_localidade or not tipo_depoimento or not detalhes:
        return jsonify({"error": "Todos os campos são necessários"}), 400
    
    depoimento_existente = Depoimento.query.filter(Depoimento.id_localidade == id_localidade) \
                                           .filter(Depoimento.tipo_depoimento == tipo_depoimento) \
                                           .filter(Depoimento.detalhes == detalhes) \
                                           .first()
    if depoimento_existente:
        return jsonify({"error": "Este depoimento já foi registrado"}), 409 
    
    localidade = Localidade.query.get(id_localidade)
    if not localidade:
        return jsonify({"error": "Localidade não encontrada"}), 404
       
    depoimento = Depoimento(
        id_localidade = localidade.id,
        tipo_depoimento = padronizar_tipo_depoimento(tipo_depoimento),
        detalhes = detalhes,
        data = datetime.now().date(),
        hora = datetime.now().time()
    )
    
    db.session.add(depoimento)
    db.session.commit()

    depoimento = [depoimento.to_dict() for depoimento in depoimento]

    
    return jsonify(depoimento.to_dict()), 200


@app.route('/depoimento/<int:idDepoimento>', methods=["PATCH"])
def patchDepoimento(idDepoimento):
    dados = request.get_json()
    
    depoimento = Depoimento.query.get(idDepoimento)
    
    if not depoimento:
        return jsonify({"error": "Depoimento não encontrado"}), 404
        
    if 'tipo_depoimento' in dados:
        depoimento.tipo_depoimento = padronizar_tipo_depoimento(dados['tipo_depoimento'])
    if 'detalhes' in dados:
        depoimento.detalhes = dados['detalhes']

    depoimento.data = datetime.now().date()
    depoimento.hora = datetime.now().time()
    
    db.session.commit()

    localidade = Localidade.query.get(depoimento.id_localidade)
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

    localidade = Localidade.query.filter_by(id=depoimento.id_localidade).first()
    if localidade:
        getTodosTipoDepoimentoPorLocalidade(localidade.id)

    
    return jsonify({"message": "Depoimento excluído com sucesso"}), 200

@app.route('/depoimento/tipo/<string:tipo_depoimento>/localidade/<int:id_localidade>', methods=["GET"])
def getPorTipoDepoimentoPorLocalidade(tipo_depoimento, id_localidade):
    depoimentos_filtrados = Depoimento.query.filter_by(tipo_depoimento=tipo_depoimento, id_localidade=id_localidade).all()
    
    if not depoimentos_filtrados:
        return jsonify([]), 200
    
    depoimentos_dict = [depoimento.to_dict() for depoimento in depoimentos_filtrados]
    
    return jsonify(depoimentos_dict), 200

@app.route('/depoimento/localidade/<int:id_localidade>', methods=["GET"])
def getTodosTipoDepoimentoPorLocalidade(id_localidade):
    depoimentos_filtrados = Depoimento.query.filter_by(id_localidade=id_localidade).all()
    
    if not depoimentos_filtrados:
        return jsonify([]), 200
    
    depoimentos_dict = [depoimento.to_dict() for depoimento in depoimentos_filtrados]

    return jsonify(depoimentos_dict), 200

        
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host='localhost', debug=True)

