
from repositorio import FaltaJustificadaBarbeiroRepositorio
from .agendamento_service import AgendamentoService
from enums import EnumStatusAgendamento

class FaltasJustificadaBarbeiroService:

    def __init__(self):
        self.__falta_justificadas_barbeiro_repositorio = FaltaJustificadaBarbeiroRepositorio()
        self.__agendamento_service = AgendamentoService()
    
    def cadastrar_falta_justificada(self, id_barbeiro, falta_justificada):
        
        if self.__falta_justificadas_barbeiro_repositorio.verificar_falta_justificativa_existente_barbeiro(id_barbeiro,falta_justificada):
            return False
        
        if self.__falta_justificadas_barbeiro_repositorio.cadastrar_falta_justificada(id_barbeiro, falta_justificada):
            motivo_cancelamento = "Motivo do cancelamento: " + falta_justificada.motivo_falta
            return self.__agendamento_service.atualizar_status_cancelamento_faltas_justificadas_service(motivo_cancelamento, EnumStatusAgendamento.CANCELADO.value, falta_justificada, id_barbeiro)
    
    def buscar_por_id(self, id_falta: int):
        return self.__falta_justificadas_barbeiro_repositorio.buscar_por_id(id_falta)

    def listar_por_barbeiro(self, id_barbeiro: int):
        return self.__falta_justificadas_barbeiro_repositorio.consultar_todos_por_barbeiro(id_barbeiro)

    def atualizar(self, id_barbeiro,falta_justificada):
        if self.__falta_justificadas_barbeiro_repositorio.verificar_atualizacao_falta_justificativa_existente_barbeiro(id_barbeiro,falta_justificada):
            return False
        
        if self.__falta_justificadas_barbeiro_repositorio.atualizar(falta_justificada):
            motivo_cancelamento = "Motivo do cancelamento: " + falta_justificada.motivo_falta
            return self.__agendamento_service.atualizar_status_cancelamento_faltas_justificadas_service(motivo_cancelamento, EnumStatusAgendamento.CANCELADO.value, falta_justificada, id_barbeiro)

    def consultar_faltas_por_periodo(self, data_inicio, data_fim):
        return self.__falta_justificadas_barbeiro_repositorio.consultar_faltas_por_periodo(data_inicio, data_fim)

    def excluir(self, id_barbeiro,falta_justificada):
        if self.__falta_justificadas_barbeiro_repositorio.excluir(falta_justificada.id_falta_justificada):
            return self.__agendamento_service.atualizar_status_cancelamento_faltas_justificadas_service(None, EnumStatusAgendamento.SERVICO_AGENDADO.value, falta_justificada, id_barbeiro)