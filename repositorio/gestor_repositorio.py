
from DAO.gestor_dao import GestorDAO


class GestorRepositorio:
    
    def __init__(self):
        self.gestor_dao = GestorDAO()
  
    def consultar_gestor(self, email):
        return self.gestor_dao.consultarGestorBarbearia(email)

    def listar_todos(self):
        return self.gestor_dao.consultarGestores()
          
    def atualizar(self, gestor):
        return self.gestor_dao.atualizar(gestor)
    
    def excluir(self, id_gestor):
        return self.gestor_dao.excluir(id_gestor)
