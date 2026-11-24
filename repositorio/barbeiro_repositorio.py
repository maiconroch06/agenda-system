
from DAO.barbeiro_dao import BarbeiroDAO


class BarbeiroRepositorio:
    
    def __init__(self):
        self.__barbeiroDao = BarbeiroDAO()
        
    def realizar_login(self, email):
        return self.__barbeiroDao.realizar_login_dao(email)
    
    def salvar(self, barbeiro):
        return self.__barbeiroDao.cadastrar(barbeiro)
    
    def buscar_por_id(self, id_barbeiro):
        return self.__barbeiroDao.buscar_por_id(id_barbeiro)
    
    def listar_todos(self):
        return self.__barbeiroDao.consultar_todos()
    
    def consultar_barbeiro_nome(self, nome_barbeiro):
        return self.__barbeiroDao.consultar_barbeiro_nome(nome_barbeiro)
    
    def consultar_nomes_barbeiro(self):
        return self.__barbeiroDao.consultar_nomes_barbeiro()
   
    def consultar_total_barbeiro_ativo(self):
        return self.__barbeiroDao.consultar_total_barbeiro_ativo()

    def listar_todos_ativos(self):
        return self.__barbeiroDao.consultar_todos_ativos()
    
    def atualizar(self, barbeiro):
        return self.__barbeiroDao.atualizar_informacoes_barbeiro(barbeiro)