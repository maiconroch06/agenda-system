
from sqlalchemy import text
from database import db

from models import AgendaMensal
from .horario_funcionamento_dao import HorarioFuncionamentoDAO


class AgendaMensalDAO:

    def __init__(self):
        self.__horarioFuncionamento = HorarioFuncionamentoDAO()

    def cadastrar(self, nova_agenda_mensal:AgendaMensal, cnpj_barbearia):
        sql = text("""
            INSERT INTO agenda_mensal (
                data_inicial_mes,
                data_final_mes,
                titulo_agenda,
                status_agenda_mensal,
                fk_barbearia_cnpj
            ) VALUES (
                :data_inicial_mes,
                :data_final_mes,
                :titulo_agenda,
                :status_agenda_mensal,
                :fk_barbearia_cnpj
            )
        """)

        resultado = db.session.execute(sql, {
            "data_inicial_mes": nova_agenda_mensal.data_inicial_mes,
            "data_final_mes": nova_agenda_mensal.data_final_mes,
            "titulo_agenda": nova_agenda_mensal.titulo_agenda,
            "status_agenda_mensal": nova_agenda_mensal.status_agenda_mensal,
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
                status_agenda_mensal,
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
                status_agenda_mensal,
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
                titulo_agenda,
                status_agenda_mensal
            FROM agenda_mensal
            ORDER BY data_inicial_mes
        """)

        resultados = db.session.execute(sql).mappings().all()

        return [
            self.__mapear_agenda_mensal(registro)
            for registro in resultados
        ]
        
    def atualizar_status_agenda_mensal(self, agenda_mensal):
        sql = text("""
                       UPDATE agenda_mensal
                       SET
                        status_agenda_mensal=:status_agenda_mensal
                       WHERE id_agenda_mensal = :id_agenda_mensal
                   """)
           
        resultado = db.session.execute(sql, {
                       "id_agenda_mensal": agenda_mensal.id_agenda_mensal,
                       "status_agenda_mensal": agenda_mensal.status_agenda_mensal,
                   })
           
        db.session.commit()

        return resultado.rowcount > 0

    def atualizar(self, agenda_mensal: AgendaMensal):
        sql = text("""
            UPDATE agenda_mensal
            SET
                data_inicial_mes = :data_inicial_mes,
                data_final_mes = :data_final_mes,
                titulo_agenda = :titulo_agenda
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
    
    
    def verificar_agenda_aberta(self, agenda):
        sql = text("""
                    SELECT count(id_agenda_mensal)  
                    FROM agenda_mensal 
                    WHERE data_final_mes >= :data_inicio_mes  and status_agenda_mensal=:status_agenda_mensal;
                """)
        
        resultado = db.session.execute(
            sql,
            {"data_inicio_mes": agenda.data_inicial_mes,
             "status_agenda_mensal": True}
        )
        
        db.session.commit()

        return resultado.scalar()

    def verificar_agenda_mensal_existente(self, agenda):
        sql = text("""
                    SELECT count(id_agenda_mensal)  FROM agenda_mensal
                    where 
                    data_final_mes >= :data_inicial_mes
                    and data_inicial_mes 
                    <= :data_final_mes 
                    and status_agenda_mensal=:status_agenda_mensal
                    and id_agenda_mensal != :id_agenda_mensal
                """)
        
        resultado = db.session.execute(
            sql,
            {"id_agenda_mensal": agenda.id_agenda_mensal,
             "data_inicial_mes": agenda.data_inicial_mes,
             "data_final_mes": agenda.data_final_mes,
             "status_agenda_mensal": True
             }
        )
        
        db.session.commit()
        

        return resultado.scalar()



    def __mapear_agenda_mensal(self, registro):
       
        return AgendaMensal(
            id_agenda_mensal=registro["id_agenda_mensal"],
            data_inicial_mes=registro["data_inicial_mes"],
            data_final_mes=registro["data_final_mes"],
            titulo_agenda=registro["titulo_agenda"],
            status_agenda_mensal=registro["status_agenda_mensal"]
        )
