from repositorio import BarbeiroRepositorio
from services_mvc.usuario_service import UsuarioService
from flask import flash, session
from werkzeug.security import check_password_hash
from utilitarios import Senha


class BarbeiroService(UsuarioService):

    def __init__(self):
        super().__init__
        self.barbeiroRepositorio = BarbeiroRepositorio()

    def consultar_barbeiros(self):
        try:
            barbeiros = self.barbeiroRepositorio.listar_todos()
            return barbeiros
        except Exception as error:
            flash(f"Erro ao buscar os barbeiros cadastrados no banco {error}")

    def cadastrarUsuarioService(self, usuario, fotoTemp):
        return super().cadastrarUsuarioService(usuario, fotoTemp)

    # Mexer mais tarde para salvar os dados do barbeiro
    def salvar_dados_especificos(self, id_usuario):
        return self.salvar_dados_especificos(id_usuario)

    # def validarDadosBarbeiro(self, barbeiro, fotoTemp):
        