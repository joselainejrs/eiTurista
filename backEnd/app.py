# from flask_cors import CORS
# from datetime import datetime
# from flask_migrate import Migrate
# from flask import Flask, jsonify, request
# from model.dblocalidade import *
# from model.dbdepoimento import *
# from services.openweather import getOpenWeather
# from helpers.texto import padronizar_tipo_depoimento
# from helpers.calcelsius import formula_celsius

# app = Flask(__name__)
# CORS(app)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///eiTurista.db'
# db.init_app(app)
# migrate = Migrate(app, db)

# @app.route('/localidade/<str:localidade>', methods=["GET"])
# def getLocalidade(localidade: str):
#     resp = getOpenWeather(localidade)

#     if resp.status_code == 200:
#         dados = resp.json()
#         id = dados['id']
#         local = dados['name']
#         pais = dados['sys']['country']
#         descricao = dados['weather'][0]['description']
#         temp_max = dados['main']['temp_max']
#         temp_min = dados['main']['temp_min']
#         sensacao_termica = dados['main']['feels_like']

#         localidade = Localidade.query.filter_by(local=local).first()
#         if not localidade:
#             localidade = Localidade(
#                 id=id,
#                 local=local,
#                 pais=pais,
#                 descricao=descricao,
#                 temp_max=formula_celsius(temp_max),
#                 temp_min=formula_celsius(temp_min),
#                 sensacao_termica=formula_celsius(sensacao_termica)
#             )
#             db.session.add(localidade)
#         else:
#             localidade.descricao = descricao
#             localidade.temp_max = formula_celsius(temp_max)
#             localidade.temp_min = formula_celsius(temp_min)
#             localidade.sensacao_termica = formula_celsius(sensacao_termica)
        
#         db.session.commit()

#         depoimentos = Depoimento.query.filter_by(id_localidade=localidade.id).all()
#         depoimentos_list = [depoimento.to_dict() for depoimento in depoimentos]

#         response = {
#             'localidade': localidade.to_dict(),
#             'depoimentos': depoimentos_list
#         }
        
#         return jsonify(response)
#     elif resp.status_code == 404:
#         return jsonify({'error': 'não encontrado'}), 404


# @app.route('/depoimento', methods=["POST"])
# def postDepoimento():
#     dados = request.get_json()

#     id_localidade = dados.get('id_localidade')
#     tipo_depoimento = dados.get('tipo_depoimento')
#     detalhes = dados.get('detalhes')

#     if not id_localidade or not tipo_depoimento or not detalhes:
#         return jsonify({"error": "Todos os campos são necessários"}), 400
    
#     depoimento_existente = Depoimento.query.filter(Depoimento.id_localidade == id_localidade) \
#                                            .filter(Depoimento.tipo_depoimento == tipo_depoimento) \
#                                            .filter(Depoimento.detalhes == detalhes) \
#                                            .first()
#     if depoimento_existente:
#         return jsonify({"error": "Este depoimento já foi registrado"}), 409 
    
#     localidade = Localidade.query.get(id_localidade)
#     if not localidade:
#         return jsonify({"error": "Localidade não encontrada"}), 404
       
#     depoimento = Depoimento(
#         id_localidade = localidade.id,
#         tipo_depoimento = padronizar_tipo_depoimento(tipo_depoimento),
#         detalhes = detalhes,
#         data = datetime.now().date(),
#         hora = datetime.now().time()
#     )
    
#     db.session.add(depoimento)
#     db.session.commit()

#     localidade = Localidade.query.get(depoimento.id_localidade)
#     if localidade:
#         nome_localidade = localidade.local
#         getLocalidade(nome_localidade)

#     return jsonify(depoimento.to_dict()), 200


# @app.route('/depoimento/<int:idDepoimento>', methods=["PATCH"])
# def patchDepoimento(idDepoimento):
#     dados = request.get_json()
    
#     depoimento = Depoimento.query.get(idDepoimento)
    
#     if not depoimento:
#         return jsonify({"error": "Depoimento não encontrado"}), 404
        
#     if 'tipo_depoimento' in dados:
#         depoimento.tipo_depoimento = padronizar_tipo_depoimento(dados['tipo_depoimento'])
#     if 'detalhes' in dados:
#         depoimento.detalhes = dados['detalhes']

#     depoimento.data = datetime.now().date()
#     depoimento.hora = datetime.now().time()
    
#     db.session.commit()

#     localidade = Localidade.query.get(depoimento.id_localidade)
#     if localidade:
#         nome_localidade = localidade.local
#         getLocalidade(nome_localidade)
    
#     return jsonify(depoimento.to_dict()), 200


# @app.route('/depoimento/<int:idDepoimento>', methods=["DELETE"])
# def deleteDepoimento(idDepoimento):
#     depoimento = Depoimento.query.get(idDepoimento)
    
#     if not depoimento:
#         return jsonify({"error": "Depoimento não encontrado"}), 404
    
#     db.session.delete(depoimento)
#     db.session.commit()

#     localidade = Localidade.query.filter_by(id=depoimento.id_localidade).first()
#     if localidade:
#         getTodosTipoDepoimentoPorLocalidade(localidade.id)

    
#     return jsonify({"message": "Depoimento excluído com sucesso"}), 200

# @app.route('/depoimento/tipo/<string:tipo_depoimento>/localidade/<int:id_localidade>', methods=["GET"])
# def getPorTipoDepoimentoPorLocalidade(tipo_depoimento, id_localidade):
#     depoimentos_filtrados = Depoimento.query.filter_by(tipo_depoimento=tipo_depoimento, id_localidade=id_localidade).all()
    
#     if not depoimentos_filtrados:
#         return jsonify([]), 200
    
#     depoimentos_dict = [depoimento.to_dict() for depoimento in depoimentos_filtrados]
    
#     return jsonify(depoimentos_dict), 200

# @app.route('/depoimento/localidade/<int:id_localidade>', methods=["GET"])
# def getTodosTipoDepoimentoPorLocalidade(id_localidade):
#     depoimentos_filtrados = Depoimento.query.filter_by(id_localidade=id_localidade).all()
    
#     if not depoimentos_filtrados:
#         return jsonify([]), 200
    
#     depoimentos_dict = [depoimento.to_dict() for depoimento in depoimentos_filtrados]

#     return jsonify(depoimentos_dict), 200

        
# if __name__ == "__main__":
#     with app.app_context():
#         db.create_all()
#     app.run(host='localhost', debug=True)

from flask import Flask
from flask_migrate import Migrate
from flask_cors import CORS
from controllers.localidade import localidade_route
from controllers.depoimento import depoimento_route
from models import db

import logging

# Configurar logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///eiTurista.db'
db.init_app(app)
migrate = Migrate(app, db)

# Registrar Blueprints
app.register_blueprint(localidade_route)
app.register_blueprint(depoimento_route, url_prefix='/depoimento')

logging.info("Registered blueprint for localidade")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        logging.info("Starting Flask app")
    app.run(host='localhost', debug=True)
