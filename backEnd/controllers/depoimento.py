from datetime import datetime
from flask import Blueprint, jsonify, request
from helpers.google import traduzir
from helpers.texto import padronizar_tipo_depoimento
from helpers.erros import erro_depoimento_nao_encontrado
from models.dblocalidade import *
from models.dbdepoimento import *
from .localidade import get_localidade
from sqlalchemy.exc import SQLAlchemyError, IntegrityError, NoResultFound

depoimento_route = Blueprint('depoimento', __name__)

@depoimento_route.route('', methods=["POST"])
def post_depoimento():
    try:
        dados = request.get_json()

        id_localidade = dados.get('id_localidade')
        tipo_depoimento = dados.get('tipo_depoimento')
        detalhes = dados.get('detalhes')

        if not id_localidade or not tipo_depoimento or not detalhes:
            return jsonify({"error": "Todos os campos são necessários"}), 400

        localidade = Localidade.query.get(id_localidade)
        if not localidade:
            return jsonify({"error": "Localidade não encontrada"}), 404

        depoimento_existente = Depoimento.query.filter(Depoimento.id_localidade == id_localidade) \
                                            .filter(Depoimento.tipo_depoimento == tipo_depoimento) \
                                            .filter(Depoimento.detalhes == detalhes) \
                                            .first()

        if depoimento_existente:
            return jsonify({"error": "Este depoimento já foi registrado"}), 409

        depoimento = Depoimento(
            id_localidade=localidade.id,
            tipo_depoimento=padronizar_tipo_depoimento(tipo_depoimento),
            detalhes=detalhes,
            data=datetime.now().date(),
            hora=datetime.now().time()
        )
        
        db.session.add(depoimento)
        db.session.commit()

        nome_localidade = localidade.local
        get_localidade(nome_localidade)

        return jsonify(depoimento.to_dict()), 200
    
    except Exception as e:
        return jsonify({"error": "Erro inesperado", "message": traduzir(str(e))}), 500
    


@depoimento_route.route('/<int:id_depoimento>', methods=["PATCH"])
def patch_depoimento(id_depoimento):
    try:
        dados = request.get_json()
        
        depoimento = Depoimento.query.get(id_depoimento)
        
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
            get_localidade(nome_localidade)
        
        return jsonify(depoimento.to_dict()), 200
    
    except NoResultFound:
        erro_depoimento_nao_encontrado(depoimento)
        
    except Exception as e:
        return jsonify({"error": "Erro inesperado", "message": traduzir(str(e))}), 500

@depoimento_route.route('/<int:id_depoimento>', methods=["DELETE"])
def delete_depoimento(id_depoimento):
    try:
        depoimento = Depoimento.query.get(id_depoimento)
        
        db.session.delete(depoimento)
        db.session.commit()

        localidade = Localidade.query.filter_by(id=depoimento.id_localidade).first()
        if localidade:
            get_todos_tipo_depoimento_por_localidade(localidade.id)
        
        return jsonify({"message": "Depoimento excluído com sucesso"}), 200
    
    except NoResultFound:
        erro_depoimento_nao_encontrado(depoimento)
        
    except Exception as e:
        return jsonify({"error": "Erro inesperado", "message": traduzir(str(e))}), 500

@depoimento_route.route('/tipo/<string:tipo_depoimento>/localidade/<int:id_localidade>', methods=["GET"])
def get_por_tipo_depoimento_por_localidade(tipo_depoimento, id_localidade):
    filtros = {
        "tipo_depoimento": tipo_depoimento,
        "id_localidade": id_localidade
    }
    return result_filter_depoimento(filtros)

@depoimento_route.route('/localidade/<int:id_localidade>', methods=["GET"])
def get_todos_tipo_depoimento_por_localidade(id_localidade):
    filtros = {
        "id_localidade": id_localidade
    }
    return result_filter_depoimento(filtros)

def result_filter_depoimento(filtros):    
    try:
        depoimentos_filtrados = Depoimento.query.filter_by(**filtros).all()
        
        if not depoimentos_filtrados:
            return jsonify([]), 200
        
        depoimentos_dict = [depoimento.to_dict() for depoimento in depoimentos_filtrados]
        return jsonify(depoimentos_dict), 200
    
    except NoResultFound:
        erro_depoimento_nao_encontrado(depoimentos_filtrados)
    
    except SQLAlchemyError as e:
        return jsonify({"error": "Erro ao acessar o banco de dados", "message": traduzir(str(e))}), 500