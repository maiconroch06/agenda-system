from models import AgendaMensal
from repositorio import AgendaMensalRepositorio
from DAO import BarbeariaDAO
from .agendamento_service import AgendamentoService
from flask import flash
from enums import EnumStatusAgendamento

class AgendaMensalService:

    def __init__(self):
        self.__agenda_mensal_repositorio = AgendaMensalRepositorio()
        self.__agendamento_service = AgendamentoService()
       
  
    def cadastrar_agenda_mensal_service(self, nova_agenda_mensal, cnpj_barbearia):
        if self.__agenda_mensal_repositorio.verificar_aganda_aberta(nova_agenda_mensal) > 0:  
            flash(f"A agenda [ {nova_agenda_mensal.titulo_agenda} ] não foi criada. A data inicial deve ser maior que a data final da agenda cadastrada.")
            raise Exception()
        
        return self.__agenda_mensal_repositorio.salvar(nova_agenda_mensal,cnpj_barbearia)
    
    def consultar_agenda_mensal_service(self):
            return self.__agenda_mensal_repositorio.listar_todos()
        
    def atualizar_agenda_mensal_service(self, nova_agenda_mensal):
        if self.__agenda_mensal_repositorio.verificar_agenda_mensal_existente(nova_agenda_mensal) > 0:  
            flash(f"A agenda [ {nova_agenda_mensal.titulo_agenda} ] não foi  atualizada. A data inicial deve ser maior que a data final da agenda cadastrada.")
            raise Exception()  
             
        return self.__agenda_mensal_repositorio.atualizar(nova_agenda_mensal)
    
    
    def atualizar_status_agenda_mensal_service(self, nova_agenda_mensal:AgendaMensal): 
        motivo_cancelamento = None if nova_agenda_mensal.status_agenda_mensal else "Agendamento cancelado devido ao fechamento da agenda pelo gestor"
        
        if self.__agendamento_service.atualizar_status_e_motivo_do_cancelamento_service(motivo_cancelamento, EnumStatusAgendamento.SERVICO_AGENDADO.value if nova_agenda_mensal.status_agenda_mensal else EnumStatusAgendamento.CANCELADO.value, nova_agenda_mensal):
            if self.__agenda_mensal_repositorio.verificar_agenda_mensal_existente(nova_agenda_mensal) > 0:  
                flash(f"O status da agenda [ {nova_agenda_mensal.titulo_agenda} ] não foi  atualizada. A data inicial ou final ja estão sendo utilizadas em outras agendas.")
                raise Exception()
        else:
            flash(f"O status da agenda [ {nova_agenda_mensal.titulo_agenda} ] não foi  atualizada. problemas no agendamentos, consulte o suporte!")
            raise Exception()
                       
        return self.__agenda_mensal_repositorio.atualizar_status_agenda_mensal(nova_agenda_mensal)
    
    def excluir_agenda_mensal_service(self, id_agenda):
        return self.__agenda_mensal_repositorio.excluir(id_agenda)

    def verificar_agenda_mensal_atual(self, cnpj_barbearia):
        return self.__agenda_mensal_repositorio.verificar_mes_atual(cnpj_barbearia)

    def consultar_ultima_agenda_cadastrada(self, cnpj_barbearia):
        return self.__agenda_mensal_repositorio.consultar_ultima_agenda(cnpj_barbearia)
            
    
            