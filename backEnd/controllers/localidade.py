from flask import Blueprint, jsonify
from services.openweather import get_open_weather
from helpers.calcelsius import formula_celsius
from models.dblocalidade import *
from models.dbdepoimento import *

localidade_route = Blueprint('localidade', __name__)

@localidade_route.route('/localidade/<string:localidade>', methods=["GET"])
def get_localidade(localidade: str):
    try:
        resp = get_open_weather(localidade)

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
                    temp_max=formula_celsius(temp_max),
                    temp_min=formula_celsius(temp_min),
                    sensacao_termica=formula_celsius(sensacao_termica)
                )
                db.session.add(localidade)
            else:
                localidade.descricao = descricao
                localidade.temp_max = formula_celsius(temp_max)
                localidade.temp_min = formula_celsius(temp_min)
                localidade.sensacao_termica = formula_celsius(sensacao_termica)

            db.session.commit()

            depoimentos = Depoimento.query.filter_by(id_localidade=localidade.id).all()
            depoimentos_list = [depoimento.to_dict() for depoimento in depoimentos]

            response = {
                'localidade': localidade.to_dict(),
                'depoimentos': depoimentos_list
            }

            return jsonify(response)
        
    except Exception as e:
        if hasattr(e, 'code') and e.code == 404:
            return jsonify({'error': 'Não encontrado'}), 404
        else:
            return jsonify({"error": "Erro inesperado", "message": str(e)}), 500
