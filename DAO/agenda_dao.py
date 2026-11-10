
from sqlalchemy import text
from database import db
from models import Agenda


class AgendaDAO:

    def cadastrar(self, agenda: Agenda):
        sql = text("""
            INSERT INTO agendas (
                horario_abertura,
                horario_fechamento,
                horario_inicio_intrajornada,
                horario_fim_intrajornada
            ) VALUES (
                :horario_abertura,
                :horario_fechamento,
                :horario_inicio_intrajornada,
                :horario_fim_intrajornada
            )
        """)

        resultado = db.session.execute(sql, {
            "horario_abertura": agenda.horario_abertura,
            "horario_fechamento": agenda.horario_fechamento,
            "horario_inicio_intrajornada": agenda.horario_inicio_intrajornada,
            "horario_fim_intrajornada": agenda.horario_fim_intrajornada
        })

        db.session.flush()

        # Retorna o ID gerado pelo banco
        return resultado.lastrowid

    def buscar_por_id(self, id_agenda: int):
        sql = text("""
            SELECT
                id,
                horario_abertura,
                horario_fechamento,
                horario_inicio_intrajornada,
                horario_fim_intrajornada
            FROM agendas
            WHERE id = :id
        """)

        registro = db.session.execute(
            sql,
            {"id": id_agenda}
        ).mappings().first()

        if registro is None:
            return None

        return self._mapear_agenda(registro)

    def consultar_todos(self):
        sql = text("""
            SELECT
                id,
                horario_abertura,
                horario_fechamento,
                horario_inicio_intrajornada,
                horario_fim_intrajornada
            FROM agendas
            ORDER BY horario_abertura
        """)

        registros = db.session.execute(sql).mappings().all()

        return [
            self._mapear_agenda(registro)
            for registro in registros
        ]

    def atualizar(self, agenda: Agenda):
        sql = text("""
            UPDATE agendas
            SET
                horario_abertura = :horario_abertura,
                horario_fechamento = :horario_fechamento,
                horario_inicio_intrajornada = :horario_inicio_intrajornada,
                horario_fim_intrajornada = :horario_fim_intrajornada
            WHERE id = :id
        """)

        resultado = db.session.execute(sql, {
            "id": agenda.id,
            "horario_abertura": agenda.horario_abertura,
            "horario_fechamento": agenda.horario_fechamento,
            "horario_inicio_intrajornada": agenda.horario_inicio_intrajornada,
            "horario_fim_intrajornada": agenda.horario_fim_intrajornada
        })

        db.session.flush()

        return resultado.rowcount > 0

    def excluir(self, id_agenda: int):
        sql = text("""
            DELETE FROM agendas
            WHERE id = :id
        """)

        resultado = db.session.execute(
            sql,
            {"id": id_agenda}
        )

        db.session.flush()

        return resultado.rowcount > 0

    @staticmethod
    def _mapear_agenda(registro):
        return Agenda(
            id=registro["id"],
            horario_abertura=registro["horario_abertura"],
            horario_fechamento=registro["horario_fechamento"],
            horario_inicio_intrajornada=registro["horario_inicio_intrajornada"],
            horario_fim_intrajornada=registro["horario_fim_intrajornada"]
        )
