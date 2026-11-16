
import json

from sqlalchemy import text
from database import db
from models import HorarioFuncionamento
from datetime import datetime


class HorarioFuncionamentoDAO:

    def buscar_por_id(self, id_horario: int):
        sql = text("""
            SELECT
                id_horario,
                horario_abertura,
                horario_fechamento,
                horario_inicio_intrajornada,
                horario_fim_intrajornada,
                dias_funcionamento
            FROM horario_funcionamento
            WHERE id_horario = :id_horario
        """)

        registro = db.session.execute(
            sql,
            {"id_horario": id_horario}
        ).mappings().first()

        if registro is None:
            return None

        return self._mapear_horario_funcionamento(registro)


    def atualizar(self, horario_funcionamento: HorarioFuncionamento):
        sql = text("""
            UPDATE horario_funcionamento
            SET
                horario_abertura = :horario_abertura,
                horario_fechamento = :horario_fechamento,
                horario_inicio_intrajornada = :horario_inicio_intrajornada,
                horario_fim_intrajornada = :horario_fim_intrajornada,
                dias_funcionamento = :dias_funcionamento
            WHERE id_horario = :id_horario
        """)

        resultado = db.session.execute(sql, {
            "id_horario": horario_funcionamento.id_horario,
            "horario_abertura": horario_funcionamento.horario_abertura,
            "horario_fechamento": horario_funcionamento.horario_fechamento,
            "horario_inicio_intrajornada": horario_funcionamento.horario_inicio_intrajornada,
            "horario_fim_intrajornada": horario_funcionamento.horario_fim_intrajornada,
            "dias_funcionamento": json.dumps(horario_funcionamento.dias_funcionamento)
        })

        db.session.commit()

        return resultado.rowcount > 0

    @staticmethod
    def _mapear_horario_funcionamento(registro):
        dias_funcionamento = registro["dias_funcionamento"]

        # Converte o JSON retornado pelo banco em uma lista Python.
        if isinstance(dias_funcionamento, str):
            dias_funcionamento = json.loads(dias_funcionamento)

        return HorarioFuncionamento(
            id_horario=registro["id_horario"],
            horario_abertura=(datetime.min + registro["horario_abertura"]).time(),
            horario_fechamento=(datetime.min + registro["horario_fechamento"]).time(),
            horario_inicio_intrajornada=(datetime.min + registro["horario_inicio_intrajornada"]).time(),
            horario_fim_intrajornada=(datetime.min + registro["horario_fim_intrajornada"]).time(),
            dias_funcionamento=dias_funcionamento or []
        )
        
        # datetime.min: representa 0001-01-01 00:00:00.
        # registro["horario_abertura"]: contém um timedelta, por exemplo, 8 horas e 30 minutos.
        # datetime.min + timedelta: soma a duração à data inicial, resultando em 0001-01-01 08:30:00.
        # .time(): extrai somente o horário, descartando a data.