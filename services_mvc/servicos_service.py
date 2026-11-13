from repositorio import ServicoRepositorio

class ServicoService():

    def __init__(self):
        self.__servico_repositorio = ServicoRepositorio()

    def consultar_todos_servicos(self):
        return self.__servico_repositorio.consultar_todos_servicos()

    def listar_servicos_ativos(self):
        return self.__servico_repositorio.listar_ativos()

    def buscar_servico_id(self, id_servico):
        return self.__servico_repositorio.buscar_por_id(id_servico)