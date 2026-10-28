
from DAO.barbeiro_has_servicos_dao import BarbeiroHasServicosDAO


class BarbeiroHasServicosRepository:

    @staticmethod
    def salvar(relacionamento):
        return BarbeiroHasServicosDAO.salvar(relacionamento)

    @staticmethod
    def buscar_por_ids(id_servico, id_barbeiro):
        return BarbeiroHasServicosDAO.buscar_por_ids(
            id_servico, id_barbeiro
        )

    @staticmethod
    def listar_todos():
        return BarbeiroHasServicosDAO.listar_todos()

    @staticmethod
    def listar_por_barbeiro(id_barbeiro):
        return BarbeiroHasServicosDAO.listar_por_barbeiro(
            id_barbeiro
        )

    @staticmethod
    def listar_por_servico(id_servico):
        return BarbeiroHasServicosDAO.listar_por_servico(
            id_servico
        )

    @staticmethod
    def atualizar_data_cadastro(
        id_servico, id_barbeiro, data_cadastro
    ):
        return BarbeiroHasServicosDAO.atualizar_data_cadastro(
            id_servico, id_barbeiro, data_cadastro
        )

    @staticmethod
    def excluir(id_servico, id_barbeiro):
        return BarbeiroHasServicosDAO.excluir(
            id_servico, id_barbeiro
        )
