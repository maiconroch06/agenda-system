from datetime import datetime, timezone
from database import db

class BarberShop(db.Model):
    __tablename__ = 'barbearias'

    # Chave Primária (CNPJ de 14 caracteres limpos)
    cnpj = db.Column(db.String(14), primary_key=True,  nullable=False)
    
    nome_barbearia = db.Column(db.String(100), nullable=False)
    telefone = db.Column(db.String(11), nullable=False)
    email_empresa = db.Column(db.String(150), nullable=False)
    logo_path = db.Column(db.String(255), nullable=False)
    
    # Controle de Data com o padrão moderno timezone-aware
    data_cadastro = db.Column(
        db.DateTime, 
        default=lambda: datetime.now(timezone.utc), 
        nullable=False
    )
    
    # Chaves Estrangeiras com Regra CASCADE
    endereco_barbearia_cnpj = db.Column(
        db.Integer, 
        db.ForeignKey('enderecos.id_endereco', onupdate='CASCADE', ondelete='CASCADE'), 
        nullable=False
    )

    gestor_id = db.Column(
        db.Integer, 
        db.ForeignKey('usuarios.id', onupdate='CASCADE', ondelete='CASCADE'), 
        nullable=False
    )
    # Metodo responsavel por retornar o cnpj da empresa
    # pode ser feito via consulta tbm
    def getCNPJ():
        return "41484370000129"

    # chamar o método pela própria classe
    # cls é uma convenção do Python que representa a própria classe
    @classmethod
    def insertDefualtBarbearia(cls, id_gestor, id_endereco:int):
        if cls.query.first() is None:

            barbearia = cls(
                    cnpj= cls.getCNPJ(),
                    nome_barbearia='TMS Barbearia',
                    telefone='84999999999',
                    email_empresa='contato@tmsbarbearia.com',
                    logo_path='default/logo.png',
                    endereco_barbearia_cnpj=id_endereco,
                    gestor_id=id_gestor
                )

            db.session.add(barbearia)
            db.session.commit()

            print('Barbearia cadastrada com sucesso.')

