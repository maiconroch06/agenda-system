from database import db
from .BarberShop import BarberShop


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

    # 2. Construtor para salvar na tabela clientes
    def __init__(self, cliente_id:int):
            self.barbearia_cnpj = BarberShop.getCNPJ()
            self.cliente_id = cliente_id 


    # CREATE - Salva o usuário e retorna o ID auto-incremental gerado pelo MySQL
    def salvar(self):
        db.session.add(self)
        db.session.commit()
        return self.cliente_id
