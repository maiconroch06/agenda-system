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

    def consultar_agendamentos_barbeiro(self, barbeiro:dict):
        try:
            id_barbeiro = barbeiro.get('id_barbeiro', 0) # exibe 0 se chave não existir
            return self.__barbeiroRepositorio.listar_agendamentos_barbeiro(id_barbeiro)

        except Exception as error:
            print("\n ERRO NO SERVICE:", repr(error)) # <-- Vai mostrar o erro exato no terminal
            flash(f"\n # ERRO AO BUSCAR AGENDAMENTOS MARCADOS AO BARBEIRO '{barbeiro.get('nome_completo', 0)}' #\n {error}\n")
            return []
            
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
        return self.__barbeiroRepositorio.atualizar(usuario)            
                
         

    # def validarDadosBarbeiro(self, barbeiro, fotoTemp):
    def definir_pasta_imagem_usuario(self):
        return EnumNomesPastaImagem.IMAGENS_BARBEIRO
            