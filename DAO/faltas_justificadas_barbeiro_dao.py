
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
                fk_id_barbeiro
            ) VALUES (
                :data_falta,
                :horario_inicio_falta,
                :horario_final_falta,
                :motivo_falta,
                :fk_id_barbeiro
            )
        """)

        resultado = db.session.execute(sql, {
            "data_falta": falta.data_falta,
            "horario_inicio_falta": falta.horario_inicio_falta,
            "horario_final_falta": falta.horario_final_falta,
            "motivo_falta": falta.motivo_falta,
            "fk_id_barbeiro": falta.barbeiro.id
        })

        db.session.flush()

        return resultado.rowcount > 0

    def buscar_por_id(self, id_falta: int):
        sql = text("""
            SELECT
                id,
                data_falta,
                horario_inicio_falta,
                horario_final_falta,
                motivo_falta,
                fk_id_barbeiro
            FROM faltas_justificadas_barbeiro
            WHERE id = :id
        """)

        registro = db.session.execute(
            sql,
            {"id": id_falta}
        ).mappings().first()

        if registro is None:
            return None

        return self._mapear_falta(registro)

    def consultar_todos_por_barbeiro(self, id_barbeiro: int):
        sql = text("""
            SELECT
                id,
                data_falta,
                horario_inicio_falta,
                horario_final_falta,
                motivo_falta,
                fk_id_barbeiro
            FROM faltas_justificadas_barbeiro
            WHERE fk_id_barbeiro = :id_barbeiro
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
            WHERE id = :id
              AND fk_id_barbeiro = :fk_id_barbeiro
        """)

        resultado = db.session.execute(sql, {
            "id": falta.id,
            "data_falta": falta.data_falta,
            "horario_inicio_falta": falta.horario_inicio_falta,
            "horario_final_falta": falta.horario_final_falta,
            "motivo_falta": falta.motivo_falta,
            "fk_id_barbeiro": falta.barbeiro.id
        })

        db.session.flush()

        return resultado.rowcount > 0

    def excluir(self, id_falta: int):
        sql = text("""
            DELETE FROM faltas_justificadas_barbeiro
            WHERE id = :id
        """)

        resultado = db.session.execute(
            sql,
            {"id": id_falta}
        )

        db.session.flush()

        return resultado.rowcount > 0

    def _mapear_falta(self, registro):
        barbeiro = BarbeiroDAO().buscar_por_id(
            registro["fk_id_barbeiro"]
        )

        return FaltaJustificadaBarbeiro(
            id=registro["id"],
            data_falta=registro["data_falta"],
            horario_inicio_falta=registro["horario_inicio_falta"],
            horario_final_falta=registro["horario_final_falta"],
            motivo_falta=registro["motivo_falta"],
            barbeiro=barbeiro
        )
