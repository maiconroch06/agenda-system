from repositorio import AgendamentoRepositorio
from models import Agendamento

class AgendamentoService:
    
    def __init__(self):
        self.__agendamento_repositorio = AgendamentoRepositorio()
        
        
    def consultar_agendamento_agendados(self, id_cliente): 
        return self.__agendamento_repositorio.consultar_agendamento_status_agendados(id_cliente)
    
    def consultar_agendamento_data_hoje(self, data_hoje): 
        return self.__agendamento_repositorio.consultar_agendamento_por_dia(data_hoje)
    
    def consultar_total_agendamento(self, data_inicio, data_final): 
        return self.__agendamento_repositorio.consultar_total_agendamentos_por_periodo(data_inicio, data_final)

    def cadastrar_agendamento(self, agendamento):
        return self.__agendamento_repositorio.salvar(agendamento)
        
    def atualizar_status_e_motivo_do_cancelamento_service(self, motivo_cancelamento, status_agendamento,agenda_mensal):
        return self.__agendamento_repositorio.atualizar_status_e_motivo_do_cancelamento(motivo_cancelamento, status_agendamento,agenda_mensal)
    
    def atualizar_status_cancelamento_faltas_justificadas_service(self, motivo_cancelamento, status_agendamento,falta_justificada):
        return self.__agendamento_repositorio.atualizar_status_e_motivo_do_cancelamento_faltas_justificadas(motivo_cancelamento, status_agendamento,falta_justificada)

    def consultar_agendamentos_por_periodo(self, data_inicio, data_fim):
        return self.__agendamento_repositorio.consultar_agendamentos_por_periodo(data_inicio, data_fim)

    def cliente_tem_conflito_horario(self, id_cliente, data_agendamento, hora_inicio, hora_fim):
        return self.__agendamento_repositorio.cliente_tem_conflito_horario(id_cliente, data_agendamento, hora_inicio, hora_fim)