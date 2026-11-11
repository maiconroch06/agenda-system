from models import AgendaMensal
from repositorio import AgendaMensalRepositorio
from DAO import BarbeariaDAO

class AgendaMensalService:

    def __init__(self):
        self.__agenda_mensal_repositorio = AgendaMensalRepositorio()
       
  
    def cadastrar_agenda_mensal_service(self, nova_agenda_mensal, cnpj_barbearia):
        return self.__agenda_mensal_repositorio.salvar(nova_agenda_mensal,cnpj_barbearia)
    
    def consultar_agenda_mensal_service(self):
            return self.__agenda_mensal_repositorio.listar_todos()
        
    def atualizar_agenda_mensal_service(self, nova_agenda_mensal):
        return self.__agenda_mensal_repositorio.atualizar(nova_agenda_mensal)
    
    def excluir_agenda_mensal_service(self, id_agenda):
        return self.__agenda_mensal_repositorio.excluir(id_agenda)
            
            
    
            