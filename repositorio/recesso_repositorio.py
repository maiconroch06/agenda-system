
from DAO.recesso_dao import RecessoDao


class RecessoRepositorio:

    @staticmethod
    def salvar(barbearia):
        return RecessoDao.salvar(barbearia)

    @staticmethod
    def buscar_por_cnpj(cnpj):
        return RecessoDao.buscar_por_cnpj(cnpj)

    @staticmethod
    def listar_todas():
        return RecessoDao.listar_todas()

    @staticmethod
    def atualizar(barbearia):
        return RecessoDao.atualizar(barbearia)

    @staticmethod
    def excluir(cnpj):
        return RecessoDao.excluir(cnpj)
