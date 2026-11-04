from repository import ClienteRepository

class ClienteService:

      @staticmethod
      def cadastrarCliente(cliente, idUsuario):
        repositoryCliente = ClienteRepository()
        return repositoryCliente.salvar(cliente, idUsuario)