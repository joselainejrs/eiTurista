from flask_sqlalchemy import SQLAlchemy
from googletrans import Translator

db = SQLAlchemy()

def traduzir(texto):
        translator = Translator()
        traducao = translator.translate(texto, src='en', dest='pt')
        return traducao.text

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

class Depoimento(db.Model):
    idDepoimento = db.Column(db.Integer, primary_key=True, autoincrement=True)
    localidade_id = db.Column(db.Integer, db.ForeignKey('localidade.id'))
    tipoDepoimento = db.Column(db.String)
    detalhes = db.Column(db.String)
    data = db.Column(db.Date)
    hora = db.Column(db.Time)


    def to_dict(self):
        data_formatada = self.data.strftime("%d/%m/%Y")
        hora_formatada = self.hora.strftime("%H:%M")

        return {
            'idDepoimento': self.idDepoimento,
            'localidade_id': self.localidade_id,
            'tipoDepoimento': self.tipoDepoimento,
            'detalhes': self.detalhes,
            'data': data_formatada,
            'hora': hora_formatada
        }


