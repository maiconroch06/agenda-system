from repositorio import BarbeiroRepositorio
from .usuario_service import UsuarioService
from .horario_funcionamento_service import HorarioFuncionamentoService
from flask import flash, session
from werkzeug.security import check_password_hash
from sqlalchemy.exc import IntegrityError
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

    def consultar_barbeiros_ativos(self):
            try:
                barbeiros = self.__barbeiroRepositorio.listar_todos_ativos()
                return barbeiros
            except Exception as error:
                flash(f"Erro ao buscar os barbeiros cadastrados no banco {error}")

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
                

    def buscar_barbeiro_id(self, id_barbeiro):
        return self.__barbeiroRepositorio.buscar_por_id(id_barbeiro)

    # def validarDadosBarbeiro(self, barbeiro, fotoTemp):
    def definir_pasta_imagem_usuario(self):
        return EnumNomesPastaImagem.IMAGENS_BARBEIRO
            