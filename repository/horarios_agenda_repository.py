from DAO.horarios_agenda_dao import HorariosAgendaDAO


class HorariosAgendaRepository:

    @staticmethod
    def salvar(horario):
        return HorariosAgendaDAO.salvar(horario)

    @staticmethod
    def buscar_por_id(id_horario):
        return HorariosAgendaDAO.buscar_por_id(id_horario)

    @staticmethod
    def listar_todos():
        return HorariosAgendaDAO.listar_todos()

    @staticmethod
    def listar_por_agenda(id_agenda):
        return HorariosAgendaDAO.listar_por_agenda(id_agenda)

    @staticmethod
    def atualizar(horario):
        return HorariosAgendaDAO.atualizar(horario)

    @staticmethod
    def excluir(id_horario):
        return HorariosAgendaDAO.excluir(id_horario)