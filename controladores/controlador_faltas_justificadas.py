from services_mvc import FaltasJustificadaBarbeiroService

class FaltasJustificadaBarbeiro:
        __faltas_justificadas = FaltasJustificadaBarbeiroService()
        
        @classmethod
        def cadastrar_falta_justificada_barbeiro(cls, falta_justificada):
                return cls.__faltas_justificadas.cadastrar_falta_justificada( falta_justificada)   
        
        @classmethod
        def excluir_falta_justificada_barbeiro(cls, id_falta_justificada):
                return cls.__faltas_justificadas.excluir( id_falta_justificada)   
        
        @classmethod
        def atualizar_falta_justificada_barbeiro(cls, falta_justificada):
                return cls.__faltas_justificadas.atualizar( falta_justificada)   
        
        @classmethod
        def consultar_falta_justidicada_barbeiro(cls):
                return cls.__faltas_justificadas.consultar_faltas_justificadas_barbeiro() 
           
        @classmethod
        def consultar_falta_justidicada_barbeiro_mensal(cls):
                return cls.__faltas_justificadas.consultar_faltas_mensais_barbeiros_ativo() 
            
        @classmethod
        def consultar_falta_justidicada_barbeiro_anual(cls):
                return cls.__faltas_justificadas.consultar_faltas_anuais_barbeiros_ativo() 
    