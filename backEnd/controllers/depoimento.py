from datetime import datetime
from flask import Blueprint, jsonify, request
from helpers.texto import padronizar_tipo_depoimento
from models.dblocalidade import *
from models.dbdepoimento import *
from .localidade import getLocalidade

depoimento_route = Blueprint('depoimento', __name__)


@depoimento_route.route('', methods=["POST"])
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

    localidade = Localidade.query.get(depoimento.id_localidade)
    if localidade:
        nome_localidade = localidade.local
        getLocalidade(nome_localidade)

    return jsonify(depoimento.to_dict()), 200


@depoimento_route.route('/<int:idDepoimento>', methods=["PATCH"])
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


@depoimento_route.route('/<int:idDepoimento>', methods=["DELETE"])
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

@depoimento_route.route('/tipo/<string:tipo_depoimento>/localidade/<int:id_localidade>', methods=["GET"])
def getPorTipoDepoimentoPorLocalidade(tipo_depoimento, id_localidade):
    depoimentos_filtrados = Depoimento.query.filter_by(tipo_depoimento=tipo_depoimento, id_localidade=id_localidade).all()
    
    if not depoimentos_filtrados:
        return jsonify([]), 200
    
    depoimentos_dict = [depoimento.to_dict() for depoimento in depoimentos_filtrados]
    
    return jsonify(depoimentos_dict), 200

@depoimento_route.route('/localidade/<int:id_localidade>', methods=["GET"])
def getTodosTipoDepoimentoPorLocalidade(id_localidade):
    depoimentos_filtrados = Depoimento.query.filter_by(id_localidade=id_localidade).all()
    
    if not depoimentos_filtrados:
        return jsonify([]), 200
    
    depoimentos_dict = [depoimento.to_dict() for depoimento in depoimentos_filtrados]

    return jsonify(depoimentos_dict), 200