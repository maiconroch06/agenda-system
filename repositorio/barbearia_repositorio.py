
from DAO.barbearia_dao import BarbeariaDAO


class BarbeariaRepositorio:

    @staticmethod
    def buscar_cnpj():
        return BarbeariaDAO().buscar_cnpj()

    staticmethod
    def buscar_todos_dados_barbearia():
        return BarbeariaDAO.buscar_todos_dados_barbearia()

