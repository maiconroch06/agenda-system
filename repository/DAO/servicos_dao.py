
from sqlalchemy import text
from database import db
from models.servicos import Servico


class ServicoDAO:

    @staticmethod
    def salvar(servico: Servico):
        sql = text("""
            INSERT INTO servicos (
                id,
                descricao,
                valor,
                duracao,
                foto_nome,
                status_servico,
                data_cadastro,
                data_atualizacao
            ) VALUES (
                :id,
                :descricao,
                :valor,
                :duracao,
                :foto_nome,
                :status_servico,
                :data_cadastro,
                :data_atualizacao
            )
        """)

        db.session.execute(sql, {
            "id": servico.id,
            "descricao": servico.descricao,
            "valor": servico.valor,
            "duracao": servico.duracao,
            "foto_nome": servico.foto_nome,
            "status_servico": servico.status_servico,
            "data_cadastro": servico.data_cadastro,
            "data_atualizacao": servico.data_atualizacao
        })

        db.session.flush()

        return servico.id

    @staticmethod
    def buscar_por_id(id_servico: int):
        sql = text("""
            SELECT
                id,
                descricao,
                valor,
                duracao,
                foto_nome,
                status_servico,
                data_cadastro,
                data_atualizacao
            FROM servicos
            WHERE id = :id
        """)

        registro = db.session.execute(
            sql,
            {"id": id_servico}
        ).mappings().first()

        if registro is None:
            return None

        return ServicoDAO._mapear(registro)

    @staticmethod
    def listar_todos():
        sql = text("""
            SELECT
                id,
                descricao,
                valor,
                duracao,
                foto_nome,
                status_servico,
                data_cadastro,
                data_atualizacao
            FROM servicos
            ORDER BY descricao
        """)

        registros = db.session.execute(sql).mappings().all()

        return [
            ServicoDAO._mapear(registro)
            for registro in registros
        ]

    @staticmethod
    def listar_ativos():
        sql = text("""
            SELECT
                id,
                descricao,
                valor,
                duracao,
                foto_nome,
                status_servico,
                data_cadastro,
                data_atualizacao
            FROM servicos
            WHERE status_servico = :status
            ORDER BY descricao
        """)

        registros = db.session.execute(
            sql,
            {"status": True}
        ).mappings().all()

        return [
            ServicoDAO._mapear(registro)
            for registro in registros
        ]

    @staticmethod
    def atualizar(servico: Servico):
        sql = text("""
            UPDATE servicos
            SET
                descricao = :descricao,
                valor = :valor,
                duracao = :duracao,
                foto_nome = :foto_nome,
                status_servico = :status_servico,
                data_atualizacao = :data_atualizacao
            WHERE id = :id
        """)

        resultado = db.session.execute(sql, {
            "id": servico.id,
            "descricao": servico.descricao,
            "valor": servico.valor,
            "duracao": servico.duracao,
            "foto_nome": servico.foto_nome,
            "status_servico": servico.status_servico,
            "data_atualizacao": servico.data_atualizacao
        })

        db.session.flush()

        return resultado.rowcount > 0

    @staticmethod
    def ativar(id_servico: int, data_atualizacao):
        sql = text("""
            UPDATE servicos
            SET
                status_servico = :status,
                data_atualizacao = :data_atualizacao
            WHERE id = :id
        """)

        resultado = db.session.execute(sql, {
            "id": id_servico,
            "status": True,
            "data_atualizacao": data_atualizacao
        })

        db.session.flush()

        return resultado.rowcount > 0

    @staticmethod
    def desativar(id_servico: int, data_atualizacao):
        sql = text("""
            UPDATE servicos
            SET
                status_servico = :status,
                data_atualizacao = :data_atualizacao
            WHERE id = :id
        """)

        resultado = db.session.execute(sql, {
            "id": id_servico,
            "status": False,
            "data_atualizacao": data_atualizacao
        })

        db.session.flush()

        return resultado.rowcount > 0

    @staticmethod
    def excluir(id_servico: int):
        sql = text("""
            DELETE FROM servicos
            WHERE id = :id
        """)

        resultado = db.session.execute(
            sql,
            {"id": id_servico}
        )

        db.session.flush()

        return resultado.rowcount > 0

    @staticmethod
    def _mapear(registro):
        return Servico(
            id=registro["id"],
            descricao=registro["descricao"],
            valor=registro["valor"],
            duracao=registro["duracao"],
            foto_nome=registro["foto_nome"],
            status_servico=bool(registro["status_servico"]),
            data_cadastro=registro["data_cadastro"],
            data_atualizacao=registro["data_atualizacao"]
        )
