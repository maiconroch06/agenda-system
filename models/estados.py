from database import db
from sqlalchemy import text

class Estados(db.Model):
    __tablename__ = 'estados'

    # Chave Primária e Configurações de Identificação
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)    
    sigla_estado = db.Column(db.CHAR(2), nullable=False)   

    def consultarTodosEstados():
        sql = text("""
            select * from estados    
        """)  
        resultado = db.session.execute(sql) # retorna um resultset
        return  resultado.fetchall()  # pega todos os registros retornados por uma consulta SQL e coloca em uma lista.

    @classmethod
    def inserirEstadosDefault(cls):

        estados_padrao = cls.consultarTodosEstados()
        

        if not estados_padrao :
            sql = text("""
                insert into estados (sigla_estado) values (:sigla_estado)
                """)

            db.session.execute(sql,
            [
            {"sigla_estado": "AC"},
            {"sigla_estado": "AL"},
            {"sigla_estado": "AP"},
            {"sigla_estado": "AM"},
            {"sigla_estado": "BA"},
            {"sigla_estado": "CE"},
            {"sigla_estado": "DF"},
            {"sigla_estado": "ES"},
            {"sigla_estado": "GO"},
            {"sigla_estado": "MA"},
            {"sigla_estado": "MT"},
            {"sigla_estado": "MS"},
            {"sigla_estado": "MG"},
            {"sigla_estado": "PA"},
            {"sigla_estado": "PB"},
            {"sigla_estado": "PR"},
            {"sigla_estado": "PE"},
            {"sigla_estado": "PI"},
            {"sigla_estado": "RJ"},
            {"sigla_estado": "RN"},
            {"sigla_estado": "RS"},
            {"sigla_estado": "RO"},
            {"sigla_estado": "RR"},
            {"sigla_estado": "SC"},
            {"sigla_estado": "SP"},
            {"sigla_estado": "SE"},
            {"sigla_estado": "TO"}
            ])

           
            return 1

        return 0

   