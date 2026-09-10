from datetime import datetime, timezone
from database import db

class Servico(db.Model):
    __tablename__ = 'servicos'

    # Chave Primária
    id_servicos = db.Column(db.Integer, primary_key=True)
    
    descricao = db.Column('descrição', db.String(255), nullable=False)  
    valor = db.Column(db.Numeric(10, 2), nullable=False)                
    duracao = db.Column(db.Integer, nullable=False)                     
    imagem = db.Column(db.String(45), nullable=False)
    ativo = db.Column(db.Boolean, default=True, nullable=False)         
    
    data_cadastro = db.Column(
        db.DateTime, 
        default=lambda: datetime.now(timezone.utc), 
        nullable=False
    )
    
    barbearia_cnpj = db.Column(
        db.String(14), 
        db.ForeignKey('barbearias.cnpj', onupdate='CASCADE', ondelete='CASCADE'), 
        nullable=False
    )
