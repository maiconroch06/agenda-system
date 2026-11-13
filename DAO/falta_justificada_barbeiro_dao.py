
from sqlalchemy import text
from database import db
from models import FaltaJustificadaBarbeiro
from DAO.barbeiro_dao import BarbeiroDAO


class FaltaJustificadaBarbeiroDAO:

    def cadastrar(self, falta: FaltaJustificadaBarbeiro):
        sql = text("""
            INSERT INTO faltas_justificadas_barbeiro (
                data_falta,
                horario_inicio_falta,
                horario_final_falta,
                motivo_falta,
                fk_falta_justificada_barbeiro
            ) VALUES (
                :data_falta,
                :horario_inicio_falta,
                :horario_final_falta,
                :motivo_falta,
                :fk_falta_justificada_barbeiro
            )
        """)

        resultado = db.session.execute(sql, {
            "data_falta": falta.data_falta,
            "horario_inicio_falta": falta.horario_inicio_falta,
            "horario_final_falta": falta.horario_final_falta,
            "motivo_falta": falta.motivo_falta,
            "fk_falta_justificada_barbeiro": falta.barbeiro.id
        })

        db.session.commit()

        return resultado.lastrowid

    def buscar_por_id(self, id_falta_justificada: int):
        sql = text("""
            SELECT
                id_falta_justificada,
                data_falta,
                horario_inicio_falta,
                horario_final_falta,
                motivo_falta,
                fk_falta_justificada_barbeiro
            FROM faltas_justificadas_barbeiro
            WHERE id_falta_justificada = :id_falta_justificada
        """)

        registro = db.session.execute(
            sql,
            {"id_falta_justificada": id_falta_justificada}
        ).mappings().first()

        if registro is None:
            return None

        return self._mapear_falta(registro)

    def consultar_todos_por_barbeiro(self, id_barbeiro: int):
        sql = text("""
            SELECT
                id_falta_justificada,
                data_falta,
                horario_inicio_falta,
                horario_final_falta,
                motivo_falta,
                fk_falta_justificada_barbeiro
            FROM faltas_justificadas_barbeiro
            WHERE fk_falta_justificada_barbeiro = :id_barbeiro
            ORDER BY data_falta DESC, horario_inicio_falta
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
            UPDATE faltas_justificadas_barbeiro
            SET
                data_falta = :data_falta,
                horario_inicio_falta = :horario_inicio_falta,
                horario_final_falta = :horario_final_falta,
                motivo_falta = :motivo_falta
            WHERE id_falta_justificada = :id_falta_justificada
              AND fk_falta_justificada_barbeiro = :fk_falta_justificada_barbeiro
        """)

        resultado = db.session.execute(sql, {
            "id_falta_justificada": falta.id_falta_justificada,
            "data_falta": falta.data_falta,
            "horario_inicio_falta": falta.horario_inicio_falta,
            "horario_final_falta": falta.horario_final_falta,
            "motivo_falta": falta.motivo_falta,
            "fk_falta_justificada_barbeiro": falta.barbeiro.id
        })

        db.session.commit()

        return resultado.rowcount > 0

    def excluir(self, id_falta_justificada: int):
        sql = text("""
            DELETE FROM faltas_justificadas_barbeiro
            WHERE id_falta_justificada = :id_falta_justificada
        """)

        resultado = db.session.execute(
            sql,
            {"id_falta_justificada": id_falta_justificada}
        )

        db.session.commit()

        return resultado.rowcount > 0

    def _mapear_falta(self, registro):
        barbeiro = BarbeiroDAO().buscar_por_id(
            registro["fk_falta_justificada_barbeiro"]
        )

        return FaltaJustificadaBarbeiro(
            id_falta_justificada=registro["id_falta_justificada"],
            data_falta=registro["data_falta"],
            horario_inicio_falta=registro["horario_inicio_falta"],
            horario_final_falta=registro["horario_final_falta"],
            motivo_falta=registro["motivo_falta"],
            barbeiro=barbeiro
        )
