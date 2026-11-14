from DAO.falta_justificada_barbeiro_dao import FaltaJustificadaBarbeiroDAO

class FaltaJustificadaBarbeiroRepositorio:

    def __init__(self):
        self.__faltaDao = FaltaJustificadaBarbeiroDAO()

    def cadastrar_falta_justificada(self, id_barbeiro, falta_justificada):
        return self.__faltaDao.cadastrar(id_barbeiro, falta_justificada)

    def atualizar(self, falta):
        return self.__faltaDao.atualizar(falta)

    def excluir(self, id_falta: int):
        return self.__faltaDao.excluir(id_falta)