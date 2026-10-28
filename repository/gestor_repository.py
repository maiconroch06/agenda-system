
from DAO.gestor_dao import GestorDAO


class GestorRepository:

    @staticmethod
    def salvar(gestor):
        return GestorDAO.salvar(gestor)

    @staticmethod
    def buscar_por_id(id_gestor):
        return GestorDAO.buscar_por_id(id_gestor)

    @staticmethod
    def listar_todos():
        return GestorDAO.listar_todos()

    @staticmethod
    def listar_por_barbearia(cnpj):
        return GestorDAO.listar_por_barbearia(cnpj)

    @staticmethod
    def atualizar(gestor):
        return GestorDAO.atualizar(gestor)

    @staticmethod
    def excluir(id_gestor):
        return GestorDAO.excluir(id_gestor)
