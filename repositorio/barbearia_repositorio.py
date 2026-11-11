
from DAO.barbearia_dao import BarbeariaDAO


class BarbeariaRepositorio:

    @staticmethod
    def buscar_cnpj():
        return BarbeariaDAO().buscar_cnpj()

