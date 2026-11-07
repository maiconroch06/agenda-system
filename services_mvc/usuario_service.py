from flask import flash
from repositorio import UsuarioRepositorio
from .endereco_service import EnderecoService
from utilitarios import ValidadorDeImagens
from models import Usuario
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash

class UsuarioService:

    def __init__(self):
        self.usuarioRepositorio = UsuarioRepositorio()

    def cadastrarUsuarioService(self, usuario: Usuario, fotoTemp:str):
        try:
            
            
            
            usuario.nomeVazioUsuario()
            usuario.senha = generate_password_hash(usuario.senha)
            usuario.endereco = EnderecoService.cadastrar_endereco(usuario.endereco)
            
            
            #usuario.foto_nome = ValidadorDeImagens.salvarImagem(fotoTemp, self.escolherPastaImagemUsuario())
            usuario.foto_nome = ValidadorDeImagens.nomeImagem(fotoTemp, usuario.getTipo()) 
            flash("Passou aqui")           
            return self.usuarioRepositorio.salvar(usuario) 

        except IntegrityError as i:
            raise Exception("ATENÇÃO: e-mail ou telefone já cadastrados no sistema") 
        
    
        
   
    def salvar_dados_especificos(self, usuario: Usuario): 
        raise NotImplementedError

    def escolherPastaImagemUsuario(self):
        raise NotImplementedError
    
    def criarAgenda(self):
        raise NotImplementedError
    
    