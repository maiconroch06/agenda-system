from database import db
from sqlalchemy.dialects.mysql import TINYINT

class barbeiroHasServicos(db.Model):
    __tablename__ = 'barbeiro_has_servicos'

    # Chaves Primárias Compostas e Chaves Estrangeiras
    id_servicos = db.Column(
        db.Integer, 
        db.ForeignKey('servicos.id', onupdate='RESTRICT', ondelete='RESTRICT'), 
        primary_key=True, 
        nullable=False
    )

    id_barbeiro = db.Column(
        db.Integer, 
        db.ForeignKey('barbeiros.id', onupdate='RESTRICT', ondelete='RESTRICT'), 
        primary_key=True, 
        nullable=False
    )
    
    ativo = db.Column(TINYINT(1), nullable=False)
