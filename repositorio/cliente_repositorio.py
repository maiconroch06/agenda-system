
from DAO.cliente_dao import ClienteDAO
from datetime import datetime


class ClienteRepositorio:

    def __init__(self):
        self.clienteDao = ClienteDAO()

    def salvar(self, id:int, dataUltimoServico:datetime | None):
        return self.clienteDao.salvar(id,dataUltimoServico)

   
    def consultarClienteId(self,id_cliente):
        return self.clienteDao.consultarClienteId(id_cliente)

    def loginClienteEmailSenha(self,email):
           return self.clienteDao.loginClienteEmailSenha(email)
       
       
    def listar_todos(self):
        return self.clienteDao.listar_todos()

   
    def atualizar(self,cliente):
        return self.clienteDao.atualizar(cliente)

   
    def atualizar_data_ultimo_servico(self,id_cliente, data):
        return self.clienteDao.atualizar_data_ultimo_servico(
            id_cliente, data
        )

    
    def excluir(self,id_cliente):
        return self.clienteDao.excluir(id_cliente)
