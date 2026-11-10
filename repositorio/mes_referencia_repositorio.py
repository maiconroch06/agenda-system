from DAO.mes_referencia_dao import MesReferenciaDao


class MesReferenciaRepositorio:

    @staticmethod
    def salvar(horario):
        return MesReferenciaDao.salvar(horario)

    @staticmethod
    def buscar_por_id(id_horario):
        return MesReferenciaDao.buscar_por_id(id_horario)

    @staticmethod
    def listar_todos():
        return MesReferenciaDao.listar_todos()

    @staticmethod
    def listar_por_agenda(id_agenda):
        return MesReferenciaDao.listar_por_agenda(id_agenda)

    @staticmethod
    def atualizar(horario):
        return MesReferenciaDao.atualizar(horario)

    @staticmethod
    def excluir(id_horario):
        return MesReferenciaDao.excluir(id_horario)