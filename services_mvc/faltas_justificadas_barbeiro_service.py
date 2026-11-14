
from repositorio import FaltaJustificadaBarbeiroRepositorio

class FaltasJustificadaBarbeiroService:

    def __init__(self):
        self.__falta_justificadas_barbeiro_repositorio = FaltaJustificadaBarbeiroRepositorio()
    
    def cadastrar_falta_justificada(self, id_barbeiro, falta_justificada):
        if self.__falta_justificadas_barbeiro_repositorio.verificar_falta_justificativa_existente_barbeiro(id_barbeiro,falta_justificada):
            return False
        
        return self.__falta_justificadas_barbeiro_repositorio.cadastrar_falta_justificada(id_barbeiro, falta_justificada)
    
    def buscar_por_id(self, id_falta: int):
        return self.__falta_justificadas_barbeiro_repositorio.buscar_por_id(id_falta)

    def listar_por_barbeiro(self, id_barbeiro: int):
        return self.__falta_justificadas_barbeiro_repositorio.consultar_todos_por_barbeiro(id_barbeiro)

    def atualizar(self, id_barbeiro,falta_justificada):
        if self.__falta_justificadas_barbeiro_repositorio.verificar_atualizacao_falta_justificativa_existente_barbeiro(id_barbeiro,falta_justificada):
            return False
        
        return self.__falta_justificadas_barbeiro_repositorio.atualizar(falta_justificada)

    def excluir(self, id_falta: int):
        return self.__falta_justificadas_barbeiro_repositorio.excluir(id_falta)