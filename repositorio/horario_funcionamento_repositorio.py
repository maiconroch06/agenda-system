
from DAO import HorarioFuncionamentoDAO


class HorarioFuncionamentoRepositorio:

    def __init__(self):
        self.__horario_funcionamento_Dao = HorarioFuncionamentoDAO()

    def buscar_por_id(self, id_barbearia: int):
        return self.__horario_funcionamento_Dao.buscar_por_id(id_barbearia)
    
    def consutar_capacidade_total_servicos_dia(self):
        return self.__horario_funcionamento_Dao.consultar_capacidade_realizar_servicos_dia()

    def listar_todos(self, id_barbearia):
        return self.__horario_funcionamento_Dao.consultar_todos(id_barbearia)

    def atualizar_horario_funcionamento_repositorio(self, horario_funcionamento):
        return self.__horario_funcionamento_Dao.atualizar(horario_funcionamento)