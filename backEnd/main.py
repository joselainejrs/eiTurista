import requests
from flask_cors import CORS
from datetime import datetime
from flask import Flask, jsonify, request
from contrato import Localidade, Depoimento, db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///eiTurista.db'
CORS(app)
db.init_app(app)

api_key = '161626b5c65c28a04018e166bb2fd19c'

def formulaCelsius(Kelvin: int) -> int:
    celsius = Kelvin - 273.15
    return f'{int(celsius)}'

@app.route('/localidade/<nome>', methods=["GET"])
def getLocalidade(nome:str):
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

        localidade = Localidade.query.filter_by(local = local).first()
        if not localidade:
            localidade = Localidade(
                id = id,
                local = local,
                pais = pais,
                descricao = descricao,
                temp_max = formulaCelsius(temp_max),
                temp_min = formulaCelsius(temp_min),
                sensacao_termica=formulaCelsius(sensacao_termica)
            )
            db.session.add(localidade)
            db.session.commit()

        depoimentos = Depoimento.query.filter_by(localidade_id=localidade.id).all()
        depoimentos_list = [depoimento.to_dict() for depoimento in depoimentos]

        response = {
            'localidade': localidade.to_dict(),
            'depoimentos': depoimentos_list
        }
        
        return jsonify(response)
    elif resp.status_code == 404:
        return 'não encontrado'

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
        tipoDepoimento = tipoDepoimento,
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
        depoimento.tipoDepoimento = dados['tipoDepoimento']
    if 'detalhes' in dados:
        depoimento.detalhes = dados['detalhes']
    if 'data' in dados:
        depoimento.data = datetime.now().date(),
    if 'hora' in dados:
        depoimento.hora = datetime.now().time()
    
    db.session.commit()
    
    return jsonify(depoimento.to_dict()), 200


@app.route('/depoimento/<int:idDepoimento>', methods=["DELETE"])
def deleteDepoimento(idDepoimento):
    depoimento = Depoimento.query.get(idDepoimento)
    
    if not depoimento:
        return jsonify({"error": "Depoimento não encontrado"}), 404
    
    db.session.delete(depoimento)
    db.session.commit()
    
    return jsonify({"message": "Depoimento excluído com sucesso"}), 200

@app.route('/depoimento/tipo/<string:tipoDepoimento>', methods=["GET"])
def filtrarPorTipoDepoimento(tipoDepoimento):
    # Filtrar os depoimentos pelo tipo fornecido na rota
    depoimentos_filtrados = Depoimento.query.filter_by(tipoDepoimento = tipoDepoimento).all()
    
    if not depoimentos_filtrados:
        return jsonify({"message": "Nenhum depoimento encontrado para este tipo"}), 404
    
    # Converter os depoimentos filtrados em lista de dicionários
    depoimentos_dict = [depoimento.to_dict() for depoimento in depoimentos_filtrados]
    
    return jsonify(depoimentos_dict), 200

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host='localhost', debug=True)

