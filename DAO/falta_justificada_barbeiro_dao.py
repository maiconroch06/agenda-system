
from sqlalchemy import text
from database import db
from models import FaltaJustificadaBarbeiro
from DAO.barbeiro_dao import BarbeiroDAO


class FaltaJustificadaBarbeiroDAO:

    def cadastrar(self, id_barbeiro, falta_justificada: FaltaJustificadaBarbeiro):
        sql = text("""
            INSERT INTO falta_justificada_barbeiro (
                data_falta,
                horario_inicio_falta,
                horario_final_falta,
                motivo_falta,
                fk_barbeiro_falta_justificada
            ) VALUES (
                :data_falta,
                :horario_inicio_falta,
                :horario_final_falta,
                :motivo_falta,
                :fk_barbeiro_falta_justificada
            )
        """)

        resultado = db.session.execute(sql, {
            "data_falta": falta_justificada.data_falta,
            "horario_inicio_falta": falta_justificada.horario_inicio_falta,
            "horario_final_falta": falta_justificada.horario_final_falta,
            "motivo_falta": falta_justificada.motivo_falta,
            "fk_barbeiro_falta_justificada": id_barbeiro
        })

        db.session.commit()

        return resultado.lastrowid > 0

    

    def consultar_todos_por_barbeiro(self, id_barbeiro: int):
        sql = text("""
            SELECT
                id_falta_justificada,
                data_falta,
                horario_inicio_falta,
                horario_final_falta,
                motivo_falta,
                fk_barbeiro_falta_justificada
            FROM falta_justificada_barbeiro
            WHERE fk_barbeiro_falta_justificada = :id_barbeiro
            ORDER BY data_falta DESC, horario_inicio_falta asc
        """)

        registros = db.session.execute(
            sql,
            {"id_barbeiro": id_barbeiro}
        ).mappings().all()

        return [
            self._mapear_falta(registro)
            for registro in registros
        ]

    def atualizar(self, falta: FaltaJustificadaBarbeiro):
        sql = text("""
            UPDATE falta_justificada_barbeiro
            SET
                data_falta = :data_falta,
                horario_inicio_falta = :horario_inicio_falta,
                horario_final_falta = :horario_final_falta,
                motivo_falta = :motivo_falta
            WHERE id_falta_justificada = :id_falta_justificada
        """)

        resultado = db.session.execute(sql, {
            "id_falta_justificada": falta.id_falta_justificada,
            "data_falta": falta.data_falta,
            "horario_inicio_falta": falta.horario_inicio_falta,
            "horario_final_falta": falta.horario_final_falta,
            "motivo_falta": falta.motivo_falta,
        })

        db.session.commit()

        return resultado.rowcount > 0

    def excluir(self, id_falta_justificada: int):
        sql = text("""
            DELETE FROM falta_justificada_barbeiro
            WHERE id_falta_justificada = :id_falta_justificada
        """)

        resultado = db.session.execute(
            sql,
            {"id_falta_justificada": id_falta_justificada}
        )

        db.session.commit()

        return resultado.rowcount > 0
    
    def verificar_falta_justificativa_existente_barbeiro_dao(self, id_barbeiro, falta_justificada):
        sql = text("""
            SELECT count(id_falta_justificada) 
            FROM falta_justificada_barbeiro
            where data_falta = :data_falta 
            and horario_final_falta >= :hora_inicial_falta
            AND horario_inicio_falta <= :horario_final_falta
            and fk_barbeiro_falta_justificada = :fk_barbeiro_falta_justificada;
        """)

        resultado = db.session.execute(
            sql,
            {
                "data_falta": falta_justificada.data_falta,
                "hora_inicial_falta": falta_justificada.horario_inicio_falta,
                "horario_final_falta": falta_justificada.horario_final_falta,
                "fk_barbeiro_falta_justificada": id_barbeiro
                }
        )

        return resultado.scalar() > 0
    
    def verificar_atualizacao_falta_justificativa_existente_barbeiro_dao(self, id_barbeiro, falta_justificada):
            sql = text("""
                SELECT count(id_falta_justificada) 
                FROM falta_justificada_barbeiro
                where data_falta = :data_falta 
                AND horario_final_falta >= :hora_inicial_falta
                AND horario_inicio_falta <= :horario_final_falta
                and id_falta_justificada != :id_falta_justificada and fk_barbeiro_falta_justificada = :fk_barbeiro_falta_justificada
            """)
    
            resultado = db.session.execute(
                sql,
                {   "id_falta_justificada":falta_justificada.id_falta_justificada,
                    "data_falta": falta_justificada.data_falta,
                    "hora_inicial_falta": falta_justificada.horario_inicio_falta,
                    "horario_final_falta": falta_justificada.horario_final_falta,
                    "fk_barbeiro_falta_justificada": id_barbeiro
                    }
            )
    
            return resultado.scalar() > 0

    @staticmethod
    def consultar_faltas_por_periodo(data_inicio, data_fim):

        sql = text("""
            SELECT
                f.id_falta_justificada,
                f.data_falta,
                f.horario_inicio_falta,
                f.horario_final_falta,
                f.motivo_falta,
                f.fk_barbeiro_falta_justificada AS id_barbeiro

            FROM falta_justificada_barbeiro f

            INNER JOIN barbeiro b
                ON b.id_barbeiro = f.fk_barbeiro_falta_justificada

            INNER JOIN usuario u
                ON u.id_usuario = b.id_barbeiro

            WHERE f.data_falta BETWEEN :data_inicio AND :data_fim

            ORDER BY
                f.data_falta,
                f.horario_inicio_falta
        """)

        resultado = db.session.execute(
            sql,
            {
                "data_inicio": data_inicio,
                "data_fim": data_fim
            }
        ).mappings().all()

        return resultado
    
    

    def _mapear_falta(self, registro):
        barbeiro = BarbeiroDAO().buscar_por_id(
            registro["fk_barbeiro_falta_justificada"]
        )

        return FaltaJustificadaBarbeiro(
            id_falta_justificada=registro["id_falta_justificada"],
            data_falta=registro["data_falta"],
            horario_inicio_falta=registro["horario_inicio_falta"],
            horario_final_falta=registro["horario_final_falta"],
            motivo_falta=registro["motivo_falta"],
            barbeiro=barbeiro
        )
