
from DAO.usuario_dao import UsuarioDAO


class UsuarioRepositorio:
    
    def __init__(self):
        self.__usuarioDao = UsuarioDAO()
    
    def salvar(self, usuario):
        return self.__usuarioDao.cadastrar(usuario)
    
    def buscar_por_id(self,id_usuario):
        return self.__usuarioDao.buscar_por_id(id_usuario)

    def buscar_por_email(self, email):
        return self.__usuarioDao.buscar_por_email(email)

    def buscar_por_cpf(self, cpf):
        return self.__usuarioDao.buscar_por_cpf(cpf)

    def listar_todos(self):
        return self.__usuarioDao.consultar_todos_usuarios()

    def listar_ativos(self):
        return self.__usuarioDao.contultar_usuarios_ativos()
    
    def atualizar(self,usuario):
        return self.__usuarioDao.atualizar_usuarios_sem_senha(usuario)

    def alterar_status(self,id_usuario, status):
        return self.__usuarioDao.alterar_status(id_usuario, status)

    def excluir(self,id_usuario):
        return self.__usuarioDao.excluir(id_usuario)
    
    def verificar_email_existente(self,email, id_ignorado=None):
        return self.__usuarioDao.verificar_email_existente(
            email, id_ignorado
        )
    
    def verificar_cpf_existente(self,cpf, id_ignorado=None):
        return self.__usuarioDao.verificar_cpf_existente(
            cpf, id_ignorado
        )
