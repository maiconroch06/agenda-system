from services_mvc import  ServicoBarbearia

class ControladorServico:
    __servicos_barbearia_service_mvc = ServicoBarbearia()
    
    @classmethod
    def consultar_servicos_resumido(cls):
        return cls.__servicos_barbearia_service_mvc.consultar_todos_servicos_resumo()
    
    
    @classmethod
    def consultar_todos_os_servicos(cls):
            return cls.__servicos_barbearia_service_mvc.consultar_todos_servicos()
            
    @classmethod
    def consultar_servico_nome(cls, nome_servico):
            return cls.__servicos_barbearia_service_mvc.consultar_servico_nome(nome_servico)
            