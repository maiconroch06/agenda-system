
from sqlalchemy import text
from database import db
from models import Barbearia, HorarioFuncionamento, Endereco
from datetime import datetime

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

    @staticmethod
    def buscar_todos_dados_barbearia():
        sql = text("""
            SELECT
                -- Dados barbearia
                b.cnpj,
                b.nome_barbearia,
                b.telefone,
                b.email_empresa,
                b.logo_barbearia,
                b.data_cadastro,
                b.fk_id_endereco,
                b.fk_id_horario_funcionamento,

                -- Dados horario Funcionamento
                h.id_horario,
                h.horario_abertura,
                h.horario_fechamento,
                h.horario_inicio_intrajornada,
                h.horario_fim_intrajornada,
                h.dias_funcionamento,

                -- Dados do Endereco
                e.id_endereco,
                e.cep,
                e.cidade,
                e.uf,
                e.logradouro,
                e.numero,
                e.bairro,
                e.sequencia,
                e.complemento

            FROM barbearia b

            INNER JOIN horario_funcionamento h
                ON b.fk_id_horario_funcionamento = h.id_horario

            INNER JOIN endereco e
                ON b.fk_id_endereco = e.id_endereco
        """)

        registro = db.session.execute(
                    sql
                ).mappings().first()

        return BarbeariaDAO.mapear_barbearia(registro)

    @staticmethod
    def mapear_barbearia(registro):

        horario_funcionamento = HorarioFuncionamento(
            id_horario=registro["id_horario"],
            horario_abertura=(datetime.min + registro["horario_abertura"]).time(),
            horario_fechamento=(datetime.min + registro["horario_fechamento"]).time(),
            horario_inicio_intrajornada=(datetime.min + registro["horario_inicio_intrajornada"]).time(),
            horario_fim_intrajornada=(datetime.min + registro["horario_fim_intrajornada"]).time(),
            dias_funcionamento=registro["dias_funcionamento"]
        )

            
        endereco = Endereco(
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

        return Barbearia(
            cnpj=registro["cnpj"],
            nome_barbearia=registro["nome_barbearia"],
            telefone=registro["telefone"],
            email_empresa=registro["email_empresa"],
            logo_barbearia=registro["logo_barbearia"],
            data_cadastro=registro["data_cadastro"],
            endereco=endereco,
            horario_funcionamento=horario_funcionamento
        )