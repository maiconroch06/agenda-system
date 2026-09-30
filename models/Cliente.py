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
            self.id  = cliente_id 


    # CREATE - Salva o usuário e retorna o ID auto-incremental gerado pelo MySQL
    def salvar(self):
        db.session.add(self)
        db.session.commit()
        return self.id

    @classmethod
    def buscarCLientePorEmail(cls, email):
        return db.session.execute(
            db.text(
            """
                select *
                from clientes c join usuarios u 
                on c.id = u.id where u.email = :email
            """
                ),
                {"email":email}
        ).first()
