
from sqlalchemy import text
from database import db
from models import Barbearia

class BarbeariaDAO:
    
    @staticmethod
    def buscar_cnpj():
        sql = text("""
            SELECT
                cnpj    
            FROM barbearia
            
        """)

        registro = db.session.execute(
            sql
        ).mappings().first()

        return registro["cnpj"]

    def _mapear_barbearia(self, registro):

        agenda = self.__horarioFuncionamentoDao.buscar_por_id(
            registro["fk_id_horario_funcionamento"]
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