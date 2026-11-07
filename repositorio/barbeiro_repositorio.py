
from DAO.barbeiro_dao import BarbeiroDAO


class BarbeiroRepositorio:
    def __init__(self):
        self.__barbeiroDao = BarbeiroDAO()

    
    def salvar(self, barbeiro):
        return self.__barbeiroDao.cadastrar(barbeiro)

    
    def buscar_por_id(self, id_barbeiro):
        return self.__barbeiroDao.buscar_por_id(id_barbeiro)

    
    def listar_todos(self, ):
        return self.__barbeiroDao.consultar_todos()

    
    def atualizar(self, barbeiro):
        return self.__barbeiroDao.atualizar_barbeiro(barbeiro)

    
    def excluir(self, id_barbeiro):
        return self.__barbeiroDao.excluir_barbeiro(id_barbeiro)
