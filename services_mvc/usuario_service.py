from flask import flash
from repositorio import UsuarioRepositorio
from .endereco_service import EnderecoService
from utilitarios import ValidadorDeImagens
from enums import EnumNomesPastaImagem
from models import Usuario
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash

class UsuarioService:

    def __init__(self):
        self.__usuarioRepositorio = UsuarioRepositorio()

    def cadastrarUsuarioService(self, usuario: Usuario, fotoTemp:str):
        try:
          
            usuario.nomeVazioUsuario()
            usuario.senha = generate_password_hash(usuario.senha)
            usuario.endereco = EnderecoService.cadastrar_endereco(usuario.endereco)
            
            #usuario.foto_nome = ValidadorDeImagens.salvarImagem(fotoTemp, self.escolherPastaImagemUsuario())
            usuario.foto_nome = ValidadorDeImagens.nomeImagem(fotoTemp, usuario.getTipo())            
            return self.__usuarioRepositorio.salvar(usuario) 

        except IntegrityError as i:
            raise Exception("ATENÇÃO: e-mail ou telefone já cadastrados no sistema") 
        
    
    def excluir_usuario_barbearia(self, id_usuario, foto_nome, nome_pasta):
                
        try:
            if self.__usuarioRepositorio.excluir(id_usuario):
                ValidadorDeImagens.removerImagem(foto_nome, nome_pasta)
                return
        except IntegrityError:
            raise
        
        
    def alterar_usuario_barbearia(self,  imagem_form, img_padrao, imagem_anterior, usuario):
                                                     
        usuario.foto_nome = ValidadorDeImagens.editarImagem(imagem_anterior,imagem_form,EnumNomesPastaImagem.IMAGEMS_SERVICOS, img_padrao, usuario.getTipo())
        
        if not self.__usuarioRepositorio.atualizar(usuario):
            raise Exception("Error ao tentar atualizar o usuario, tente novamente!")
           
        
   
    def salvar_dados_especificos(self, usuario: Usuario): 
        raise NotImplementedError

    def escolherPastaImagemUsuario(self):
        raise NotImplementedError
    
    def atualizar_endereco(self, endereco):
         EnderecoService.alterar_endereco(endereco) 
    
    def criarAgenda(self):
        raise NotImplementedError
    
    