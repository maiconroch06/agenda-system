
from sqlalchemy import text
from database import db
from models import Agendamento, Barbeiro, Servico
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
                -- Dados do agendamento
                a.id_agendamento,
                a.data_agendamento,
                a.hora_inicio,
                a.hora_fim,
                a.status_agendamento,
                a.data_atualizacao,
                a.fk_id_servico,
                a.fk_id_barbeiro,
                a.fk_id_cliente,
                a.motivo_cancelamento,

                -- Dados do barbeiro
                b.id_barbeiro,
                u.nome_completo,
                u.email,
                u.telefone,
                u.cpf,
                u.data_atualizacao,
                b.bio,

                -- Dados do serviço
                s.id_servico,
                s.descricao_servico,
                s.valor,
                s.duracao

            FROM agendamento a

            INNER JOIN barbeiro b
                ON a.fk_id_barbeiro = b.id_barbeiro

            INNER JOIN usuario u
                ON b.id_barbeiro = u.id_usuario

            INNER JOIN servico s
                ON a.fk_id_servico = s.id_servico

            WHERE a.fk_id_cliente = :fk_id_cliente

            ORDER BY a.data_agendamento ASC, a.hora_inicio ASC
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
                motivo_cancelamento = :motivo_cancelamento,
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
            "motivo_cancelamento": agendamento.motivo_cancelamento,
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

        barbeiro = Barbeiro(
            id_usuario=registro["id_barbeiro"],
            nome_completo=registro["nome_completo"],
            email=registro["email"],
            telefone=registro["telefone"],
            bio=registro["bio"],
            cpf=registro["cpf"],
            data_atualizacao=registro["data_atualizacao"]
        )

        servico = Servico(
            id_servico=registro["id_servico"],
            descricao_servico=registro["descricao_servico"],
            valor=registro["valor"],
            duracao=registro["duracao"]
        )

        agendamento = Agendamento(
            id_agendamento=registro["id_agendamento"],
            data_agendamento=registro["data_agendamento"],
            hora_inicio=(datetime.min + registro["hora_inicio"]).time(),
            hora_fim=(datetime.min + registro["hora_fim"]).time(),
            motivo_cancelamento=registro["motivo_cancelamento"],
            status_agendamento=registro["status_agendamento"],
            data_atualizacao=registro["data_atualizacao"],
            barbeiro = barbeiro,
            servico = servico,
            cliente = None
        )

        return agendamento
