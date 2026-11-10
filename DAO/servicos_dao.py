
from sqlalchemy import text
from database import db
from models import Servico


class ServicoDAO:

    def cadastrar_servico(self, servico: Servico):
        sql = text("""
            INSERT INTO servico (
                descricao_servico,
                valor,
                duracao,
                foto_nome_servico,
                status_servico,
                data_cadastro,
                data_atualizacao
            ) VALUES (
                :descricao_servico,
                :valor,
                :duracao,
                :foto_nome_servico,
                :status_servico,
                :data_cadastro,
                :data_atualizacao
            )
        """)

        resultado = db.session.execute(sql, {
            "descricao_servico": servico.descricao_servico,
            "valor": servico.valor,
            "duracao": servico.duracao,
            "foto_nome_servico": servico.foto_nome_servico,
            "status_servico": servico.status_servico,
            "data_cadastro": servico.data_cadastro,
            "data_atualizacao": servico.data_atualizacao
        })

        db.session.flush()

        return resultado.lastrowid

    def consultar_servico_id(self, id_servico: int):
        sql = text("""
            SELECT
                id_servico,
                descricao_servico,
                valor,
                duracao,
                foto_nome_servico,
                status_servico,
                data_cadastro,
                data_atualizacao
            FROM servico
            WHERE id_servico = :id_servico
        """)

        registro = db.session.execute(
            sql,
            {"id_servico": id_servico}
        ).mappings().first()

        return dict(registro) if registro else None

    def consultar_todos_os_servicos(self):
        sql = text("""
            SELECT
                id_servico,
                descricao_servico,
                valor,
                duracao,
                foto_nome_servico,
                status_servico,
                data_cadastro,
                data_atualizacao
            FROM servico
            ORDER BY descricao_servico
        """)

        registros = db.session.execute(sql).mappings().all()

        return [dict(registro) for registro in registros]

    def consultar_todos_os_servicos_resumo(self):
        sql = text("""
            SELECT
                id_servico,
                descricao_servico,
                valor,
                duracao,
                foto_nome_servico
            FROM servico
            WHERE status_servico = 1
            ORDER BY descricao_servico
        """)

        registros = db.session.execute(sql).mappings().all()

        return [dict(registro) for registro in registros]

    def consultar_servicos_status(self, status_servicos: bool):
        sql = text("""
            SELECT
                id_servico,
                descricao_servico,
                valor,
                duracao,
                foto_nome_servico,
                status_servico,
                data_cadastro,
                data_atualizacao
            FROM servico
            WHERE status_servico = :status
            ORDER BY descricao_servico
        """)

        registros = db.session.execute(
            sql,
            {"status": status_servicos}
        ).mappings().all()

        return [dict(registro) for registro in registros]

    def atualizar(self, servico: Servico):
        sql = text("""
            UPDATE servico
            SET
                descricao_servico = :descricao_servico,
                valor = :valor,
                duracao = :duracao,
                foto_nome_servico = :foto_nome_servico,
                status_servico = :status_servico,
                data_atualizacao = :data_atualizacao
            WHERE id_servico = :id_servico
        """)

        resultado = db.session.execute(sql, {
            "id_servico": servico.id_servico,
            "descricao_servico": servico.descricao_servico,
            "valor": servico.valor,
            "duracao": servico.duracao,
            "foto_nome_servico": servico.foto_nome_servico,
            "status_servico": servico.status_servico,
            "data_atualizacao": servico.data_atualizacao
        })

        db.session.flush()

        return resultado.rowcount > 0

    def ativar(self, id_servico: int, data_atualizacao):
        sql = text("""
            UPDATE servico
            SET
                status_servico = :status,
                data_atualizacao = :data_atualizacao
            WHERE id_servico = :id_servico
        """)

        resultado = db.session.execute(sql, {
            "id_servico": id_servico,
            "status": True,
            "data_atualizacao": data_atualizacao
        })

        db.session.flush()

        return resultado.rowcount > 0

    def desativar(self, id_servico: int, data_atualizacao):
        sql = text("""
            UPDATE servico
            SET
                status_servico = :status,
                data_atualizacao = :data_atualizacao
            WHERE id_servico = :id_servico
        """)

        resultado = db.session.execute(sql, {
            "id_servico": id_servico,
            "status": False,
            "data_atualizacao": data_atualizacao
        })

        db.session.flush()

        return resultado.rowcount > 0

    def excluir(self, id_servico: int):
        sql = text("""
            DELETE FROM servico
            WHERE id_servico = :id_servico
        """)

        resultado = db.session.execute(
            sql,
            {"id_servico": id_servico}
        )

        db.session.flush()

        return resultado.rowcount > 0
