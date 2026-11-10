
from sqlalchemy import text
from database import db
from models import Barbearia
from DAO.agenda_dao import AgendaDAO
from DAO.endereco_dao import EnderecoDAO


class BarbeariaDAO:

    def __init__(self):
        self.__agendaDao = AgendaDAO()
        self.__enderecoDao = EnderecoDAO()

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