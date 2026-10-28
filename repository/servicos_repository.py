
from DAO.servicos_dao import ServicoDAO


class ServicoRepository:

    @staticmethod
    def salvar(servico):
        return ServicoDAO.salvar(servico)

    @staticmethod
    def buscar_por_id(id_servico):
        return ServicoDAO.buscar_por_id(id_servico)

    @staticmethod
    def listar_todos():
        return ServicoDAO.listar_todos()

    @staticmethod
    def listar_ativos():
        return ServicoDAO.listar_ativos()

    @staticmethod
    def atualizar(servico):
        return ServicoDAO.atualizar(servico)

    @staticmethod
    def ativar(id_servico, data_atualizacao):
        return ServicoDAO.ativar(
            id_servico, data_atualizacao
        )

    @staticmethod
    def desativar(id_servico, data_atualizacao):
        return ServicoDAO.desativar(
            id_servico, data_atualizacao
        )

    @staticmethod
    def excluir(id_servico):
        return ServicoDAO.excluir(id_servico)
