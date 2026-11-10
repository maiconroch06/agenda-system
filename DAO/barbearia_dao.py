
from sqlalchemy import text
from database import db
from models import Barbearia
from DAO.agenda_dao import AgendaDAO
from DAO.endereco_dao import EnderecoDAO


class BarbeariaDAO:

    def __init__(self):
        self.__agendaDao = AgendaDAO()
        self.__enderecoDao = EnderecoDAO()

    def cadastrar(self, barbearia: Barbearia):
        sql = text("""
            INSERT INTO barbearia (
                cnpj,
                nome_barbearia,
                telefone,
                email_empresa,
                logo_barbearia_nome,
                data_cadastro,
                fk_id_endereco,
                agenda_id_agenda
            ) VALUES (
                :cnpj,
                :nome_barbearia,
                :telefone,
                :email_empresa,
                :logo_barbearia_nome,
                :data_cadastro,
                :fk_id_endereco,
                :agenda_id_agenda
            )
        """)

        resultado = db.session.execute(sql, {
            "cnpj": barbearia.cnpj,
            "nome_barbearia": barbearia.nome_barbearia,
            "telefone": barbearia.telefone,
            "email_empresa": barbearia.email_empresa,
            "logo_barbearia_nome": barbearia.logo_barbearia,
            "data_cadastro": barbearia.data_cadastro,
            "fk_id_endereco": barbearia.endereco.id,
            "agenda_id_agenda": barbearia.agenda.id
        })

        db.session.flush()

        return resultado.rowcount > 0

    def buscar_por_cnpj(self, cnpj: str):
        sql = text("""
            SELECT
                cnpj,
                nome_barbearia,
                telefone,
                email_empresa,
                logo_barbearia_nome,
                data_cadastro,
                fk_id_endereco,
                agenda_id_agenda
            FROM barbearia
            WHERE cnpj = :cnpj
        """)

        registro = db.session.execute(
            sql,
            {"cnpj": cnpj}
        ).mappings().first()

        if registro is None:
            return None

        return self._mapear_barbearia(registro)

    def consultar_todos(self):
        sql = text("""
            SELECT
                cnpj,
                nome_barbearia,
                telefone,
                email_empresa,
                logo_barbearia_nome,
                data_cadastro,
                fk_id_endereco,
                agenda_id_agenda
            FROM barbearia
            ORDER BY nome_barbearia
        """)

        registros = db.session.execute(sql).mappings().all()

        return [
            self._mapear_barbearia(registro)
            for registro in registros
        ]

    def atualizar(self, barbearia: Barbearia):
        sql = text("""
            UPDATE barbearia
            SET
                nome_barbearia = :nome_barbearia,
                telefone = :telefone,
                email_empresa = :email_empresa,
                logo_barbearia_nome = :logo_barbearia_nome,
                fk_id_endereco = :fk_id_endereco,
                agenda_id_agenda = :agenda_id_agenda
            WHERE cnpj = :cnpj
        """)

        resultado = db.session.execute(sql, {
            "cnpj": barbearia.cnpj,
            "nome_barbearia": barbearia.nome_barbearia,
            "telefone": barbearia.telefone,
            "email_empresa": barbearia.email_empresa,
            "logo_barbearia_nome": barbearia.logo_barbearia,
            "fk_id_endereco": barbearia.endereco.id,
            "agenda_id_agenda": barbearia.agenda.id
        })

        db.session.flush()

        return resultado.rowcount > 0

    def excluir(self, cnpj: str):
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

    def _mapear_barbearia(self, registro):

        agenda = self.__agendaDao.buscar_por_id(
            registro["agenda_id_agenda"]
        )

        endereco = self.__enderecoDao.buscar_por_id(
            registro["fk_id_endereco"]
        )

        return Barbearia(
            cnpj=registro["cnpj"],
            nome_barbearia=registro["nome_barbearia"],
            telefone=registro["telefone"],
            email_empresa=registro["email_empresa"],
            logo_barbearia=registro["logo_barbearia_nome"],
            data_cadastro=registro["data_cadastro"],
            endereco=endereco,
            agenda=agenda
        )
