
from sqlalchemy import text
from database import db
from models.agendamento import Agendamento
from datetime import date, time, datetime


class AgendamentoDAO:

    @staticmethod
    def salvar(agendamento: Agendamento):
        sql = text("""
            INSERT INTO agendamento (
                id,
                data_agendamento,
                hora_inicio,
                hora_fim,
                status_agendamento,
                data_atualizacao,
                fk_id_servico,
                fk_id_barbeiro,
                fk_id_cliente
            ) VALUES (
                :id,
                :data_agendamento,
                :hora_inicio,
                :hora_fim,
                :status_agendamento,
                :data_atualizacao,
                :fk_id_servico,
                :fk_id_barbeiro,
                :fk_id_cliente
            )
        """)

        db.session.execute(sql, {
            "id": agendamento.id,
            "data_agendamento": agendamento.data_agendamento,
            "hora_inicio": agendamento.hora_inicio,
            "hora_fim": agendamento.hora_fim,
            "status_agendamento": agendamento.status_agendamento,
            "data_atualizacao": agendamento.data_atualizacao,
            "fk_id_servico": agendamento.fk_id_servico,
            "fk_id_barbeiro": agendamento.fk_id_barbeiro,
            "fk_id_cliente": agendamento.fk_id_cliente
        })

        db.session.flush()
        return agendamento.id

    @staticmethod
    def buscar_por_id(id_agendamento: int):
        sql = text("""
            SELECT *
            FROM agendamento
            WHERE id = :id
        """)

        resultado = db.session.execute(
            sql,
            {"id": id_agendamento}
        ).mappings().first()

        if resultado is None:
            return None

        return AgendamentoDAO._mapear_agendamento(resultado)

    @staticmethod
    def listar_todos():
        sql = text("""
            SELECT *
            FROM agendamento
            ORDER BY data_agendamento, hora_inicio
        """)

        resultados = db.session.execute(sql).mappings().all()

        return [
            AgendamentoDAO._mapear_agendamento(registro)
            for registro in resultados
        ]

    @staticmethod
    def listar_por_cliente(id_cliente: int):
        sql = text("""
            SELECT *
            FROM agendamento
            WHERE fk_id_cliente = :id_cliente
            ORDER BY data_agendamento, hora_inicio
        """)

        resultados = db.session.execute(
            sql,
            {"id_cliente": id_cliente}
        ).mappings().all()

        return [
            AgendamentoDAO._mapear_agendamento(registro)
            for registro in resultados
        ]

    @staticmethod
    def listar_por_barbeiro(id_barbeiro: int, data: date = None):
        sql = """
            SELECT *
            FROM agendamento
            WHERE fk_id_barbeiro = :id_barbeiro
        """

        parametros = {
            "id_barbeiro": id_barbeiro
        }

        if data is not None:
            sql += " AND data_agendamento = :data"
            parametros["data"] = data

        sql += " ORDER BY data_agendamento, hora_inicio"

        resultados = db.session.execute(
            text(sql),
            parametros
        ).mappings().all()

        return [
            AgendamentoDAO._mapear_agendamento(registro)
            for registro in resultados
        ]

    @staticmethod
    def atualizar(agendamento: Agendamento):
        sql = text("""
            UPDATE agendamento
            SET
                data_agendamento = :data_agendamento,
                hora_inicio = :hora_inicio,
                hora_fim = :hora_fim,
                status_agendamento = :status_agendamento,
                data_atualizacao = :data_atualizacao,
                fk_id_servico = :fk_id_servico,
                fk_id_barbeiro = :fk_id_barbeiro,
                fk_id_cliente = :fk_id_cliente
            WHERE id = :id
        """)

        resultado = db.session.execute(sql, {
            "id": agendamento.id,
            "data_agendamento": agendamento.data_agendamento,
            "hora_inicio": agendamento.hora_inicio,
            "hora_fim": agendamento.hora_fim,
            "status_agendamento": agendamento.status_agendamento,
            "data_atualizacao": agendamento.data_atualizacao,
            "fk_id_servico": agendamento.fk_id_servico,
            "fk_id_barbeiro": agendamento.fk_id_barbeiro,
            "fk_id_cliente": agendamento.fk_id_cliente
        })

        db.session.flush()
        return resultado.rowcount > 0

    @staticmethod
    def excluir(id_agendamento: int):
        sql = text("""
            DELETE FROM agendamento
            WHERE id = :id
        """)

        resultado = db.session.execute(
            sql,
            {"id": id_agendamento}
        )

        db.session.flush()
        return resultado.rowcount > 0

    @staticmethod
    def _mapear_agendamento(registro):
        return Agendamento(
            id=registro["id"],
            data_agendamento=registro["data_agendamento"],
            hora_inicio=registro["hora_inicio"],
            hora_fim=registro["hora_fim"],
            status_agendamento=bool(registro["status_agendamento"]),
            data_atualizacao=registro["data_atualizacao"],
            fk_id_servico=registro["fk_id_servico"],
            fk_id_barbeiro=registro["fk_id_barbeiro"],
            fk_id_cliente=registro["fk_id_cliente"]
        )
