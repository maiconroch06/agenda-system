from repositorio import BarbeiroRepositorio
from .usuario_service import UsuarioService
from .horario_funcionamento_service import HorarioFuncionamentoService
from flask import flash, session
from werkzeug.security import check_password_hash
from sqlalchemy.exc import IntegrityError
from enums import EnumNomesPastaImagem
from database import db
from utilitarios import ValidadorDeImagens
from utilitarios import Senha
from datetime import datetime, date
import calendar

class BarbeiroService(UsuarioService):

    def __init__(self):
        super().__init__()
        self.__barbeiroRepositorio = BarbeiroRepositorio()
        
    def barbeiro_realizar_login_service(self, email:str, senha:str):  
        if not email or not senha:
            raise Exception("Por favor, verifique se você preencheu todos os campos!")               
                
        barbeiro = self.__barbeiroRepositorio.realizar_login(email)
        if barbeiro is not None:        
            Senha.validar_senha(barbeiro['senha'], senha)    
            session.permanent = True 
            session['dados_barbeiro'] = barbeiro  
            return  
        
        raise Exception("E-mail inexistente. Verifique o email e tente novamente!")
        
    def consultar_barbeiros(self):
        try:
            barbeiros = self.__barbeiroRepositorio.listar_todos()
            return barbeiros
        except Exception as error:
            flash(f"Erro ao buscar os barbeiros cadastrados no banco {error}")
    
    def consultar_barbeiro_nome(self, nome_barbeiro):
        try:
            barbeiros = self.__barbeiroRepositorio.consultar_barbeiro_nome(nome_barbeiro)
            return barbeiros
        except Exception as error:
            flash(f"Erro ao buscar os barbeiros cadastrados no banco {error}")

    def consultar_barbeiros_ativos(self):
            try:
                barbeiros = self.__barbeiroRepositorio.listar_todos_ativos()
                return barbeiros
            except Exception :
                flash(f"Erro ao buscar os barbeiros cadastrados no banco")
    
    def consultar_faltas_mensais_barbeiros_ativo(self):
            try:
                barbeiros = self.__barbeiroRepositorio.consultar_faltas_mensais_barbeiros_ativo(date.today().replace(day=1),date.today().replace(day=calendar.monthrange(date.today().year, date.today().month)[1]))
                return barbeiros
            except Exception:
                flash(f"Erro ao buscar os barbeiros cadastrados no banco, contate o suporte")
   
    def consultar_faltas_anuais_barbeiros_ativo(self):
            try:
                barbeiros = self.__barbeiroRepositorio.consultar_faltas_mensais_barbeiros_ativo(date.today().replace(day=1, month=1),date.today().replace(day=31, month=12))
                return barbeiros
            except Exception:
                flash(f"Erro ao buscar os barbeiros cadastrados no banco, contate o suporte")

    def consultar_agendamentos_barbeiro(self, barbeiro:dict):
        try:
            id_barbeiro = barbeiro.get('id_barbeiro', 0) # exibe 0 se chave não existir
            return self.__barbeiroRepositorio.listar_agendamentos_barbeiro(id_barbeiro)

        except Exception as error:
            print("\n ERRO NO SERVICE:", repr(error)) # <-- Vai mostrar o erro exato no terminal
            flash(f"\n # ERRO AO BUSCAR AGENDAMENTOS MARCADOS AO BARBEIRO '{barbeiro.get('nome_completo', 0)}")
            return []
        
    def consultar_faltas_por_barbeiro_ativo(self):
        return self.__barbeiroRepositorio.consultar_faltas_por_barbeiro_ativo()
        
            
    # Mexer mais tarde para salvar os dados do barbeiro
    def salvar_dados_especificos(self, usuario, fotoTemp):
        try:
                                  
            salvou_barbeiro = self.__barbeiroRepositorio.salvar(usuario)
            
            ValidadorDeImagens.salvarImagem(fotoTemp, self.definir_pasta_imagem_usuario(), usuario.foto_nome_usuario)
            db.session.commit()
            
            return salvou_barbeiro
        
        except Exception as erros:
            db.session.rollback()
            flash(f"{erros}")
            raise Exception ("Não foi possivel cadastrar o Barbeiro")
        
    def alterar_barbeiro_barbearia(self, usuario):
        status = self.__barbeiroRepositorio.atualizar(usuario)
        return status            
                

    def buscar_barbeiro_id(self, id_barbeiro):
        return self.__barbeiroRepositorio.buscar_por_id(id_barbeiro)
    
    def alterar_status_agendamento(self, id_agendamento:int, status_agendamento:int):
        try:
            data_hoje = datetime.today()
            data_hoje = data_hoje.strftime("%Y-%m-%d")
            
            return self.__barbeiroRepositorio.atualizar_status_agendamento(id_agendamento, status_agendamento, data_hoje)
        except Exception as erros: 
            print(f"\n ERRO NO SERVICE: {repr(erros)}\n\n") # <-- Vai mostrar o erro exato no terminal
            flash(f"\n\n # ERRO AO #\n {erros}\n\n")
            return 
    
    def alterar_status_agendamento(self, id_agendamento:int, status_agendamento:int, motivo_cancelamento):
        try:
            data_hoje = datetime.today()
            data_hoje = data_hoje.strftime("%Y-%m-%d")
            
            return self.__barbeiroRepositorio.atualizar_status_agendamento(id_agendamento, status_agendamento, data_hoje, motivo_cancelamento)
        except Exception as erros: 
            print(f"\n ERRO NO SERVICE: {repr(erros)}\n\n") # <-- Vai mostrar o erro exato no terminal
            flash(f"\n\n # ERRO AO #\n {erros}\n\n")
            return 
         

    # def validarDadosBarbeiro(self, barbeiro, fotoTemp):
    def definir_pasta_imagem_usuario(self):
        return EnumNomesPastaImagem.IMAGENS_BARBEIRO
    