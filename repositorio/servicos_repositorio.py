from DAO.servicos_dao import ServicoDAO

class ServicoRepositorio:
    
    def __init__(self):
        self.servico_dao = ServicoDAO()

    def cadastrar_servico(self, servico):
        return self.servico_dao.cadastrar_servico(servico)
    
    def buscar_por_id(self, id_servico):
        return self.servico_dao.consultar_servico_id(id_servico)

    def consultar_todos_servicos(self):
        return self.servico_dao.consultar_todos_os_servicos()
    
    def consultar_todos_os_servicos_resumo(self):
        return self.servico_dao.consultar_todos_os_servicos_resumo()
    
    def listar_ativos(self):
        return self.servico_dao.consultar_servicos_status(1)

    def atualizar(self, servico):
        return self.servico_dao.atualizar(servico)

   
    def ativar(self, id_servico, data_atualizacao):
        return self.servico_dao.ativar(
            id_servico, data_atualizacao
        )

    def desativar(self, id_servico, data_atualizacao):
        return self.servico_dao.desativar(
            id_servico, data_atualizacao
        )

    def excluir(self, id_servico):
        return self.servico_dao.excluir(id_servico)
