
from DAO.agendamento_dao import AgendamentoDAO


class AgendamentoRepositorio:

    @staticmethod
    def salvar(agendamento):
        return AgendamentoDAO.salvar(agendamento)

    @staticmethod
    def buscar_por_id(id_agendamento):
        return AgendamentoDAO.buscar_por_id(id_agendamento)

    @staticmethod
    def consultar_agendamento_status_agendados(id_cliente):
        return AgendamentoDAO.consultar_todos_os_agendamento_do_cliente(id_cliente)

    @staticmethod
    def consultar_agendamento_por_dia(data_hoje):
        return AgendamentoDAO.consultar_todos_os_agendamento_do_dia(data_hoje)
   
    @staticmethod
    def consultar_total_agendamento_cancelado_por_dia(data_hoje):
        return AgendamentoDAO.consultar_total_agendamentos_cancelados(data_hoje)
    
    @staticmethod
    def consultar_media_mensal_agendamento(data_inicio, data_final):
        return AgendamentoDAO.consultar_media_agendamentos_mensal(data_inicio, data_final)

    @staticmethod
    def listar_por_cliente(id_cliente):
        return AgendamentoDAO.listar_por_cliente(id_cliente)

    @staticmethod
    def listar_por_barbeiro(id_barbeiro, data=None):
        return AgendamentoDAO.listar_por_barbeiro(
            id_barbeiro, data
        )

    @staticmethod
    def atualizar(agendamento):
        return AgendamentoDAO.atualizar(agendamento)

    @staticmethod
    def atualizar_status_e_motivo_do_cancelamento(motivo_cancelamento, status_agendamento,agenda_mensal):
        return AgendamentoDAO.atualizar_status_e_motivo_do_cancelamento_agenda_mensal(motivo_cancelamento, status_agendamento,agenda_mensal)

    @staticmethod
    def atualizar_status_e_motivo_do_cancelamento_faltas_justificadas(motivo_cancelamento, status_agendamento,falta_justificada):
        return AgendamentoDAO.atualizar_status_e_motivo_do_cancelamento_faltas_justificadas_dao(motivo_cancelamento, status_agendamento,falta_justificada)

    @staticmethod
    def consultar_agendamentos_por_periodo(data_inicio, data_fim):
        return AgendamentoDAO.consultar_agendamentos_por_periodo(data_inicio, data_fim)

    @staticmethod
    def cliente_tem_conflito_horario(id_cliente, data_agendamento, hora_inicio, hora_fim):
        return AgendamentoDAO.cliente_tem_conflito_horario(id_cliente, data_agendamento, hora_inicio, hora_fim)
   
    @staticmethod
    def consultar_total_agendamentos_por_periodo(data_inicio, data_final):
        return AgendamentoDAO.consultar_total_agendamentos_por_periodo(data_inicio, data_final)

    @staticmethod
    def excluir(id_agendamento):
        return AgendamentoDAO.excluir(id_agendamento)
    
    
