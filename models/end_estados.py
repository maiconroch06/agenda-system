from database import db

class Estados(db.Model):
    __tablename__ = 'enderecos'

    # Chave Primária e Configurações de Identificação
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
        
    sigla_estado = db.Column(db.String(2), nullable=False)        
   

   