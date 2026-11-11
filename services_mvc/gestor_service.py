from repositorio import GestorRepositorio
from services_mvc.usuario_service import UsuarioService
from flask import flash, session
from utilitarios import Senha

class GestorServiceMVC(UsuarioService):

      def __init__(self):
          super().__init__()
          self.__gestor_repositorio = GestorRepositorio()  
          
      def gestor_realizar_login_service(self, email:str, senha:str):  
                
        if not email or not senha:
            raise Exception("Por favor, verifique se você preencheu todos os campos!")               
               
        gestor = self.__gestor_repositorio.realizar_login(email)
        
        if gestor is not None:        
            Senha.validar_senha(gestor['senha'], senha)    
            session.permanent = True 
            session['dados_gestor'] =  gestor  
            return  
        
        raise Exception("E-mail inexistente. Verifique o email e tente novamente!")
             
        
                  
        
                

     

      

      

    