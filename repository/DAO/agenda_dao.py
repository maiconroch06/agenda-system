
from sqlalchemy import text
from database import db
from models.agenda import Agenda


class AgendaDAO:

    @staticmethod
    def salvar(agenda: Agenda):
        sql = text("""
            INSERT INTO agendas (
                descricao,
                data_criacao,
                ativo
            ) VALUES (
                :descricao,
                :data_criacao,
                :ativo
            )
        """)

        resultado = db.session.execute(sql, {
            "descricao": agenda.descricao,
            "data_criacao": agenda.data_criacao,
            "ativo": agenda.ativo
        })

        agenda.id = resultado.lastrowid

        db.session.flush()

        return agenda.id

    @staticmethod
    def buscar_por_id(id_agenda: int):
        sql = text("""
            SELECT
                id,
                descricao,
                data_criacao,
                ativo
            FROM agendas
            WHERE id = :id
        """)

        registro = db.session.execute(
            sql,
            {"id": id_agenda}
        ).mappings().first()

        if registro is None:
            return None

        return AgendaDAO._mapear(registro)

    @staticmethod
    def listar_todos():
        sql = text("""
            SELECT
                id,
                descricao,
                data_criacao,
                ativo
            FROM agendas
            ORDER BY descricao
        """)

        registros = db.session.execute(sql).mappings().all()

        return [
            AgendaDAO._mapear(registro)
            for registro in registros
        ]

    @staticmethod
    def listar_ativas():
        sql = text("""
            SELECT
                id,
                descricao,
                data_criacao,
                ativo
            FROM agendas
            WHERE ativo = :ativo
            ORDER BY descricao
        """)

        registros = db.session.execute(
            sql,
            {"ativo": True}
        ).mappings().all()

        return [
            AgendaDAO._mapear(registro)
            for registro in registros
        ]

    @staticmethod
    def atualizar(agenda: Agenda):
        sql = text("""
            UPDATE agendas
            SET
                descricao = :descricao,
                ativo = :ativo
            WHERE id = :id
        """)

        resultado = db.session.execute(sql, {
            "id": agenda.id,
            "descricao": agenda.descricao,
            "ativo": agenda.ativo
        })

        db.session.flush()

        return resultado.rowcount > 0

    @staticmethod
    def excluir(id_agenda: int):
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
    def _mapear(registro):
        return Agenda(
            id=registro["id"],
            descricao=registro["descricao"],
            data_criacao=registro["data_criacao"],
            ativo=bool(registro["ativo"])
        )
