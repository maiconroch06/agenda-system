
from DAO.endereco_dao import EnderecoDAO


class EnderecoRepository:

    @staticmethod
    def salvar(endereco):
        return EnderecoDAO.salvar(endereco)

    @staticmethod
    def buscar_por_id(id_endereco):
        return EnderecoDAO.buscar_por_id(id_endereco)

    @staticmethod
    def listar_todos():
        return EnderecoDAO.listar_todos()

    @staticmethod
    def buscar_por_cep(cep):
        return EnderecoDAO.buscar_por_cep(cep)

    @staticmethod
    def atualizar(endereco):
        return EnderecoDAO.atualizar(endereco)

    @staticmethod
    def excluir(id_endereco):
        return EnderecoDAO.excluir(id_endereco)
