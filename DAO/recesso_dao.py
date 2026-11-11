
from sqlalchemy import text
from database import db

from models import Recesso
from DAO.mes_referencia_dao import MesReferenciaDAO


class RecessoDAO:

    def __init__(self):
        self.__mesReferenciaDao = MesReferenciaDAO()

    def cadastrar(self, recesso: Recesso):
        sql = text("""
            INSERT INTO recesso (
                data_dia,
                descricao_feriado,
                fk_mes_agenda
            ) VALUES (
                :data_dia,
                :descricao_feriado,
                :fk_mes_agenda
            )
        """)

        resultado = db.session.execute(sql, {
            "data_dia": recesso.data_dia,
            "descricao_feriado": recesso.descricao_feriado,
            "fk_mes_agenda": recesso.mes_referencia.id_mes_referencia
        })

        db.session.commit()

        return resultado.lastrowid

    def buscar_por_id(self, id_recesso: int):
        sql = text("""
            SELECT
                id_recesso,
                data_dia,
                descricao_feriado,
                fk_mes_agenda
            FROM recesso
            WHERE id_recesso = :id_recesso
        """)

        resultado = db.session.execute(
            sql,
            {"id_recesso": id_recesso}
        ).mappings().first()

        if not resultado:
            return None

        return self.__mapear_recesso(resultado)

    def listar_por_mes_referencia(self, id_mes_referencia: int):
        sql = text("""
            SELECT
                id_recesso,
                data_dia,
                descricao_feriado,
                fk_mes_agenda
            FROM recesso
            WHERE fk_mes_agenda = :id_mes_referencia
            ORDER BY data_dia
        """)

        resultados = db.session.execute(
            sql,
            {"id_mes_referencia": id_mes_referencia}
        ).mappings().all()

        return [
            self.__mapear_recesso(registro)
            for registro in resultados
        ]

    def listar_todos(self):
        sql = text("""
            SELECT
                id_recesso,
                data_dia,
                descricao_feriado,
                fk_mes_agenda
            FROM recesso
            ORDER BY data_dia
        """)

        resultados = db.session.execute(sql).mappings().all()

        return [
            self.__mapear_recesso(registro)
            for registro in resultados
        ]

    def atualizar(self, recesso: Recesso):
        sql = text("""
            UPDATE recesso
            SET
                data_dia = :data_dia,
                descricao_feriado = :descricao_feriado,
                fk_mes_agenda = :fk_mes_agenda
            WHERE id_recesso = :id_recesso
        """)

        resultado = db.session.execute(sql, {
            "id_recesso": recesso.id_recesso,
            "data_dia": recesso.data_dia,
            "descricao_feriado": recesso.descricao_feriado,
            "fk_mes_agenda": recesso.mes_referencia.id_mes_referencia
        })

        db.session.commit()

        return resultado.rowcount > 0

    def excluir(self, id_recesso: int):
        sql = text("""
            DELETE FROM recesso
            WHERE id_recesso = :id_recesso
        """)

        resultado = db.session.execute(
            sql,
            {"id_recesso": id_recesso}
        )

        db.session.commit()

        return resultado.rowcount > 0

    def __mapear_recesso(self, registro):
        mes_referencia = self.__mesReferenciaDao.buscar_por_id(
            registro["fk_mes_agenda"]
        )

        return Recesso(
            id_recesso=registro["id_recesso"],
            data_dia=registro["data_dia"],
            descricao_feriado=registro["descricao_feriado"],
            mes_referencia=mes_referencia
        )
