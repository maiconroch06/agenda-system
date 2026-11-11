from repositorio import HorarioFuncionamentoRepositorio
from models import HorarioFuncionamento

class HorarioFuncionamentoService:
    
    def __init__(self):
        self.__agenda_repositorio = HorarioFuncionamentoRepositorio()
        
    def consultar_horario_funcionamento_barbearia(self, id_barbearia):
        return self.__agenda_repositorio.buscar_por_id(id_barbearia)
    
    def atualizar_horario_funcionamento_barbearia(self, novo_horario_funcionamento_barbearia):
        return self.__agenda_repositorio.atualizar_horario_funcionamento_repositorio(novo_horario_funcionamento_barbearia)
            