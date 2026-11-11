
from sqlalchemy import text
from database import db

from models import AgendaMensal
from .horario_funcionamento_dao import HorarioFuncionamentoDAO


class AgendaMensalDAO:

    def __init__(self):
        self.__horarioFuncionamento = HorarioFuncionamentoDAO()

    def cadastrar(self, nova_agenda_mensal, cnpj_barbearia):
        sql = text("""
            INSERT INTO agenda_mensal (
                data_inicial_mes,
                data_final_mes,
                titulo_agenda,
                fk_barbearia_cnpj
            ) VALUES (
                :data_inicial_mes,
                :data_final_mes,
                :titulo_agenda,
                :fk_barbearia_cnpj
            )
        """)

        resultado = db.session.execute(sql, {
            "data_inicial_mes": nova_agenda_mensal.data_inicial_mes,
            "data_final_mes": nova_agenda_mensal.data_final_mes,
            "titulo_agenda": nova_agenda_mensal.titulo_agenda,
            "fk_barbearia_cnpj": cnpj_barbearia
        })

        db.session.commit()

        return resultado.lastrowid

    def buscar_por_id(self, id_agenda_mensal: int):
        sql = text("""
            SELECT
                id_agenda_mensal,
                data_inicial_mes,
                data_final_mes,
                titulo_agenda,
                fk_id_horario
            FROM agenda_mensal
            WHERE id_agenda_mensal = :id_agenda_mensal
        """)

        resultado = db.session.execute(
            sql,
            {"id_agenda_mensal": id_agenda_mensal}
        ).mappings().first()

        if not resultado:
            return None

        return self.__mapear_agenda_mensal(resultado)

    def listar_por_agenda(self, id_agenda_mensal: int):
        sql = text("""
            SELECT
                id_agenda_mensal,
                data_inicial_mes,
                data_final_mes,
                titulo_agenda,
                fk_id_horario
            FROM agenda_mensal
            WHERE fk_id_horario = :id_agenda
            ORDER BY data_inicial_mes
        """)

        resultados = db.session.execute(
            sql,
            {"id_agenda": id_agenda_mensal}
        ).mappings().all()

        return [
            self.__mapear_agenda_mensal(registro)
            for registro in resultados
        ]

    def listar_todos(self):
        sql = text("""
            SELECT
                id_agenda_mensal,
                data_inicial_mes,
                data_final_mes,
                titulo_agenda
            FROM agenda_mensal
            ORDER BY data_inicial_mes
        """)

        resultados = db.session.execute(sql).mappings().all()

        return [
            self.__mapear_agenda_mensal(registro)
            for registro in resultados
        ]

    def atualizar(self, agenda_mensal: AgendaMensal):
        sql = text("""
            UPDATE agenda_mensal
            SET
                data_inicial_mes = :data_inicial_mes,
                data_final_mes = :data_final_mes,
                titulo_agenda = :titulo_agenda,
            WHERE id_agenda_mensal = :id_agenda_mensal
        """)

        resultado = db.session.execute(sql, {
            "id_agenda_mensal": agenda_mensal.id_agenda_mensal,
            "data_inicial_mes": agenda_mensal.data_inicial_mes,
            "data_final_mes": agenda_mensal.data_final_mes,
            "titulo_agenda": agenda_mensal.titulo_agenda,
        })

        db.session.commit()

        return resultado.rowcount > 0

    def excluir(self, id_agenda_mensal: int):
        sql = text("""
            DELETE FROM agenda_mensal
            WHERE id_agenda_mensal = :id_agenda_mensal
        """)

        resultado = db.session.execute(
            sql,
            {"id_agenda_mensal": id_agenda_mensal}
        )

        db.session.commit()

        return resultado.rowcount > 0

    def __mapear_agenda_mensal(self, registro):
       
        return AgendaMensal(
            id_agenda_mensal=registro["id_agenda_mensal"],
            data_inicial_mes=registro["data_inicial_mes"],
            data_final_mes=registro["data_final_mes"],
            titulo_agenda=registro["titulo_agenda"]
        )
