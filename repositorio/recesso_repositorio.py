
from DAO.recesso_dao import RecessoDAO


class RecessoRepositorio:

    def __init__(self):
        self.__recessoDao = RecessoDAO()

    def cadastrar_recesso(self, recesso, cnpj_barbearia):
        return self.__recessoDao.cadastrar_dao(recesso, cnpj_barbearia)
    
    def verificar_recesso_existente_cadastro(self, recesso):
        return self.__recessoDao.verificar_recesso_existente_cadastro(recesso)

    def consultar_por_mes(self):
        return self.__recessoDao.listar_por_mes()

    def consultar_todos(self):
        return self.__recessoDao.listar_todos()
   
    def consultar_recessos_intervalo_datas(self, data_inicio, data_final):
        return self.__recessoDao.consultar_recessos_por_intervalo_datas(data_inicio, data_final)
    
    def atualizar(self, recesso):
        return self.__recessoDao.atualizar(recesso)
    
    def verificar_recesso_intervalo_existente(self, recesso):
        return self.__recessoDao.verificar_recesso_intervalo_existente_dao(recesso)

    def excluir(self, id_recesso: int):
        return self.__recessoDao.excluir(id_recesso)