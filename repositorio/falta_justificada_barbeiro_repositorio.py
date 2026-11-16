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

    def verificar_falta_justificativa_existente_barbeiro(self, id_barbeiro, falta_justificada):
        return self.__faltaDao.verificar_falta_justificativa_existente_barbeiro_dao(id_barbeiro, falta_justificada)

    def verificar_atualizacao_falta_justificativa_existente_barbeiro(self, id_barbeiro, falta_justificada):
        return self.__faltaDao.verificar_atualizacao_falta_justificativa_existente_barbeiro_dao(id_barbeiro, falta_justificada)