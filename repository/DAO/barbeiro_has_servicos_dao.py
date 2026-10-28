
from sqlalchemy import text
from database import db
from models.barbeiro_has_servicos import BarbeiroHasServicos
from datetime import datetime


class BarbeiroHasServicosDAO:

    @staticmethod
    def salvar(relacionamento: BarbeiroHasServicos):
        sql = text("""
            INSERT INTO barbeiro_has_Servicos (
                id_servico,
                id_barbeiro,
                data_cadastro
            ) VALUES (
                :id_servico,
                :id_barbeiro,
                :data_cadastro
            )
        """)

        db.session.execute(sql, {
            "id_servico": relacionamento.id_servico,
            "id_barbeiro": relacionamento.id_barbeiro,
            "data_cadastro": relacionamento.data_cadastro
        })

        db.session.flush()

        return relacionamento

    @staticmethod
    def buscar_por_ids(
        id_servico: int,
        id_barbeiro: int
    ):
        sql = text("""
            SELECT
                id_servico,
                id_barbeiro,
                data_cadastro
            FROM barbeiro_has_Servicos
            WHERE id_servico = :id_servico
              AND id_barbeiro = :id_barbeiro
        """)

        registro = db.session.execute(sql, {
            "id_servico": id_servico,
            "id_barbeiro": id_barbeiro
        }).mappings().first()

        if registro is None:
            return None

        return BarbeiroHasServicosDAO._mapear(registro)

    @staticmethod
    def listar_todos():
        sql = text("""
            SELECT
                id_servico,
                id_barbeiro,
                data_cadastro
            FROM barbeiro_has_Servicos
            ORDER BY id_barbeiro, id_servico
        """)

        registros = db.session.execute(sql).mappings().all()

        return [
            BarbeiroHasServicosDAO._mapear(registro)
            for registro in registros
        ]

    @staticmethod
    def listar_por_barbeiro(id_barbeiro: int):
        sql = text("""
            SELECT
                id_servico,
                id_barbeiro,
                data_cadastro
            FROM barbeiro_has_Servicos
            WHERE id_barbeiro = :id_barbeiro
            ORDER BY id_servico
        """)

        registros = db.session.execute(
            sql,
            {"id_barbeiro": id_barbeiro}
        ).mappings().all()

        return [
            BarbeiroHasServicosDAO._mapear(registro)
            for registro in registros
        ]

    @staticmethod
    def listar_por_servico(id_servico: int):
        sql = text("""
            SELECT
                id_servico,
                id_barbeiro,
                data_cadastro
            FROM barbeiro_has_Servicos
            WHERE id_servico = :id_servico
            ORDER BY id_barbeiro
        """)

        registros = db.session.execute(
            sql,
            {"id_servico": id_servico}
        ).mappings().all()

        return [
            BarbeiroHasServicosDAO._mapear(registro)
            for registro in registros
        ]

    @staticmethod
    def atualizar_data_cadastro(
        id_servico: int,
        id_barbeiro: int,
        data_cadastro: datetime
    ):
        sql = text("""
            UPDATE barbeiro_has_Servicos
            SET data_cadastro = :data_cadastro
            WHERE id_servico = :id_servico
              AND id_barbeiro = :id_barbeiro
        """)

        resultado = db.session.execute(sql, {
            "id_servico": id_servico,
            "id_barbeiro": id_barbeiro,
            "data_cadastro": data_cadastro
        })

        db.session.flush()

        return resultado.rowcount > 0

    @staticmethod
    def excluir(
        id_servico: int,
        id_barbeiro: int
    ):
        sql = text("""
            DELETE FROM barbeiro_has_Servicos
            WHERE id_servico = :id_servico
              AND id_barbeiro = :id_barbeiro
        """)

        resultado = db.session.execute(sql, {
            "id_servico": id_servico,
            "id_barbeiro": id_barbeiro
        })

        db.session.flush()

        return resultado.rowcount > 0

    @staticmethod
    def _mapear(registro):
        return BarbeiroHasServicos(
            id_servico=registro["id_servico"],
            id_barbeiro=registro["id_barbeiro"],
            data_cadastro=registro["data_cadastro"]
        )
