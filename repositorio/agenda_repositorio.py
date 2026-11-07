
from DAO.agenda_dao import AgendaDAO

class AgendaRepositorio:
    def __init__(self):
       self.__agenda_dao = AgendaDAO()

    def cadastrar_agenda(self, agenda):
        return  self.__agenda_dao.cadastrar_agenda_dao(agenda)

    
    def buscar_por_id(self,id_agenda):
        return  self.__agenda_dao.buscar_por_id(id_agenda)

   
    def listar_todos(self):
        return  self.__agenda_dao.listar_todos()

    
    def atualizar(self, agenda):
        return  self.__agenda_dao.atualizar(agenda)

   
    def excluir(self,id_agenda):
        return  self.__agenda_dao.excluir(id_agenda)
