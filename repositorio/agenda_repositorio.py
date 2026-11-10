
from DAO.agenda_dao import AgendaDAO


class AgendaRepositorio:

    def __init__(self):
        self.__agendaDao = AgendaDAO()

    def salvar(self, agenda):
        return self.__agendaDao.cadastrar(agenda)

    def buscar_por_id(self, id_agenda: int):
        return self.__agendaDao.buscar_por_id(id_agenda)

    def listar_todos(self):
        return self.__agendaDao.consultar_todos()

    def atualizar(self, agenda):
        return self.__agendaDao.atualizar(agenda)

    def excluir(self, id_agenda: int):
        return self.__agendaDao.excluir(id_agenda)