from repositorio import BarbeiroRepositorio
from .usuario_service import UsuarioService
from .agenda_service import AgendaService
from flask import flash, session
from werkzeug.security import check_password_hash
from utilitarios import Senha
from enums import EnumNomesPastaImagem
from database import db
from utilitarios import ValidadorDeImagens

class BarbeiroService(UsuarioService):

    def __init__(self):
        super().__init__()
        self.__barbeiroRepositorio = BarbeiroRepositorio()
        

    def consultar_barbeiros(self):
        try:
            barbeiros = self.__barbeiroRepositorio.listar_todos()
            return barbeiros
        except Exception as error:
            flash(f"Erro ao buscar os barbeiros cadastrados no banco {error}")

    # Mexer mais tarde para salvar os dados do barbeiro
    def salvar_dados_especificos(self, usuario, fotoTemp):
        try:
            
            agenda_service = AgendaService()
            
            usuario.agenda = agenda_service.cadastrar_agenda(usuario.nome_completo.split(" ")[0])
                        
            salvou_barbeiro = self.__barbeiroRepositorio.salvar(usuario)
            
            ValidadorDeImagens.salvarImagem(fotoTemp, self.escolherPastaImagemUsuario(), usuario.foto_nome)
            db.session.commit()
            
            return salvou_barbeiro
        
        except Exception as erros:
            db.session.rollback()
            flash(f"{erros}")
            raise Exception ("Não foi possivel cadastrar o Barbeiro")
        

    # def validarDadosBarbeiro(self, barbeiro, fotoTemp):
    def escolherPastaImagemUsuario(self):
        return EnumNomesPastaImagem.IMAGENS_BARBEIRO
            