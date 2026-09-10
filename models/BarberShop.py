from datetime import datetime, timezone
from database import db

class BarberShop(db.Model):
    __tablename__ = 'barbearias'

    # Chave Primária (CNPJ de 14 caracteres limpos)
    cnpj = db.Column(db.String(14), primary_key=True, unique=True, nullable=False)
    
    nome_barbearia = db.Column(db.String(100), nullable=False)
    telefone = db.Column(db.String(11), nullable=False)
    email_empresa = db.Column(db.String(150), nullable=False)
    logo_path = db.Column(db.String(255), nullable=False)
    
    # Controle de Data com o padrão moderno timezone-aware
    data_cadastro = db.Column(
        db.DateTime, 
        default=lambda: datetime.now(timezone.utc), 
        nullable=False
    )
    
    # Chaves Estrangeiras com Regra CASCADE
    endereco_barbearia_cnpj = db.Column(
        db.Integer, 
        db.ForeignKey('enderecos.id_endereco', onupdate='CASCADE', ondelete='CASCADE'), 
        nullable=False
    )
    gestor_id = db.Column(
        db.Integer, 
        db.ForeignKey('usuarios.id', onupdate='CASCADE', ondelete='CASCADE'), 
        nullable=False
    )
