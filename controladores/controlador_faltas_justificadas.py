from services_mvc import FaltasJustificadaBarbeiroService

class FaltasJustificadaBarbeiro:

    __faltas_justificadas = FaltasJustificadaBarbeiroService()
    
    @classmethod
    def cadastrar_falta_justificada_do_barbeiro(cls, id_barbeiro, falta_justificada):
            return cls.__faltas_justificadas.cadastrar_falta_justificada(id_barbeiro, falta_justificada)   
    
    @classmethod
    def excluir_falta_justificada_do_barbeiro(cls, id_falta_justificada):
            return cls.__faltas_justificadas.excluir(id_falta_justificada)   
    
    @classmethod
    def atualizar_falta_justificada_do_barbeiro(cls, falta_justificada):
            return cls.__faltas_justificadas.atualizar(falta_justificada)   
           
        
            

    