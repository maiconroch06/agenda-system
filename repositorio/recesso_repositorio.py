
from DAO.recesso_dao import RecessoDAO


class RecessoRepositorio:

    def __init__(self):
        self.__recessoDao = RecessoDAO()

    def salvar(self, recesso):
        return self.__recessoDao.cadastrar(recesso)

    def buscar_por_id(self, id_recesso: int):
        return self.__recessoDao.buscar_por_id(id_recesso)

    def listar_por_mes_referencia(self, id_mes: int):
        return self.__recessoDao.listar_por_mes_referencia(id_mes)

    def listar_todos(self):
        return self.__recessoDao.listar_todos()

    def atualizar(self, recesso):
        return self.__recessoDao.atualizar(recesso)

    def excluir(self, id_recesso: int):
        return self.__recessoDao.excluir(id_recesso)