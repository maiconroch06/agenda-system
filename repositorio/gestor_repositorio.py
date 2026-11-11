
from DAO.gestor_dao import GestorDAO


class GestorRepositorio:
    
    def __init__(self):
        self.gestor_dao = GestorDAO()
  
    def realizar_login(self, email):
        return self.gestor_dao.realizar_login_dao(email)
