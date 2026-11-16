from models import Recesso
from repositorio import RecessoRepositorio
from .barbearia_service import BarbeariaService
from flask import flash

class RecessoService:

    def __init__(self):
        self.__recesso_repositorio = RecessoRepositorio()
        
    def consultar_recessos_por_mes_services(self):
        return self.__recesso_repositorio.consultar_todos()
    
    def consultar_recessos_services(self):
        return self.__recesso_repositorio.consultar_todos()
  
    def cadastrar_recessos_services(self, recesso):
        if self.__recesso_repositorio.verificar_recesso_existente_cadastro(recesso)>0:
            flash(f"Não é possivel cadastras o recesso [ {recesso.descricao_recesso} ], pois ja existe um recesso com essa data")
            raise Exception()
        
        return self.__recesso_repositorio.cadastrar_recesso(recesso, BarbeariaService.consultar_cnpj_barbearia())
  
    def atualizar_recessos_services(self, recesso):
        if self.__recesso_repositorio.verificar_recesso_intervalo_existente(recesso)>0:
            flash(f"Não é possivel atualizar o recesso [ {recesso.descricao_recesso} ], pois ja existe um recesso com essa data")
            raise Exception()
        
        return self.__recesso_repositorio.atualizar(recesso)
  
    def excluir_recessos_services(self, id_recesso):
        return self.__recesso_repositorio.excluir(id_recesso)
  
  
  
  
  
  
  