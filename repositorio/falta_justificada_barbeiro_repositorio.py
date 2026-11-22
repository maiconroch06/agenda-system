from DAO.falta_justificada_barbeiro_dao import FaltaJustificadaBarbeiroDAO

class FaltaJustificadaBarbeiroRepositorio:

    def __init__(self):
        self.__faltaDao = FaltaJustificadaBarbeiroDAO()

    def cadastrar_falta_justificada(self,  falta_justificada):
        return self.__faltaDao.cadastrar( falta_justificada)

    def atualizar(self, falta):
        return self.__faltaDao.atualizar(falta)

    def excluir(self, id_falta: int):
        return self.__faltaDao.excluir(id_falta)

    def verificar_falta_justificativa_existente_barbeiro(self,  falta_justificada):
        return self.__faltaDao.verificar_falta_justificativa_existente_barbeiro_dao( falta_justificada)

    def verificar_atualizacao_falta_justificativa_existente_barbeiro(self, falta_justificada):
        return self.__faltaDao.verificar_atualizacao_falta_justificativa_existente_barbeiro_dao( falta_justificada)
    
    def consultar_faltas_por_barbeiro_ativo(self):
        return self.__faltaDao.consultar_faltas_dos_barbeiros_ativo()
        
    def consultar_faltas_barbeiros_ativo_periodo(self, data_inicio_mes, data_final_mes):
        return self.__faltaDao.consultar_faltas_barbeiros_ativo_periodo( data_inicio_mes, data_final_mes)
    
    def consultar_faltas_por_periodo(self,data_inicio, data_fim):
        return self.__faltaDao.consultar_faltas_por_periodo(data_inicio, data_fim)
