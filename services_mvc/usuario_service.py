from flask import flash
from repositorio import UsuarioRepositorio
from .endereco_service import EnderecoService
from utilitarios import ValidadorDeImagens
from enums import EnumStatusMensagens
from models import Usuario
from sqlalchemy.exc import IntegrityError
from utilitarios import Senha

class UsuarioService:

    def __init__(self):
        self.__usuarioRepositorio = UsuarioRepositorio()

    def cadastrarUsuarioService(self, usuario: Usuario, fotoTemp:str):
        try:
            
            usuario.nomeVazioUsuario()
            usuario.senha = Senha.gerar_senha(usuario.senha)
            usuario.endereco = EnderecoService.cadastrar_endereco(usuario.endereco)
           
            usuario.foto_nome_usuario = ValidadorDeImagens.nomeImagem(fotoTemp, usuario.getTipo())   
        
            return self.__usuarioRepositorio.salvar(usuario) 

        except IntegrityError as i:
            raise Exception("ATENÇÃO: e-mail ou telefone já cadastrados no sistema") 
        
    
    def excluir_usuario_barbearia(self, id_usuario, foto_nome, nome_pasta):
                
        try:
            if self.__usuarioRepositorio.excluir(id_usuario):
                ValidadorDeImagens.excluir_imagem(foto_nome, nome_pasta)
                return
        except IntegrityError:
            raise
        
        
    def alterar_usuario_barbearia(self,  imagem_form, img_padrao, imagem_anterior, usuario):
                                                     
        usuario.foto_nome_usuario = ValidadorDeImagens.editarImagem(imagem_anterior,imagem_form,self.definir_pasta_imagem_usuario(), img_padrao, usuario.getTipo())
        
        if not usuario.senha.strip():
            if self.__usuarioRepositorio.atualizar_usuario_sem_senha(usuario):
                flash(f"As infomações do barbeiro {usuario.nome_completo} foi alterada com sucesso!",EnumStatusMensagens.SUCESSO.value)
                return True
            else:
                raise Exception()   
        else:
            usuario.senha = Senha.gerar_senha(usuario.senha.strip()) 
            if self.__usuarioRepositorio.atualizar_usuario_com_senha(usuario):
                flash(f"A senha e as infomaações do barbeiro {usuario.nome_completo} foi atualizada com sucesso!", EnumStatusMensagens.SUCESSO.value)
                return True
            else:
                raise Exception()
           
           
        
   
    def salvar_dados_especificos(self, usuario: Usuario): 
        raise NotImplementedError

    def definir_pasta_imagem_usuario(self):
        raise NotImplementedError
    
    def atualizar_endereco(self, endereco):
         EnderecoService.alterar_endereco(endereco) 
    
    def criarAgenda(self):
        raise NotImplementedError
    
    