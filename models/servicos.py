from datetime import datetime, timezone
from database import db
from sqlalchemy.dialects.mysql import TINYINT

class Servicos(db.Model):
    __tablename__ = 'servicos'

    # Chave Primária
    id = db.Column(db.Integer, primary_key=True)
    
    descricao = db.Column('descricao', db.String(255), nullable=False)  
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
        
    def salvarServico(self):
        resultado = db.session.execute(
            
            db.text(
                """
                    INSERT INTO servicos (descricao,valor,duracao,foto_nome,ativo,data_cadastro, data_atualizacao)
                     values(:descricao, :valor, :duracao, :foto_nome, :ativo, :data_cadastro, :data_atualizacao)
                """
            ),{
               "descricao":self.descricao,
                "valor": self.valor,
                "duracao": self.duracao,
                "foto_nome":"teste",
                "ativo": 1,
                "data_cadastro":datetime.now(timezone.utc),
                "data_atualizacao":datetime.now(timezone.utc)
            }
        )

        return resultado.lastrowid

    @classmethod    
    def consultarTodosOsServicos(cls):
        resultado = db.session.execute( 
            db.text(
                """
                    select * FROM servicos where ativo = 1
                """
            )
        )

        return resultado.mappings().all()

   
    def deletarServico(self, id: int):
                
        db.session.execute( 
                db.text(
                    """
                    DELETE FROM servicos WHERE id = :id
                    """
                ),{
                    "id": id
                }
        )
    
        return 1

    def atualizarServico(self, id: int):
                
        db.session.execute( 
             db.text(
                """
                 update servicos set ....  where id = :id
                """
            ),{
                "id": id
            }
            )
    
        return 1

    