
from sqlalchemy import text
from database import db
from models.horarios_agenda import HorariosAgenda


class HorariosAgendaDAO:

    @staticmethod
    def salvar(horario: HorariosAgenda):
        sql = text("""
            INSERT INTO horarios_agenda (
                inicio_expediente,
                fim_expediente,
                data_mes,
                intervalo_descanco_inicio,
                intervalo_descanso_fim,
                dias_semana,
                fk_id_agenda
            ) VALUES (
                :inicio_expediente,
                :fim_expediente,
                :data_mes,
                :intervalo_descanco_inicio,
                :intervalo_descanso_fim,
                :dias_semana,
                :fk_id_agenda
            )
        """)

        resultado = db.session.execute(sql, {
            "inicio_expediente": horario.inicio_expediente,
            "fim_expediente": horario.fim_expediente,
            "data_mes": horario.data_mes,
            "intervalo_descanco_inicio": horario.intervalo_descanco_inicio,
            "intervalo_descanso_fim": horario.intervalo_descanso_fim,
            "dias_semana": horario.dias_semana,
            "fk_id_agenda": horario.fk_id_agenda
        })

        horario.id = resultado.lastrowid

        db.session.flush()

        return horario.id

    @staticmethod
    def buscar_por_id(id_horario: int):
        sql = text("""
            SELECT
                id,
                inicio_expediente,
                fim_expediente,
                data_mes,
                intervalo_descanco_inicio,
                intervalo_descanso_fim,
                dias_semana,
                fk_id_agenda
            FROM horarios_agenda
            WHERE id = :id
        """)

        registro = db.session.execute(
            sql,
            {"id": id_horario}
        ).mappings().first()

        if registro is None:
            return None

        return HorariosAgendaDAO._mapear(registro)

    @staticmethod
    def listar_todos():
        sql = text("""
            SELECT
                id,
                inicio_expediente,
                fim_expediente,
                data_mes,
                intervalo_descanco_inicio,
                intervalo_descanso_fim,
                dias_semana,
                fk_id_agenda
            FROM horarios_agenda
            ORDER BY data_mes, inicio_expediente
        """)

        registros = db.session.execute(sql).mappings().all()

        return [
            HorariosAgendaDAO._mapear(registro)
            for registro in registros
        ]

    @staticmethod
    def listar_por_agenda(fk_id_agenda: int):
        sql = text("""
            SELECT
                id,
                inicio_expediente,
                fim_expediente,
                data_mes,
                intervalo_descanco_inicio,
                intervalo_descanso_fim,
                dias_semana,
                fk_id_agenda
            FROM horarios_agenda
            WHERE fk_id_agenda = :fk_id_agenda
            ORDER BY data_mes, inicio_expediente
        """)

        registros = db.session.execute(
            sql,
            {"fk_id_agenda": fk_id_agenda}
        ).mappings().all()

        return [
            HorariosAgendaDAO._mapear(registro)
            for registro in registros
        ]

    @staticmethod
    def atualizar(horario: HorariosAgenda):
        sql = text("""
            UPDATE horarios_agenda
            SET
                inicio_expediente = :inicio_expediente,
                fim_expediente = :fim_expediente,
                data_mes = :data_mes,
                intervalo_descanco_inicio = :intervalo_descanco_inicio,
                intervalo_descanso_fim = :intervalo_descanso_fim,
                dias_semana = :dias_semana,
                fk_id_agenda = :fk_id_agenda
            WHERE id = :id
        """)

        resultado = db.session.execute(sql, {
            "id": horario.id,
            "inicio_expediente": horario.inicio_expediente,
            "fim_expediente": horario.fim_expediente,
            "data_mes": horario.data_mes,
            "intervalo_descanco_inicio": horario.intervalo_descanco_inicio,
            "intervalo_descanso_fim": horario.intervalo_descanso_fim,
            "dias_semana": horario.dias_semana,
            "fk_id_agenda": horario.fk_id_agenda
        })

        db.session.flush()

        return resultado.rowcount > 0

    @staticmethod
    def excluir(id_horario: int):
        sql = text("""
            DELETE FROM horarios_agenda
            WHERE id = :id
        """)

        resultado = db.session.execute(
            sql,
            {"id": id_horario}
        )

        db.session.flush()

        return resultado.rowcount > 0

    @staticmethod
    def _mapear(registro):
        return HorariosAgenda(
            id=registro["id"],
            inicio_expediente=registro["inicio_expediente"],
            fim_expediente=registro["fim_expediente"],
            data_mes=registro["data_mes"],
            intervalo_descanco_inicio=registro["intervalo_descanco_inicio"],
            intervalo_descanso_fim=registro["intervalo_descanso_fim"],
            dias_semana=registro["dias_semana"],
            fk_id_agenda=registro["fk_id_agenda"]
        )
