from flask import flash
from repositorio import UsuarioRepositorio
from models import Usuario
from sqlalchemy.exc import IntegrityError
from enums import EnumStatusMensagens, EnumNomesPastaImagem
from services.validador_de_imagens import ValidadorDeImagens
from werkzeug.security import generate_password_hash

class UsuarioService:

    def __init__(self):
        self.usuarioRepositorio = UsuarioRepositorio()

    def cadastrarUsuarioService(self, usuario: Usuario, fotoTemp):
        try:

            usuario.nomeVazioUsuario()
            usuario.foto_nome = self.validarImagem(fotoTemp)
            usuario.senha = generate_password_hash(usuario.senha)
            return self.usuarioRepositorio.salvar(usuario) 

        except IntegrityError as i:
            flash( "ATENÇÃO: e-mail ou telefone já cadastrados no sistema" , EnumStatusMensagens.ERRO.value)
            raise 
        
        except Exception as erro:
            flash(str(erro), EnumStatusMensagens.ERRO.value)
            raise
        
  
    def salvar_dados_especificos(self, id_usuario): 
        raise NotImplementedError

    def validarImagem(self,fotoImagem):
        enviarImagem = ValidadorDeImagens()
        return enviarImagem.enviarImagem(fotoImagem, EnumNomesPastaImagem)
