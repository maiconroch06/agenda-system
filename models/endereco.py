from database import db
from sqlalchemy import text

class Endereco(db.Model):
    __tablename__ = 'enderecos'

    # Chave Primária e Configurações de Identificação
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
        
    cep = db.Column(db.String(10), nullable=False)        
    cidade = db.Column(db.String(40), nullable=False)     
    numero = db.Column(db.Integer, nullable=False)        
    bairro = db.Column(db.String(150), nullable=False)    
    sequencia = db.Column(db.Integer, nullable=True)      
    complemento = db.Column(db.String(100), nullable=True)
    fk_estado =  db.Column(db.Integer, db.ForeignKey('estados.id'), nullable=True)     

    def __init__(
        self,
        cep,
        cidade,
        numero,
        bairro,
        estado,
        sequencia=None,
        complemento=None
    ):
        self.cep = cep
        self.cidade = cidade
        self.numero = numero
        self.bairro = bairro
        self.fk_estado = estado
        self.sequencia = sequencia
        self.complemento = complemento

    def consultarEnderecoInicial():
        sql = text("""
                    select * from enderecos limit 1    
                """)  
        resultado = db.session.execute(sql) # retorna um resultset
        return  resultado.fetchall() # pega todos os registros retornados por uma consulta SQL e coloca em uma lista.

    def inserirEndereco(self):
        resultado = db.session.execute(
                        db.text("""
                            INSERT INTO enderecos
                            (
                                cep,
                                cidade,
                                numero,
                                bairro,
                                sequencia,
                                complemento,
                                fk_estado
                            )
                            VALUES
                            (
                                :cep,
                                :cidade,
                                :numero,
                                :bairro,
                                :sequencia,
                                :complemento,
                                :fk_estado
                            )
                        """),
                        {
                            "cep": self.cep,
                            "cidade":self.cidade,
                            "numero": self.numero,
                            "bairro": self.bairro,
                            "sequencia": self.sequencia,
                            "complemento": self.complemento,
                            "fk_estado": self.fk_estado
                        }
                    )
        
                        
        return resultado.lastrowid

    @classmethod
    def inserirEnderecoPadrao(cls):

        endereco_padrao = cls.consultarEnderecoInicial()
        
        if not endereco_padrao: # Verifica se não existe endereço padrão cadastrado
            cls.cep = "59215000"
            cls.cidade= "Nova Cruz"
            cls.numero= 55
            cls.bairro= "Centro"
            cls.sequencia= None
            cls.complemento= None
            cls.fk_estado= 20
                     
            return cls.inserirEndereco(cls)

        return -1