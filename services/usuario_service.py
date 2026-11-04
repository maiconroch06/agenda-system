from repository import UsuarioRepository

class UsuarioService:
    
    @staticmethod
    def cadastrarCliente(usuario):
        # validações precisam ser efetuadas aqui;
        repositoryUsuario = UsuarioRepository()
        return repositoryUsuario.salvar(usuario)