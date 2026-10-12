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
    foto_nome = db.Column(db.String(45), nullable=True, default='default.png')
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
                "foto_nome":self.foto_nome,
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
                    select * FROM servicos
                """
            )
        )

        return resultado.mappings().all()

    @classmethod    
    def consultarIdServico(cls, id:int):
        resultado = db.session.execute( 
            db.text(
                    """
                        select * FROM servicos where id=:id
                    """
            ),{
                "id": id
            }
        )
    
        return resultado.mappings().first()

    @classmethod    
    def consultarIdServicoValido(cls, id:int):
        resultado = db.session.execute( 
            db.text(
                        """
                            select count(id) FROM servicos where ativo = 1 and id=:id
                        """
                ),{
                    "id": id
                }
            )
        
        return resultado.mappings().first()
   
    @staticmethod
    def deletarServico(id: int):
                
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

    
    def atualizarServico(self):
                
        resultado = db.session.execute( 
             db.text(
                """
                 update servicos set descricao = :descricao, valor=:valor,duracao=:duracao,foto_nome=:foto_nome,ativo=:ativo,data_atualizacao=:data_atualizacao  where id = :id
                """
            ),{
                "id": self.id,
                "descricao": self.descricao,
                "valor": self.valor,
                "duracao":self.duracao,
                "foto_nome":self.foto_nome,
                "ativo": self.ativo,
                "data_atualizacao":self.data_atualizacao
            }
        )
        
        return resultado
    
    
    @staticmethod
    def dataFormatada() -> datetime:
        return datetime.now(timezone.utc)



    