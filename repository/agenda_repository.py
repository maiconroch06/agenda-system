
from DAO.agenda_dao import AgendaDAO


class AgendaRepository:

    @staticmethod
    def salvar(agenda):
        return AgendaDAO.salvar(agenda)

    @staticmethod
    def buscar_por_id(id_agenda):
        return AgendaDAO.buscar_por_id(id_agenda)

    @staticmethod
    def listar_todos():
        return AgendaDAO.listar_todos()

    @staticmethod
    def atualizar(agenda):
        return AgendaDAO.atualizar(agenda)

    @staticmethod
    def excluir(id_agenda):
        return AgendaDAO.excluir(id_agenda)
