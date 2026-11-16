from services_mvc import AgendaMensalService,  BarbeariaService

class ControladorAgendaMensal():
    __agenda_mensal_service = AgendaMensalService()
    
    @classmethod
    def consultar_todas_agenda_mensal_service(cls):
        return cls.__agenda_mensal_service.consultar_agenda_mensal_service()
    
    @classmethod
    def cadastrar_agenda_mensal_service(cls, nova_agenda_mensal):
        return cls.__agenda_mensal_service.cadastrar_agenda_mensal_service(nova_agenda_mensal, BarbeariaService.consultar_cnpj_barbearia())

    @classmethod
    def atualizar_agenda_mensal_service(cls, nova_agenda_mensal):
        return cls.__agenda_mensal_service.atualizar_agenda_mensal_service(nova_agenda_mensal)
    
    @classmethod
    def excluir_agenda_mensal_service(cls, id_agenda_mensal):
        return cls.__agenda_mensal_service.cadastrar_agenda_mensal_service(id_agenda_mensal)
    @classmethod
    def excluir_agenda_mensal_service(cls, id_agenda_mensal):
        return cls.__agenda_mensal_service.cadastrar_agenda_mensal_service(id_agenda_mensal)
    
    @classmethod
    def atualizar_status_agenda_mensal_service(cls, agenda_mensal):
        return cls.__agenda_mensal_service.atualizar_status_agenda_mensal_service(agenda_mensal)