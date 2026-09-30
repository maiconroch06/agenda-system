from datetime import datetime, timezone
from database import db
from sqlalchemy import text

class Barbearia(db.Model):

    # Chave Primária (CNPJ de 14 caracteres limpos)
    cnpj = db.Column(db.CHAR(14), primary_key=True,  nullable=False)
    
    nome_barbearia = db.Column(db.String(150), nullable=False)
    telefone = db.Column(db.String(11), nullable=False, unique=True)
    email_empresa = db.Column(db.String(150), nullable=False, unique=True)
    logo_barbearia = db.Column(db.String(255), nullable=False)
    
    # Controle de Data com o padrão moderno timezone-aware
    data_cadastro = db.Column(
        db.DateTime, 
        default=lambda: datetime.now(timezone.utc), 
        nullable=False
    )
    
    # Chaves Estrangeiras com Regra CASCADE
    fk_id_endereco = db.Column(
        db.Integer, 
        db.ForeignKey('enderecos.id', onupdate='RESTRICT', ondelete='RESTRICT'), 
        nullable=False
    )

    def getCNPJ():
        return "00000000000101"

    # Metodo responsavel por retornar o cnpj da empresa
    # pode ser feito via consulta tbm
    def consultarBarbearia():
       return db.session.execute ( 
           db.text("""
            SELECT * from barbearia limit 1
            """)  
            ).fetchall()

    # chamar o método pela própria classe
    # cls é uma convenção do Python que representa a própria classe
    @classmethod
    def inserirBarbeariaPadrao(cls, id_endereco:int):
        
        barbearia = cls.consultarBarbearia()
        print("barbearia", barbearia )
        if not barbearia:

            db.session.execute(
                    db.text("""
                        INSERT INTO barbearia
                        (
                            cnpj,
                            nome_barbearia,
                            telefone,
                            email_empresa,
                            logo_barbearia,
                            data_cadastro,
                            fk_id_endereco
                        )
                        VALUES
                        (
                            :cnpj,
                            :nome_barbearia,
                            :telefone,
                            :email_empresa,
                            :logo_barbearia,
                            :data_cadastro,
                            :fk_id_endereco
                        )
                    """),
                    {
                        "cnpj": cls.getCNPJ(),
                        "nome_barbearia": "TMS Barbearia",
                        "telefone": "84999999999",
                        "email_empresa": "contato@tmsbarbearia.com",
                        "logo_barbearia": "default/logo.png",
                        "data_cadastro": datetime.now(),
                        "fk_id_endereco": id_endereco
                    }
                )

            db.session.commit()

            print('Barbearia cadastrada com sucesso.')

            return cls.getCNPJ()

        return None
