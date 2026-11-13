
from DAO.cliente_dao import ClienteDAO
from datetime import datetime


class ClienteRepositorio:

    def __init__(self):
        self.clienteDao = ClienteDAO()

    def salvar(self, id:int, dataUltimoServico:datetime | None):
        return self.clienteDao.cadastrar(id,dataUltimoServico)

   
    def consultarClienteId(self,id_cliente):
        return self.clienteDao.consultarClienteId(id_cliente)

    def loginClienteEmailSenha(self,email):
           return self.clienteDao.login_cliente_email(email)
       
       
    def consultar_clientes_services(self):
        return self.clienteDao.consultar_clientes_services()

    def buscar_cliente_id(self, id_cliente):
        return self.clienteDao.consultarClienteId(id_cliente)

   
    def atualizar(self,cliente):
        return self.clienteDao.atualizar(cliente)

   
    def atualizar_data_ultimo_servico(self,id_cliente, data):
        return self.clienteDao.atualizar_data_ultimo_servico(
            id_cliente, data
        )