from database import db
from sqlalchemy.dialects.mysql import TINYINT

class Barbeiro(db.Model):
    __tablename__ = 'barbeiros'

    id = db.Column(
        db.Integer, 
        db.ForeignKey('usuarios.id', onupdate='CASCADE', ondelete='CASCADE'), 
        primary_key=True, 
        nullable=False
    )
    data_liberacao = db.Column(db.DateTime, nullable = True )
    ativo = db.Column(TINYINT(1), nullable=False) 
    
    descricao = db.Column(
        db.String(500), 
        nullable=False
    )

    # CREATE - Salva o usuário e retorna o ID auto-incremental gerado pelo MySQL
    def salvar(self):
        db.session.execute(
            db.text(
                """
                insert into barbeiros (id, data_liberacao,ativo,descricao) values (:id,:data_liberacao,:ativo,:descricao)
                """
            ),{
                "id": self.id,
                "data_liberacao":self.data_liberacao,
                "ativo": self.ativo,
                "descricao": self.descricao
            }
        )

        
    # CREATE - Salva o usuário e retorna o ID auto-incremental gerado pelo MySQL
    def consultarBarbeiros(self):
        return db.session.execute(
            db.text(
                    """
                    SELECT * FROM barbeiros b inner join usuarios u on b.id = u.id 
            
                     """
                 )
             ).mappings().all()  

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
