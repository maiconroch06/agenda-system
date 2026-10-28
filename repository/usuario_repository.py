
from DAO.usuario_dao import UsuarioDAO


class UsuarioRepository:

    @staticmethod
    def salvar(usuario):
        return UsuarioDAO.salvar(usuario)

    @staticmethod
    def buscar_por_id(id_usuario):
        return UsuarioDAO.buscar_por_id(id_usuario)

    @staticmethod
    def buscar_por_email(email):
        return UsuarioDAO.buscar_por_email(email)

    @staticmethod
    def buscar_por_cpf(cpf):
        return UsuarioDAO.buscar_por_cpf(cpf)

    @staticmethod
    def listar_todos():
        return UsuarioDAO.listar_todos()

    @staticmethod
    def listar_ativos():
        return UsuarioDAO.listar_ativos()

    @staticmethod
    def atualizar(usuario):
        return UsuarioDAO.atualizar(usuario)

    @staticmethod
    def alterar_status(id_usuario, status):
        return UsuarioDAO.alterar_status(id_usuario, status)

    @staticmethod
    def excluir(id_usuario):
        return UsuarioDAO.excluir(id_usuario)

    @staticmethod
    def verificar_email_existente(email, id_ignorado=None):
        return UsuarioDAO.verificar_email_existente(
            email, id_ignorado
        )

    @staticmethod
    def verificar_cpf_existente(cpf, id_ignorado=None):
        return UsuarioDAO.verificar_cpf_existente(
            cpf, id_ignorado
        )
