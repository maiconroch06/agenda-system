
import json

from sqlalchemy import text
from database import db
from models import Agenda


class AgendaDAO:

    def cadastrar(self, agenda: Agenda):
        sql = text("""
            INSERT INTO agenda (
                horario_abertura,
                horario_fechamento,
                horario_inicio_intrajornada,
                horario_fim_intrajornada,
                dias_fechados
            ) VALUES (
                :horario_abertura,
                :horario_fechamento,
                :horario_inicio_intrajornada,
                :horario_fim_intrajornada,
                :dias_fechados
            )
        """)

        resultado = db.session.execute(sql, {
            "horario_abertura": agenda.horario_abertura,
            "horario_fechamento": agenda.horario_fechamento,
            "horario_inicio_intrajornada": agenda.horario_inicio_intrajornada,
            "horario_fim_intrajornada": agenda.horario_fim_intrajornada,
            "dias_fechados": json.dumps(agenda.dias_fechados)
        })

        db.session.flush()

        return resultado.lastrowid

    def buscar_por_id(self, id_agenda: int):
        sql = text("""
            SELECT
                id_agenda,
                horario_abertura,
                horario_fechamento,
                horario_inicio_intrajornada,
                horario_fim_intrajornada,
                dias_fechados
            FROM agenda
            WHERE id_agenda = :id_agenda
        """)

        registro = db.session.execute(
            sql,
            {"id_agenda": id_agenda}
        ).mappings().first()

        if registro is None:
            return None

        return self._mapear_agenda(registro)

    def consultar_todos(self):
        sql = text("""
            SELECT
                id_agenda,
                horario_abertura,
                horario_fechamento,
                horario_inicio_intrajornada,
                horario_fim_intrajornada,
                dias_fechados
            FROM agenda
            ORDER BY horario_abertura
        """)

        registros = db.session.execute(sql).mappings().all()

        return [
            self._mapear_agenda(registro)
            for registro in registros
        ]

    def atualizar(self, agenda: Agenda):
        sql = text("""
            UPDATE agenda
            SET
                horario_abertura = :horario_abertura,
                horario_fechamento = :horario_fechamento,
                horario_inicio_intrajornada = :horario_inicio_intrajornada,
                horario_fim_intrajornada = :horario_fim_intrajornada,
                dias_fechados = :dias_fechados
            WHERE id_agenda = :id_agenda
        """)

        resultado = db.session.execute(sql, {
            "id_agenda": agenda.id_agenda,
            "horario_abertura": agenda.horario_abertura,
            "horario_fechamento": agenda.horario_fechamento,
            "horario_inicio_intrajornada": agenda.horario_inicio_intrajornada,
            "horario_fim_intrajornada": agenda.horario_fim_intrajornada,
            "dias_fechados": json.dumps(agenda.dias_fechados)
        })

        db.session.flush()

        return resultado.rowcount > 0

    def excluir(self, id_agenda: int):
        sql = text("""
            DELETE FROM agenda
            WHERE id_agenda = :id_agenda
        """)

        resultado = db.session.execute(
            sql,
            {"id_agenda": id_agenda}
        )

        db.session.flush()

        return resultado.rowcount > 0

    @staticmethod
    def _mapear_agenda(registro):
        dias_fechados = registro["dias_fechados"]

        # Converte o JSON retornado pelo banco em uma lista Python.
        if isinstance(dias_fechados, str):
            dias_fechados = json.loads(dias_fechados)

        return Agenda(
            id_agenda=registro["id_agenda"],
            horario_abertura=registro["horario_abertura"],
            horario_fechamento=registro["horario_fechamento"],
            horario_inicio_intrajornada=registro["horario_inicio_intrajornada"],
            horario_fim_intrajornada=registro["horario_fim_intrajornada"],
            dias_fechados=dias_fechados or []
        )