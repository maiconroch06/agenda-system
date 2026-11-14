from DAO.agendamento_servicos_dao import AgendamentoServicosDAO

class AgendamentoServicosRepositorio:

    @staticmethod
    def salvar(id_agendamento, id_servicos):
        return AgendamentoServicosDAO.salvar(id_agendamento, id_servicos)

    @staticmethod
    def consultar_dados_por_cliente(id_cliente):
        return AgendamentoServicosDAO.consultar_dados_por_cliente(id_cliente)