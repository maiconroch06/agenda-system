
from sqlalchemy import text
from database import db
from datetime import date, timezone
import calendar

from models import Recesso
from DAO.agenda_mensal_dao import AgendaMensalDAO


class RecessoDAO:

    def __init__(self):
        self.__mesReferenciaDao = AgendaMensalDAO()

    def cadastrar_dao(self, recesso: Recesso, barbearia_cnpj):
        sql = text("""
            INSERT INTO recesso (
                data_inicio_recesso,
                data_fim_recesso,
                descricao_recesso,
                fk_barbearia_cnpj
            ) VALUES (
                :data_inicio_recesso,
                :data_fim_recesso,
                :descricao_recesso,
                :fk_barbearia_cnpj
            )
        """)

        resultado = db.session.execute(sql, {
            "data_inicio_recesso": recesso.data_inicio_recesso,
            "data_fim_recesso": recesso.data_fim_recesso,
            "descricao_recesso": recesso.descricao_recesso,
            "fk_barbearia_cnpj":barbearia_cnpj
        })

        db.session.commit()

        return resultado.rowcount > 0

    def listar_por_mes (self):
        sql = text("""
            SELECT
                id_recesso,
                descricao_recesso,
                data_inicio_recesso,
                data_fim_recesso
            FROM recesso
            WHERE data_inicio_recesso >= :data_inicio and data_fim_recesso <= :data_final
        """)

        resultado = db.session.execute(
            sql,
            {
                "data_inicio": date.today().replace(day=1),
                "data_final": date.today().replace(day=calendar.monthrange(date.today().year, date.today().month)[1]),
             }
        ).mappings().all()

      
        if not resultado:
            return None

        return  [
            self.__mapear_recesso(registro)
            for registro in resultado
        ]
        
    def verificar_recesso_existente_cadastro(self, recesso):
        sql = text("""
                    SELECT count(id_recesso)  
                    FROM recesso 
                    WHERE data_fim_recesso >= :data_inicio_mes;
                """)
        
           
        resultado = db.session.execute(
            sql,
            {"data_inicio_mes": recesso.data_inicio_recesso}
        )
        
        db.session.commit()

        return resultado.scalar()
    
    
    def verificar_recesso_intervalo_existente_dao(self, recesso):
        sql = text("""
                    SELECT count(id_recesso)  FROM recesso
                    where 
                    data_fim_recesso >= :data_inicio_recesso
                    and data_inicio_recesso 
                    <= :data_fim_recesso 
                    and id_recesso != :id_recesso
                """)
        
        resultado = db.session.execute(
            sql,
            {"id_recesso": recesso.id_recesso,
                "data_inicio_recesso": recesso.data_inicio_recesso,
                "data_fim_recesso": recesso.data_fim_recesso,
               
                }
        )
        
        db.session.commit()
        
        return resultado.scalar()

    def listar_todos(self):
        sql = text("""
            SELECT
                id_recesso,
                descricao_recesso,
                data_inicio_recesso,
                data_fim_recesso
            FROM recesso
            ORDER BY data_fim_recesso DESC
        """)

        resultados = db.session.execute(sql).mappings().all()

        return  [
                    self.__mapear_recesso(registro)
                    for registro in resultados
                ]
            

    def atualizar(self, recesso: Recesso):
        sql = text("""
            UPDATE recesso
            SET
                data_inicio_recesso = :data_inicio_recesso,
                descricao_recesso = :descricao_recesso,
                data_fim_recesso = :data_fim_recesso
            WHERE id_recesso = :id_recesso
        """)

        resultado = db.session.execute(sql, {
            "id_recesso": recesso.id_recesso,
            "data_inicio_recesso": recesso.data_inicio_recesso,
            "data_fim_recesso": recesso.data_fim_recesso,
            "descricao_recesso": recesso.descricao_recesso,
            
        })

        db.session.commit()

        return resultado.rowcount > 0

    def excluir(self, id_recesso: int):
        sql = text("""
            DELETE FROM recesso
            WHERE id_recesso = :id_recesso
        """)

        resultado = db.session.execute(
            sql,
            {"id_recesso": id_recesso}
        )

        db.session.commit()

        return resultado.rowcount > 0

    def __mapear_recesso(self, registro):
        
        return Recesso(
            id_recesso=registro["id_recesso"],
            data_inicio_recesso=registro["data_inicio_recesso"],
            descricao_recesso=registro["descricao_recesso"],
            data_fim_recesso=registro["data_fim_recesso"],
        )
