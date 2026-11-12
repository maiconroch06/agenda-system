from models import AgendaMensal
from repositorio import AgendaMensalRepositorio
from DAO import BarbeariaDAO
from flask import flash

class AgendaMensalService:

    def __init__(self):
        self.__agenda_mensal_repositorio = AgendaMensalRepositorio()
       
  
    def cadastrar_agenda_mensal_service(self, nova_agenda_mensal, cnpj_barbearia):
        if self.__agenda_mensal_repositorio.verificar_aganda_aberta(nova_agenda_mensal) > 0:  
            flash(f"A agenda [ {nova_agenda_mensal.titulo_agenda} ] não foi criada. A data inicial deve ser maior que a data final da agenda cadastrada.")
            raise Exception()
        
        return self.__agenda_mensal_repositorio.salvar(nova_agenda_mensal,cnpj_barbearia)
    
    def consultar_agenda_mensal_service(self):
            return self.__agenda_mensal_repositorio.listar_todos()
        
    def atualizar_agenda_mensal_service(self, nova_agenda_mensal):
        if self.__agenda_mensal_repositorio.verificar_aganda_aberta(nova_agenda_mensal) > 0:  
            flash(f"A agenda [ {nova_agenda_mensal.titulo_agenda} ] não foi  atualizada. A data inicial deve ser maior que a data final da agenda cadastrada.")
            raise Exception()  
             
        return self.__agenda_mensal_repositorio.atualizar(nova_agenda_mensal)
    
    def excluir_agenda_mensal_service(self, id_agenda):
        return self.__agenda_mensal_repositorio.excluir(id_agenda)
            
            
    
            