
from DAO.faltas_justificadas_barbeiro_dao import FaltaJustificadaBarbeiroDAO


class FaltaJustificadaBarbeiroRepositorio:

    def __init__(self):
        self.__faltaDao = FaltaJustificadaBarbeiroDAO()

    def salvar(self, falta):
        return self.__faltaDao.cadastrar(falta)

    def buscar_por_id(self, id_falta: int):
        return self.__faltaDao.buscar_por_id(id_falta)

    def listar_por_barbeiro(self, id_barbeiro: int):
        return self.__faltaDao.consultar_todos_por_barbeiro(id_barbeiro)

    def atualizar(self, falta):
        return self.__faltaDao.atualizar(falta)

    def excluir(self, id_falta: int):
        return self.__faltaDao.excluir(id_falta)
