from flask import jsonify

def erro_depoimento_nao_encontrado(tipo):
    if not tipo:
            return jsonify({"error": "Depoimento não encontrado"}), 404
