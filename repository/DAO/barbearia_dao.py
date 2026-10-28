
from sqlalchemy import text
from database import db
from models.barbearia import Barbearia


class BarbeariaDAO:

    @staticmethod
    def salvar(barbearia: Barbearia):
        sql = text("""
            INSERT INTO barbearia (
                cnpj,
                nome_barbearia,
                telefone,
                email_empresa,
                logo_barbearia,
                data_cadastro,
                fk_id_endereco,
                fk_id_agenda
            ) VALUES (
                :cnpj,
                :nome_barbearia,
                :telefone,
                :email_empresa,
                :logo_barbearia,
                :data_cadastro,
                :fk_id_endereco,
                :fk_id_agenda
            )
        """)

        db.session.execute(sql, {
            "cnpj": barbearia.cnpj,
            "nome_barbearia": barbearia.nome_barbearia,
            "telefone": barbearia.telefone,
            "email_empresa": barbearia.email_empresa,
            "logo_barbearia": barbearia.logo_barbearia,
            "data_cadastro": barbearia.data_cadastro,
            "fk_id_endereco": barbearia.fk_id_endereco,
            "fk_id_agenda": barbearia.fk_id_agenda
        })

        db.session.flush()
        return barbearia.cnpj

    @staticmethod
    def buscar_por_cnpj(cnpj: str):
        sql = text("""
            SELECT *
            FROM barbearia
            WHERE cnpj = :cnpj
        """)

        registro = db.session.execute(
            sql,
            {"cnpj": cnpj}
        ).mappings().first()

        if registro is None:
            return None

        return BarbeariaDAO._mapear_barbearia(registro)

    @staticmethod
    def listar_todas():
        sql = text("""
            SELECT *
            FROM barbearia
            ORDER BY nome_barbearia
        """)

        registros = db.session.execute(sql).mappings().all()

        return [
            BarbeariaDAO._mapear_barbearia(registro)
            for registro in registros
        ]

    @staticmethod
    def atualizar(barbearia: Barbearia):
        sql = text("""
            UPDATE barbearia
            SET
                nome_barbearia = :nome_barbearia,
                telefone = :telefone,
                email_empresa = :email_empresa,
                logo_barbearia = :logo_barbearia,
                fk_id_endereco = :fk_id_endereco,
                fk_id_agenda = :fk_id_agenda
            WHERE cnpj = :cnpj
        """)

        resultado = db.session.execute(sql, {
            "cnpj": barbearia.cnpj,
            "nome_barbearia": barbearia.nome_barbearia,
            "telefone": barbearia.telefone,
            "email_empresa": barbearia.email_empresa,
            "logo_barbearia": barbearia.logo_barbearia,
            "fk_id_endereco": barbearia.fk_id_endereco,
            "fk_id_agenda": barbearia.fk_id_agenda
        })

        db.session.flush()
        return resultado.rowcount > 0

    @staticmethod
    def excluir(cnpj: str):
        sql = text("""
            DELETE FROM barbearia
            WHERE cnpj = :cnpj
        """)

        resultado = db.session.execute(
            sql,
            {"cnpj": cnpj}
        )

        db.session.flush()
        return resultado.rowcount > 0

    @staticmethod
    def _mapear_barbearia(registro):
        return Barbearia(
            cnpj=registro["cnpj"],
            nome_barbearia=registro["nome_barbearia"],
            telefone=registro["telefone"],
            email_empresa=registro["email_empresa"],
            logo_barbearia=registro["logo_barbearia"],
            data_cadastro=registro["data_cadastro"],
            fk_id_endereco=registro["fk_id_endereco"],
            fk_id_agenda=registro["fk_id_agenda"]
        )
