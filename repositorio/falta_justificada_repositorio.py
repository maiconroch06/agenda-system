
from DAO.falta_justificada_dao import FaltaJustificadaDao


class FaltaJustificadaRepositorio:

    @staticmethod
    def salvar(relacionamento):
        return FaltaJustificadaDao.salvar(relacionamento)

    @staticmethod
    def buscar_por_ids(id_servico, id_barbeiro):
        return FaltaJustificadaDao.buscar_por_ids(
            id_servico, id_barbeiro
        )

    @staticmethod
    def listar_todos():
        return FaltaJustificadaDao.listar_todos()

    @staticmethod
    def listar_por_barbeiro(id_barbeiro):
        return FaltaJustificadaDao.listar_por_barbeiro(
            id_barbeiro
        )

    @staticmethod
    def listar_por_servico(id_servico):
        return FaltaJustificadaDao.listar_por_servico(
            id_servico
        )

    @staticmethod
    def atualizar_data_cadastro(
        id_servico, id_barbeiro, data_cadastro
    ):
        return FaltaJustificadaDao.atualizar_data_cadastro(
            id_servico, id_barbeiro, data_cadastro
        )

    @staticmethod
    def excluir(id_servico, id_barbeiro):
        return FaltaJustificadaDao.excluir(
            id_servico, id_barbeiro
        )
