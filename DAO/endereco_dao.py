
from sqlalchemy import text
from database import db
from models import Endereco


class EnderecoDAO:

    @staticmethod
    def salvar(endereco: Endereco):
        sql = text("""
            INSERT INTO endereco (
                cep,
                cidade,
                uf,
                logradouro,
                numero,
                bairro,
                sequencia,
                complemento
            ) VALUES (
                :cep,
                :cidade,
                :uf,
                :logradouro,
                :numero,
                :bairro,
                :sequencia,
                :complemento
            )
        """)

        resultado = db.session.execute(sql, {
            "cep": endereco.cep,
            "cidade": endereco.cidade,
            "uf": endereco.uf,
            "logradouro": endereco.logradouro,
            "numero": endereco.numero,
            "bairro": endereco.bairro,
            "sequencia": endereco.sequencia,
            "complemento": endereco.complemento
        })

        db.session.flush()

        return resultado.lastrowid

    @staticmethod
    def buscar_por_id(id_endereco: int):
        sql = text("""
            SELECT
                id_endereco,
                cep,
                cidade,
                uf,
                logradouro,
                numero,
                bairro,
                sequencia,
                complemento
            FROM endereco
            WHERE id_endereco = :id_endereco
        """)

        registro = db.session.execute(
            sql,
            {"id_endereco": id_endereco}
        ).mappings().first()

        if registro is None:
            return None

        return EnderecoDAO._mapear(registro)

    @staticmethod
    def listar_todos():
        sql = text("""
            SELECT
                id_endereco,
                cep,
                cidade,
                uf,
                logradouro,
                numero,
                bairro,
                sequencia,
                complemento
            FROM endereco
            ORDER BY cidade, bairro, logradouro
        """)

        registros = db.session.execute(sql).mappings().all()

        return [
            EnderecoDAO._mapear(registro)
            for registro in registros
        ]

    @staticmethod
    def buscar_por_cep(cep: str):
        sql = text("""
            SELECT
                id_endereco,
                cep,
                cidade,
                uf,
                logradouro,
                numero,
                bairro,
                sequencia,
                complemento
            FROM endereco
            WHERE cep = :cep
            ORDER BY cidade, bairro, logradouro
        """)

        registros = db.session.execute(
            sql,
            {"cep": cep}
        ).mappings().all()

        return [
            EnderecoDAO._mapear(registro)
            for registro in registros
        ]

    @staticmethod
    def atualizar(endereco: Endereco):
        sql = text("""
            UPDATE endereco
            SET
                cep = :cep,
                cidade = :cidade,
                uf = :uf,
                logradouro = :logradouro,
                numero = :numero,
                bairro = :bairro,
                sequencia = :sequencia,
                complemento = :complemento
            WHERE id_endereco = :id_endereco
        """)

        resultado = db.session.execute(sql, {
            "id_endereco": endereco.id_endereco,
            "cep": endereco.cep,
            "cidade": endereco.cidade,
            "uf": endereco.uf,
            "logradouro": endereco.logradouro,
            "numero": endereco.numero,
            "bairro": endereco.bairro,
            "sequencia": endereco.sequencia,
            "complemento": endereco.complemento
        })

        db.session.commit()

        return resultado.rowcount > 0

    @staticmethod
    def _mapear(registro):
        return Endereco(
            id_endereco=registro["id_endereco"],
            cep=registro["cep"],
            cidade=registro["cidade"],
            uf=registro["uf"],
            logradouro=registro["logradouro"],
            numero=registro["numero"],
            bairro=registro["bairro"],
            sequencia=registro["sequencia"],
            complemento=registro["complemento"]
        )
