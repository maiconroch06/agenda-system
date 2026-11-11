from services_mvc import HorarioFuncionamentoService

class ControladorHorarioFuncionamento():
    __horario_funcionamento = HorarioFuncionamentoService()
    
    @classmethod
    def consultar_horario_funcionamento(cls, id_barbearia):
        return cls.__horario_funcionamento.consultar_horario_funcionamento_barbearia(id_barbearia)
    
    
    @classmethod
    def atualizar_horario_funcionamento(cls, horario_funcionamento_barbearia):
        return cls.__horario_funcionamento.atualizar_horario_funcionamento_barbearia(horario_funcionamento_barbearia)
        