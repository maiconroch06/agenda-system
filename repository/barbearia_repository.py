
from DAO.barbearia_dao import BarbeariaDAO


class BarbeariaRepository:

    @staticmethod
    def salvar(barbearia):
        return BarbeariaDAO.salvar(barbearia)

    @staticmethod
    def buscar_por_cnpj(cnpj):
        return BarbeariaDAO.buscar_por_cnpj(cnpj)

    @staticmethod
    def listar_todas():
        return BarbeariaDAO.listar_todas()

    @staticmethod
    def atualizar(barbearia):
        return BarbeariaDAO.atualizar(barbearia)

    @staticmethod
    def excluir(cnpj):
        return BarbeariaDAO.excluir(cnpj)
