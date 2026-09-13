from database import db

class DaysWeek(db.Model):
    __tablename__ = 'dias_da_semana'

    # Chave Primária
    id = db.Column(db.Integer, primary_key=True)
    
    nome_dia = db.Column(db.String(15), nullable=False)

    # Construtor para facilitar inserções manuais
    def __init__(self, id, nome_dia):
        self.id = id
        self.nome_dia = nome_dia

    # Serializador para respostas JSON
    def to_dict(self):
        return {
            'id': self.id,
            'nome_dia': self.nome_dia
        }
