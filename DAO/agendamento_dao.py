
from sqlalchemy import text
from database import db
from models import Agendamento
from datetime import date, datetime


class AgendamentoDAO:

    @staticmethod
    def salvar(agendamento: Agendamento):

        sql = text("""
            INSERT INTO agendamento (
                data_agendamento,
                hora_inicio,
                hora_fim,
                status_agendamento,
                data_atualizacao,
                fk_id_servico,
                fk_id_barbeiro,
                fk_id_cliente
            ) VALUES (
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

        parametros = {
            "data_agendamento": agendamento.data_agendamento,
            "hora_inicio": agendamento.hora_inicio,
            "hora_fim": agendamento.hora_fim,
            "status_agendamento": agendamento.status_agendamento,
            "data_atualizacao": agendamento.data_atualizacao,
            "fk_id_servico": agendamento.servico.id_servico,
            "fk_id_barbeiro": agendamento.barbeiro.id_usuario,
            "fk_id_cliente": agendamento.cliente.id_usuario
        }


        resultado = db.session.execute(sql, parametros)

        db.session.commit()

        return resultado.lastrowid

    # Gerenciar conflito
    @staticmethod
    def verificar_conflito(
        id_barbeiro: int,
        data_agendamento,
        hora_inicio,
        hora_fim
    ):
        sql = text("""
            SELECT id_agendamento
            FROM agendamento
            WHERE fk_id_barbeiro = :id_barbeiro
            AND data_agendamento = :data_agendamento
            AND hora_inicio < :hora_fim
            AND hora_fim > :hora_inicio
            LIMIT 1
        """)

        resultado = db.session.execute(sql, {
            "id_barbeiro": id_barbeiro,
            "data_agendamento": data_agendamento,
            "hora_inicio": hora_inicio,
            "hora_fim": hora_fim
        }).first()

        return resultado is not None

    @staticmethod
    def buscar_por_id(id_agendamento: int):
        sql = text("""
            SELECT
                id_agendamento,
                data_agendamento,
                hora_inicio,
                hora_fim,
                status_agendamento,
                data_atualizacao,
                fk_id_servico,
                fk_id_barbeiro,
                fk_id_cliente
            FROM agendamento
            WHERE id_agendamento = :id_agendamento
        """)

        resultado = db.session.execute(
            sql,
            {"id_agendamento": id_agendamento}
        ).mappings().first()

        if resultado is None:
            return None

        return AgendamentoDAO._mapear_agendamento(resultado)

    @staticmethod
    def consultar_todos_os_agendamento_do_cliente(id_cliente):
        sql = text("""
            SELECT
                id_agendamento,
                data_agendamento,
                hora_inicio,
                hora_fim,
                status_agendamento,
                data_atualizacao,
                fk_id_servico,
                fk_id_barbeiro,
                fk_id_cliente
            FROM agendamento
            WHERE 
             fk_id_cliente=:fk_id_cliente
            ORDER BY data_agendamento, hora_inicio ASC
        """)

        resultados = db.session.execute(
                    sql,
                    {
                     "fk_id_cliente": id_cliente
                     }              
                    ).mappings().all()

        return [
            AgendamentoDAO._mapear_agendamento(registro)
            for registro in resultados
        ]

    @staticmethod
    def listar_por_cliente(id_cliente: int):
        sql = text("""
            SELECT
                id_agendamento,
                data_agendamento,
                hora_inicio,
                hora_fim,
                status_agendamento,
                data_atualizacao,
                fk_id_servico,
                fk_id_barbeiro,
                fk_id_cliente
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
            SELECT
                id_agendamento,
                data_agendamento,
                hora_inicio,
                hora_fim,
                status_agendamento,
                data_atualizacao,
                fk_id_servico,
                fk_id_barbeiro,
                fk_id_cliente
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
            WHERE id_agendamento = :id_agendamento
        """)

        resultado = db.session.execute(sql, {
            "id_agendamento": agendamento.id_agendamento,
            "data_agendamento": agendamento.data_agendamento,
            "hora_inicio": agendamento.hora_inicio,
            "hora_fim": agendamento.hora_fim,
            "status_agendamento": agendamento.status_agendamento,
            "data_atualizacao": agendamento.data_atualizacao,
            "fk_id_servico": agendamento.fk_id_servico,
            "fk_id_barbeiro": agendamento.fk_id_barbeiro,
            "fk_id_cliente": agendamento.fk_id_cliente
        })

        db.session.commit()

        return resultado.rowcount > 0

    @staticmethod
    def excluir(id_agendamento: int):
        sql = text("""
            DELETE FROM agendamento
            WHERE id_agendamento = :id_agendamento
        """)

        resultado = db.session.execute(
            sql,
            {"id_agendamento": id_agendamento}
        )

        db.session.commit()

        return resultado.rowcount > 0

    @staticmethod
    def _mapear_agendamento(registro):
        return Agendamento(
            id_agendamento=registro["id_agendamento"],
            data_agendamento=registro["data_agendamento"],
            hora_inicio=(datetime.min + registro["hora_inicio"]).time(),
            hora_fim=(datetime.min +registro["hora_fim"]).time(),
            status_agendamento=registro["status_agendamento"],
            data_atualizacao=registro["data_atualizacao"],
        )
