
from sqlalchemy import text
from database import db
from models import Agenda


class AgendaDAO:

    
    def cadastrar_agenda_dao(self, agenda: Agenda):
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

        db.session.flush()

        return resultado.lastrowid

    
    def buscar_por_id(self, id_agenda: int):
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

    
    def listar_todos(self, ):
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

    
    def listar_ativas(self, ):
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

    
    def atualizar(self, agenda: Agenda):
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

    
    def _mapear(self, registro):
        return Agenda(
            id=registro["id"],
            descricao=registro["descricao"],
            data_criacao=registro["data_criacao"],
            ativo=bool(registro["ativo"])
        )
