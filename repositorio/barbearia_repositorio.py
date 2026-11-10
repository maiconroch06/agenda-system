
from DAO.barbearia_dao import BarbeariaDAO


class BarbeariaRepositorio:

    def __init__(self):
        self.__barbeariaDao = BarbeariaDAO()

    def buscar_por_cnpj(self, cnpj: str):
        return self.__barbeariaDao.buscar_por_cnpj(cnpj)

    def listar_todos(self):
        return self.__barbeariaDao.consultar_todos()