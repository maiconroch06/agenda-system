from datetime import datetime, timezone
from database import db
from sqlalchemy.dialects.mysql import TINYINT

class Servicos(db.Model):
    __tablename__ = 'servicos'

    # Chave Primária
    id = db.Column(db.Integer, primary_key=True)
    
    descricao = db.Column('descrição', db.String(255), nullable=False)  
    valor = db.Column(db.Numeric(10, 2), nullable=False)                
    duracao = db.Column(db.Integer, nullable=False)                     
    foto_nome = db.Column(db.String(45), nullable=False)
    ativo = db.Column(TINYINT(1),  nullable=False)         
    
    data_cadastro = db.Column(
        db.DateTime, 
        default=lambda: datetime.now(timezone.utc), 
        nullable=False
    )
    
    data_atualizacao = db.Column(
            db.DateTime, 
            default=lambda: datetime.now(timezone.utc), 
            nullable=False
        )
    