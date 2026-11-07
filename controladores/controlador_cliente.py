from models import Cliente
from flask import  session, redirect, url_for, flash
from models.cliente import Cliente
from database import db
from services_mvc import ClienteService
from enums import EnumStatusMensagens

class ControladorCliente():

    def __init__(self):
        self.clienteService = ClienteService()
    
    def login(self, email:str, senha:str):
        try:
            self.clienteService.realizarLoginService(email,senha)
            return redirect(url_for('cliente.clientAgendamentoServicos'))
       
        except Exception as erros:
           flash(f"{erros}", EnumStatusMensagens.ERRO.value) 
           return  redirect(url_for('cliente.clientLoginPage'))
              
    def cadastrarCliente(self, cliente:Cliente):      
        try:
            cliente.id  =  self.clienteService.cadastrarUsuarioService(cliente, cliente.foto_nome)
                     
            if self.clienteService.salvar_dados_especificos(cliente):                                      
                return redirect(url_for('cliente.cadastroSucesso'))
        
        except Exception as erros:
            flash(f"{erros}", EnumStatusMensagens.ERRO.value)
            return redirect(url_for('cliente.clientRegisterPage'))
        
   
    def consultar_todos_clientes(self):
        return self.clienteService.consultar_clientes_services()
   