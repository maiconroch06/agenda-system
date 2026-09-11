from database import db

class Address(db.Model):
    __tablename__ = 'enderecos'

    # Chave Primária e Configurações de Identificação
    id_endereco = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
        
    cep = db.Column(db.String(10), nullable=False)        
    cidade = db.Column(db.String(40), nullable=False)     
    numero = db.Column(db.Integer, nullable=False)        
    bairro = db.Column(db.String(150), nullable=False)    
    estado = db.Column(db.String(2), nullable=False)      
    sequencia = db.Column(db.Integer, nullable=True)      
    complemento = db.Column(db.String(100), nullable=True) 

    def __init__(self, cep, cidade, numero, bairro, estado, sequencia=None, complemento=None):
        self.cep = cep
        self.cidade = cidade if (cidade := cidade) else None
        self.cidade = cidade
        self.numero = numero
        self.bairro = bairro
        self.estado = estado
        self.sequencia = sequencia
        self.complemento = complemento

    # Serializador para converter o endereço em dicionário/JSON se precisar
    def to_dict(self):
        return {
            'id_endereco': self.id_endereco,
            'cep': self.cep,
            'cidade': self.cidade,
            'numero': self.numero,
            'bairro': self.bairro,
            'estado': self.estado,
            'sequencia': self.sequencia,
            'complemento': self.complemento
        }

    @classmethod
    def insertDefaultAdress(cls):
        if cls.query.first() is None:

            adress_default = cls(
                cep = "59215-000",
                cidade = "Nova Cruz",
                numero = 55,
                bairro = "Centro",
                estado = "RN",
                sequencia = None,
                complemento = None
                    )

            db.session.add(adress_default)
            db.session.commit()
                
            return adress_default.id_endereco
        return cls.query.first().id_endereco;