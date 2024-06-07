from helpers.google import traduzir
from . import db

class Localidade(db.Model):
    id = db.Column(db.Integer, primary_key=True,)
    local = db.Column(db.String, unique=True,)
    pais = db.Column(db.String(2))
    descricao = db.Column(db.String)
    temp_max = db.Column(db.Integer)
    temp_min = db.Column(db.Integer)
    sensacao_termica = db.Column(db.Integer)
    depoimentos = db.relationship('Depoimento', backref='localidade', lazy=True)
   
    def to_dict(self):
        return {
            'id': self.id,
            'local': self.local,
            'pais': self.pais,
            'descricao': traduzir(self.descricao),
            'temp_max': self.temp_max,
            'temp_min': self.temp_min,
            'sensacao_termica': self.sensacao_termica
        }