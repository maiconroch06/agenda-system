
from sqlalchemy import text
from database import db

from models import MesReferencia
from DAO.agenda_dao import AgendaDAO


class MesReferenciaDAO:

    def __init__(self):
        self.__agendaDao = AgendaDAO()

    def cadastrar(self, mes_referencia: MesReferencia):
        sql = text("""
            INSERT INTO mes_referencia (
                data_inicial_mes,
                data_final_mes,
                nome_mes,
                fk_id_agenda
            ) VALUES (
                :data_inicial_mes,
                :data_final_mes,
                :nome_mes,
                :fk_id_agenda
            )
        """)

        resultado = db.session.execute(sql, {
            "data_inicial_mes": mes_referencia.data_inicial_mes,
            "data_final_mes": mes_referencia.data_final_mes,
            "nome_mes": mes_referencia.nome_mes,
            "fk_id_agenda": mes_referencia.agenda.id
        })

        db.session.commit()

        return resultado.lastrowid

    def buscar_por_id(self, id_mes_referencia: int):
        sql = text("""
            SELECT
                id_mes_referencia,
                data_inicial_mes,
                data_final_mes,
                nome_mes,
                fk_id_agenda
            FROM mes_referencia
            WHERE id_mes_referencia = :id_mes_referencia
        """)

        resultado = db.session.execute(
            sql,
            {"id_mes_referencia": id_mes_referencia}
        ).mappings().first()

        if not resultado:
            return None

        return self.__mapear_mes_referencia(resultado)

    def listar_por_agenda(self, id_agenda: int):
        sql = text("""
            SELECT
                id_mes_referencia,
                data_inicial_mes,
                data_final_mes,
                nome_mes,
                fk_id_agenda
            FROM mes_referencia
            WHERE fk_id_agenda = :id_agenda
            ORDER BY data_inicial_mes
        """)

        resultados = db.session.execute(
            sql,
            {"id_agenda": id_agenda}
        ).mappings().all()

        return [
            self.__mapear_mes_referencia(registro)
            for registro in resultados
        ]

    def listar_todos(self):
        sql = text("""
            SELECT
                id_mes_referencia,
                data_inicial_mes,
                data_final_mes,
                nome_mes,
                fk_id_agenda
            FROM mes_referencia
            ORDER BY data_inicial_mes
        """)

        resultados = db.session.execute(sql).mappings().all()

        return [
            self.__mapear_mes_referencia(registro)
            for registro in resultados
        ]

    def atualizar(self, mes_referencia: MesReferencia):
        sql = text("""
            UPDATE mes_referencia
            SET
                data_inicial_mes = :data_inicial_mes,
                data_final_mes = :data_final_mes,
                nome_mes = :nome_mes,
                fk_id_agenda = :fk_id_agenda
            WHERE id_mes_referencia = :id_mes_referencia
        """)

        resultado = db.session.execute(sql, {
            "id_mes_referencia": mes_referencia.id_mes_referencia,
            "data_inicial_mes": mes_referencia.data_inicial_mes,
            "data_final_mes": mes_referencia.data_final_mes,
            "nome_mes": mes_referencia.nome_mes,
            "fk_id_agenda": mes_referencia.agenda.id
        })

        db.session.commit()

        return resultado.rowcount > 0

    def excluir(self, id_mes_referencia: int):
        sql = text("""
            DELETE FROM mes_referencia
            WHERE id_mes_referencia = :id_mes_referencia
        """)

        resultado = db.session.execute(
            sql,
            {"id_mes_referencia": id_mes_referencia}
        )

        db.session.commit()

        return resultado.rowcount > 0

    def __mapear_mes_referencia(self, registro):
        agenda = self.__agendaDao.buscar_por_id(
            registro["fk_id_agenda"]
        )

        return MesReferencia(
            id_mes_referencia=registro["id_mes_referencia"],
            data_inicial_mes=registro["data_inicial_mes"],
            data_final_mes=registro["data_final_mes"],
            nome_mes=registro["nome_mes"],
            agenda=agenda
        )
