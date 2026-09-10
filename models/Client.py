from database import db

class Client(db.Model):
    __tablename__ = 'clientes'

    # O parêntese do ForeignKey agora fecha DEPOIS do ondelete/onupdate
    barbearia_cnpj = db.Column(
        db.String(14), 
        db.ForeignKey('barbearias.cnpj', onupdate='CASCADE', ondelete='CASCADE'), 
        primary_key=True, 
        nullable=False
    )
    
    cliente_id = db.Column(
        db.Integer, 
        db.ForeignKey('usuarios.id', onupdate='CASCADE', ondelete='CASCADE'), 
        primary_key=True, 
        nullable=False
    )
