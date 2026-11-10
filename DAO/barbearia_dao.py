
from sqlalchemy import text
from database import db
from models import Barbearia


class BarbeariaDAO:

    @staticmethod
    def buscar_por_cnpj(cnpj: str):
        sql = text("""
            SELECT *
            FROM barbearia
            WHERE cnpj = :cnpj
        """)

        registro = db.session.execute(
            sql,
            {"cnpj": cnpj}
        ).mappings().first()

        if registro is None:
            return None

        return BarbeariaDAO._mapear_barbearia(registro)

