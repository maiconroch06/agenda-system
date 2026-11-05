from flask import flash
from repositorio import UsuarioRepositorio
from models import Usuario
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash

class UsuarioService:

    def __init__(self):
        self.usuarioRepositorio = UsuarioRepositorio()

    def cadastrarUsuarioService(self, usuario: Usuario, fotoTemp):
        try:

            usuario.nomeVazioUsuario()
            usuario.foto_nome = ""
            usuario.senha = generate_password_hash(usuario.senha)
            return self.usuarioRepositorio.salvar(usuario) 

        except IntegrityError as i:
            raise Exception("ATENÇÃO: e-mail ou telefone já cadastrados no sistema")  
        
   
    def salvar_dados_especificos(self, id_usuario): 
        raise NotImplementedError

    
