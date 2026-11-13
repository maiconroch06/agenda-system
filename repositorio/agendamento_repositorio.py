
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
        return AgendamentoDAO.atualizar_status_e_motivo_do_cancelamento(motivo_cancelamento, status_agendamento,agenda_mensal)

    @staticmethod
    def excluir(id_agendamento):
        return AgendamentoDAO.excluir(id_agendamento)
