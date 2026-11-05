from repositorio import ClienteRepositorio
from services.usuario_service import UsuarioService
from flask import flash, session
from werkzeug.security import check_password_hash


class ClienteService(UsuarioService):

      def __init__(self):
          super().__init__()
          self.clienteRepositorio = ClienteRepositorio()
       
      def salvar_dados_especificos(self, id_usuario):
          try:
              self.clienteRepositorio.salvar(id_usuario, None)
              session.permanent = True
              session['dados_cliente'] =  self.clienteRepositorio.consultarClienteId(id_usuario)
          
          except Exception as error:
              flash(f"Erro o salvar o cliente {error}")

      def realizarLoginService(self, email, senha):
          try:
            
              if not email or not senha:
                raise Exception("Por favor, preencha todos os campos!")
                          
              session.permanent = True
              cliente = self.clienteRepositorio.loginClienteEmailSenha(email, senha)
                
              if  not check_password_hash(cliente['senha'], senha):
                  flash(f"Senha invalida, tente novamente!")
                  raise Exception()
                  
              session['dados_cliente'] =  cliente
          except Exception as error:
              flash(f"Erro ao consultar o cliente: {error}") 
              return       

     

      

      

    