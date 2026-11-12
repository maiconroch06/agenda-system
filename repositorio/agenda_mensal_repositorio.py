
from DAO.agenda_mensal_dao import AgendaMensalDAO


class AgendaMensalRepositorio:

    def __init__(self):
        self.__aganda_mensal_DAO = AgendaMensalDAO()

    def salvar(self, nova_agenda_mensal, cnpj_barbearia):
        return self.__aganda_mensal_DAO.cadastrar(nova_agenda_mensal, cnpj_barbearia)
    
    def verificar_aganda_aberta(self, nova_agenda_mensal):
        return self.__aganda_mensal_DAO.verificar_aganda_aberta(nova_agenda_mensal)

    def buscar_por_id(self, id_mes: int):
        return self.__aganda_mensal_DAO.buscar_por_id(id_mes)

    def listar_por_agenda(self, id_agenda: int):
        return self.__aganda_mensal_DAO.listar_por_agenda(id_agenda)

    def listar_todos(self):
        return self.__aganda_mensal_DAO.listar_todos()

    def atualizar(self, nova_agenda_mensal):
        return self.__aganda_mensal_DAO.atualizar(nova_agenda_mensal)

    def excluir(self, id_mes: int):
        return self.__aganda_mensal_DAO.excluir(id_mes)