
from DAO.agendamento_dao import AgendamentoDAO


class AgendamentoRepositorio:

    @staticmethod
    def salvar(agendamento):
        return AgendamentoDAO.salvar(agendamento)

    @staticmethod
    def buscarPorId(id_agendamento):
        return AgendamentoDAO.buscarPorIdDao(id_agendamento)

    @staticmethod
    def consultarAgendamentoStatusAgendados(id_cliente):
        return AgendamentoDAO.consultarTodosOsAgendamentoDoCliente(id_cliente)

    @staticmethod
    def consultarAgendamentoDataAtual(data_hoje):
        return AgendamentoDAO.consultarTodosOsAgendamentoDataAtual(data_hoje)
   
    @staticmethod
    def consultarTotalAgendamentoCanceladoPorDia(data_hoje):
        return AgendamentoDAO.consultarTotalAgendamentosCancelados(data_hoje)
    
    @staticmethod
    def consultarMediaMensalAgendamento(data_inicio, data_final):
        return AgendamentoDAO.consultarMediaMensalAgendamentoDao(data_inicio, data_final)

    @staticmethod
    def listarPorCliente(id_cliente):
        return AgendamentoDAO.listarPorClienteDao(id_cliente)

    @staticmethod
    def listarPorBarbeiro(id_barbeiro, data=None):
        return AgendamentoDAO.listarPorBarbeiro(
            id_barbeiro, data
        )

    @staticmethod
    def atualizar(agendamento):
        return AgendamentoDAO.atualizar(agendamento)

    @staticmethod
    def atualizarStatusMotivoDoCancelamentoAgendaMensal(motivo_cancelamento, status_agendamento,agenda_mensal):
        return AgendamentoDAO.atualizarStatusMotivoDoCancelamentoAgendaMensalDao(motivo_cancelamento, status_agendamento,agenda_mensal)
    
    @staticmethod
    def atualizarStatusAgendamentoUsuarios(id_agendamento, status_agendamento, motivo_cancelamento):
         return AgendamentoDAO.atualizarStatusagendamentoUsuarios(id_agendamento, status_agendamento,motivo_cancelamento)

    @staticmethod
    def atualizarStatusMotivoDoCancelamentoFaltasJustificadas(motivo_cancelamento, status_agendamento,falta_justificada):
        return AgendamentoDAO.atualizarStatusMotivoDoCancelamentoFaltasJustificadasDao(motivo_cancelamento, status_agendamento,falta_justificada)

    @staticmethod
    def consultarAgendamentosPorPeriodo(data_inicio, data_fim):
        return AgendamentoDAO.consultarAgendamentosPorPeriodoDAO(data_inicio, data_fim)

    @staticmethod
    def clienteTemConflitoHorario(id_cliente, data_agendamento, hora_inicio, hora_fim):
        return AgendamentoDAO.clienteTemConflitoHorarioDao(id_cliente, data_agendamento, hora_inicio, hora_fim)
   
    @staticmethod
    def consultarTotalAgendamentosPorPeriodo(data_inicio, data_final):
        return AgendamentoDAO.consultarTotalAgendamentosPorPeriodoDao(data_inicio, data_final)

    @staticmethod
    def excluir(id_agendamento):
        return AgendamentoDAO.excluirDao(id_agendamento)
    
    
