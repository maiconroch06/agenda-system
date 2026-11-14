from repositorio import AgendamentoServicosRepositorio

class AgendamentoServicosService:

    def __init__(self):
        self.__agendamento_servicos_repository = AgendamentoServicosRepositorio()


    def salvar_agendamento_servicos(self, id_agendamento, id_servicos):
        return self.__agendamento_servicos_repository.salvar(id_agendamento, id_servicos)

    def consultar_agendamentos_por_cliente(self, id_cliente):
        return self.__agendamento_servicos_repository.consultar_dados_por_cliente(id_cliente)