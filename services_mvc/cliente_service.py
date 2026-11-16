from repositorio import ClienteRepositorio
from services_mvc.usuario_service import UsuarioService
from flask import flash, session
from werkzeug.security import check_password_hash
from utilitarios import Senha
from enums import EnumNomesPastaImagem
from database import db

class ClienteService(UsuarioService):

    def __init__(self):
        super().__init__()
        self.__clienteRepositorio = ClienteRepositorio()
       
    def salvar_dados_especificos(self, usuario):
        try:
            resposta_repositorio = self.__clienteRepositorio.salvar(usuario.id, None)
            
            session.permanent = True
            session['dados_cliente'] =  self.__clienteRepositorio.consultarClienteId(usuario.id)
            
            db.session.commit()
            print(str(resposta_repositorio))
            return resposta_repositorio
            
        except Exception as error:
            flash(f"Erro o salvar o cliente {error}")

    def realizarLoginService(self, email, senha):
        if not email or not senha:
            raise Exception("Por favor, preencha todos os campos!")
                        
            
        cliente = self.__clienteRepositorio.loginClienteEmailSenha(email)
            
        if cliente is not None:                 
            Senha.validar_senha(cliente['senha'], senha)
            session.permanent = True
            session['dados_cliente'] =  cliente
            return

        raise Exception("E-mail inexistente. Verifique o email e tente novamente!")

    def buscar_cliente_id(self, id_cliente):
        try:
            return self.__clienteRepositorio.consultarClienteId(id_cliente)
        except Exception as error:
                    flash(f"Erro ao buscar o cliente por id {error}")

    def definir_pasta_imagem_usuario(self):
            return EnumNomesPastaImagem.IMAGENS_CLIENTE

    def consultar_clientes_services(self):
           return self.__clienteRepositorio.consultar_clientes_services()  

      

      

    