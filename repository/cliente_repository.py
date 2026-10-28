
from DAO.cliente_dao import ClienteDAO


class ClienteRepository:

    @staticmethod
    def salvar(cliente):
        return ClienteDAO.salvar(cliente)

    @staticmethod
    def buscar_por_id(id_cliente):
        return ClienteDAO.buscar_por_id(id_cliente)

    @staticmethod
    def listar_todos():
        return ClienteDAO.listar_todos()

    @staticmethod
    def atualizar(cliente):
        return ClienteDAO.atualizar(cliente)

    @staticmethod
    def atualizar_data_ultimo_servico(id_cliente, data):
        return ClienteDAO.atualizar_data_ultimo_servico(
            id_cliente, data
        )

    @staticmethod
    def excluir(id_cliente):
        return ClienteDAO.excluir(id_cliente)
