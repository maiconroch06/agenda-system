
from DAO.barbeiro_dao import BarbeiroDAO


class BarbeiroRepository:

    @staticmethod
    def salvar(barbeiro):
        return BarbeiroDAO.salvar(barbeiro)

    @staticmethod
    def buscar_por_id(id_barbeiro):
        return BarbeiroDAO.buscar_por_id(id_barbeiro)

    @staticmethod
    def listar_todos():
        return BarbeiroDAO.listar_todos()

    @staticmethod
    def atualizar(barbeiro):
        return BarbeiroDAO.atualizar(barbeiro)

    @staticmethod
    def excluir(id_barbeiro):
        return BarbeiroDAO.excluir(id_barbeiro)
