from datetime import datetime, timezone
from database import db

class Barber(db.Model):
    __tablename__ = 'barbeiros'

    # Chaves Primárias Compostas e Chaves Estrangeiras Simples
    barbearia_cnpj = db.Column(
        db.String(14), 
        db.ForeignKey('barbearias.cnpj', onupdate='CASCADE', ondelete='CASCADE'), 
        primary_key=True, 
        nullable=False
    )
    barbeiro_id = db.Column(
        db.Integer, 
        db.ForeignKey('usuarios.id', onupdate='CASCADE', ondelete='CASCADE'), 
        primary_key=True, 
        nullable=False
    )
    
    ativo = db.Column(db.Boolean, default=True, nullable=False) 
    
    data_liberacao = db.Column(
        db.DateTime, 
        default=lambda: datetime.now(timezone.utc), 
        nullable=False
    )
