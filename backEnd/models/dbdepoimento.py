from . import db

class Depoimento(db.Model):
    id_depoimento = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_localidade = db.Column(db.Integer, db.ForeignKey('localidade.id'))
    tipo_depoimento = db.Column(db.String)
    detalhes = db.Column(db.String)
    data = db.Column(db.Date)
    hora = db.Column(db.Time)

    def to_dict(self):
        data_formatada = self.data.strftime("%d/%m/%Y")
        hora_formatada = self.hora.strftime("%H:%M")

        return {
            'id_depoimento': self.id_depoimento,
            'id_localidade': self.id_localidade,
            'tipo_depoimento': self.tipo_depoimento,
            'detalhes': self.detalhes,
            'data': data_formatada,
            'hora': hora_formatada
        }


