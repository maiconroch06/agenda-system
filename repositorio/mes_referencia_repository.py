
from DAO.mes_referencia_dao import MesReferenciaDAO


class MesReferenciaRepositorio:

    def __init__(self):
        self.__mesReferenciaDao = MesReferenciaDAO()

    def salvar(self, mes_referencia):
        return self.__mesReferenciaDao.cadastrar(mes_referencia)

    def buscar_por_id(self, id_mes: int):
        return self.__mesReferenciaDao.buscar_por_id(id_mes)

    def listar_por_agenda(self, id_agenda: int):
        return self.__mesReferenciaDao.listar_por_agenda(id_agenda)

    def listar_todos(self):
        return self.__mesReferenciaDao.listar_todos()

    def atualizar(self, mes_referencia):
        return self.__mesReferenciaDao.atualizar(mes_referencia)

    def excluir(self, id_mes: int):
        return self.__mesReferenciaDao.excluir(id_mes)
