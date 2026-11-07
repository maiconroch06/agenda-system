
from DAO.agenda_dao import AgendaDAO

class AgendaRepositorio:

    def salvar(self, agenda):
        return AgendaDAO.salvar(agenda)

    
    def buscar_por_id(self,id_agenda):
        return AgendaDAO.buscar_por_id(id_agenda)

   
    def listar_todos(self):
        return AgendaDAO.listar_todos()

    
    def atualizar(self, agenda):
        return AgendaDAO.atualizar(agenda)

   
    def excluir(self,id_agenda):
        return AgendaDAO.excluir(id_agenda)
