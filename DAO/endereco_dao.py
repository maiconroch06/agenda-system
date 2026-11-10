
from sqlalchemy import text
from database import db
from models import Endereco


class EnderecoDAO:

    @staticmethod
    def salvar( endereco: Endereco):
        sql = text("""
            INSERT INTO endereco (
                cep,
                cidade,
                estados_br_sigla,
                logradouro,
                numero,
                bairro,
                sequencia,
                complemento
            ) VALUES (
                :cep,
                :cidade,
                :estados_br_sigla,
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
            "estados_br_sigla": endereco.estados_br_sigla,
            "logradouro": endereco.logradouro,
            "numero": endereco.numero,
            "bairro": endereco.bairro,
            "sequencia": endereco.sequencia,
            "complemento": endereco.complemento
        })
        db.session.flush()

        # O ID é gerado pelo AUTO_INCREMENT da tabela.
        return resultado.lastrowid

    @staticmethod
    def buscar_por_id( id_endereco: int):
        sql = text("""
            SELECT
                id,
                cep,
                cidade,
                estados_br_sigla,
                logradouro,
                numero,
                bairro,
                sequencia,
                complemento
            FROM endereco
            WHERE id = :id
        """)

        registro = db.session.execute(
            sql,
            {"id": id_endereco}
        ).mappings().first()

        if registro is None:
            return None

        return EnderecoDAO._mapear(registro)

    @staticmethod
    def listar_todos(cls):
        sql = text("""
            SELECT
                id,
                cep,
                cidade,
                estados_br_sigla,
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
                id,
                cep,
                cidade,
                estados_br_sigla,
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
    def atualizar( endereco: Endereco):
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
            WHERE id_endereco = :id
        """)

        resultado = db.session.execute(sql, {
            "id": endereco.id_endereco,
            "cep": endereco.cep,
            "cidade": endereco.cidade,
            "uf": endereco.uf,
            "logradouro": endereco.logradouro,
            "numero": endereco.numero,
            "bairro": endereco.bairro,
            "sequencia": endereco.sequencia,
            "complemento": endereco.complemento
        })

        print("o valor é "+ str(endereco.sequencia))
        db.session.commit()

        return resultado.rowcount > 0

    @staticmethod
    def excluir( id_endereco: int):
        sql = text("""
            DELETE FROM endereco
            WHERE id = :id
        """)

        resultado = db.session.execute(
            sql,
            {"id": id_endereco}
        )

        db.session.flush()

        return resultado.rowcount > 0

    @staticmethod
    def _mapear( registro):
        return Endereco(
            id=registro["id"],
            cep=registro["cep"],
            cidade=registro["cidade"],
            estados_br_sigla=registro["estados_br_sigla"],
            logradouro=registro["logradouro"],
            numero=registro["numero"],
            bairro=registro["bairro"],
            sequencia=registro["sequencia"],
            complemento=registro["complemento"]
        )
