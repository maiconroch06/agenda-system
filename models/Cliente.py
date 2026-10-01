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

    # 1. Construtor para salvar na tabela clientes
    def __init__(self, cliente_id:int = None):
         # Comportamento do Construtor 1 (Salvando com ID)
        if cliente_id is not None:
           
            self.id = cliente_id
        # Comportamento do Construtor 2 (Criando vazio)
        else:
            
            self.id = None



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

    @staticmethod  
    def buscarTodosCLientes():
        return db.session.execute(
                db.text(
                """
                    select u.nome_completo, u.telefone, c.data_ultimo_servico
                    from clientes c join usuarios u 
                    on c.id = u.id
                """
                    )
            ).all()
