
from DAO.agendamento_dao import AgendamentoDAO


class AgendamentoRepository:

    @staticmethod
    def salvar(agendamento):
        return AgendamentoDAO.salvar(agendamento)

    @staticmethod
    def buscar_por_id(id_agendamento):
        return AgendamentoDAO.buscar_por_id(id_agendamento)

    @staticmethod
    def listar_todos():
        return AgendamentoDAO.listar_todos()

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
    def excluir(id_agendamento):
        return AgendamentoDAO.excluir(id_agendamento)
