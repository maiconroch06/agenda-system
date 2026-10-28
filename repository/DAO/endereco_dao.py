
from sqlalchemy import text
from database import db
from models.endereco import Endereco


class EnderecoDAO:

    @staticmethod
    def salvar(endereco: Endereco):
        sql = text("""
            INSERT INTO enderecos (
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

        # O ID é gerado pelo AUTO_INCREMENT da tabela.
        endereco.id = resultado.lastrowid

        db.session.flush()

        return endereco.id

    @staticmethod
    def buscar_por_id(id_endereco: int):
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
            FROM enderecos
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
    def listar_todos():
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
            FROM enderecos
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
            FROM enderecos
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
            UPDATE enderecos
            SET
                cep = :cep,
                cidade = :cidade,
                estados_br_sigla = :estados_br_sigla,
                logradouro = :logradouro,
                numero = :numero,
                bairro = :bairro,
                sequencia = :sequencia,
                complemento = :complemento
            WHERE id = :id
        """)

        resultado = db.session.execute(sql, {
            "id": endereco.id,
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

        return resultado.rowcount > 0

    @staticmethod
    def excluir(id_endereco: int):
        sql = text("""
            DELETE FROM enderecos
            WHERE id = :id
        """)

        resultado = db.session.execute(
            sql,
            {"id": id_endereco}
        )

        db.session.flush()

        return resultado.rowcount > 0

    @staticmethod
    def _mapear(registro):
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
