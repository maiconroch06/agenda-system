from database import db


class Cliente(db.Model):
    __tablename__ = 'clientes'

    id = db.Column(
        db.Integer, 
        db.ForeignKey('usuarios.id', onupdate='CASCADE', ondelete='CASCADE'), 
        primary_key=True, 
        nullable=False
    )
    data_ultimo_servico = db.Column(db.DateTime,  nullable=True)

    # 2. Construtor para salvar na tabela clientes
    def __init__(self, cliente_id:int):
            self.barbearia_cnpj = Barbearia.getCNPJ()
            self.cliente_id = cliente_id 


    # CREATE - Salva o usuário e retorna o ID auto-incremental gerado pelo MySQL
    def salvar(self):
        db.session.add(self)
        db.session.commit()
        return self.cliente_id
