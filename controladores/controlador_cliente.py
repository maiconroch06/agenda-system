from models import Cliente
from flask import  session, redirect, url_for, flash, render_template
from models import Cliente, Agendamento
from database import db
from services_mvc import ClienteService, ServicoService, AgendaMensalService, BarbeariaService, BarbeiroService, AgendamentoService
from enums import EnumStatusMensagens
from flask import jsonify

class ControladorCliente():

    def __init__(self):
        self.__clienteService = ClienteService()
        self.__servicosServices = ServicoService()
        self.__agendaMensalService = AgendaMensalService()
        self.__barbeariaService = BarbeariaService()
        self.__barbeiroService = BarbeiroService()
        self.__agendamentoService = AgendamentoService()
    
    def login(self, email:str, senha:str):
        try:
            self.__clienteService.realizarLoginService(email,senha)
            return redirect(url_for('cliente.clientAgendamentoServicos'))
       
        except Exception as erros:
           flash(f"{erros}", EnumStatusMensagens.ERRO.value) 
           return  redirect(url_for('cliente.clientLoginPage'))
              
    def cadastrarCliente(self, cliente:Cliente):      
        try:
            cliente.id  =  self.__clienteService.cadastrarUsuarioService(cliente, cliente.foto_nome_usuario)
               
            if cliente.id:     
                if self.__clienteService.salvar_dados_especificos(cliente):                                      
                    return redirect(url_for('cliente.cadastroSucesso'))
            else:
                flash(f"Erro ao cadastrar o cliente", EnumStatusMensagens.ERRO.value)
        except Exception as erros:
            flash(f"{erros}", EnumStatusMensagens.ERRO.value)
            return redirect(url_for('cliente.clientRegisterPage'))

    # Lembrar de buscar os dias de recesso da agenda caso seja o ultimo dia
    # Depois buscar os dias de faltas de cada barbeiro
    def gerenciarAgendamentoServico(self):
        try:
            cnpj_barbearia = self.__barbeariaService.consultar_cnpj_barbearia()
            agenda_mensal = self.__agendaMensalService.consultar_ultima_agenda_cadastrada(cnpj_barbearia)
            servicos = self.__servicosServices.listar_servicos_ativos()
            barbeiros = self.__barbeiroService.consultar_barbeiros_ativos()

            return render_template('pages/cliente/cliente-agendamento-rp.html', servicos=servicos, barbeiros=barbeiros, agenda_mensal=agenda_mensal)
        except Exception as erros:
            flash(f"{erros}", EnumStatusMensagens.ERRO.value)
            return redirect(url_for('cliente.clientLoginPage'))

    def cadastrarAgendamento(self, agendamento: Agendamento, id_servico, id_barbeiro):
        try:
            agendamento.servico= self.__servicosServices.buscar_servico_id(id_servico)
            agendamento.barbeiro= self.__barbeiroService.buscar_barbeiro_id(id_barbeiro)
            self.__agendamentoService.cadastrar_agendamento(agendamento)

            return redirect(url_for('cliente.clientMeusAgendamentos'))

        except Exception as erros:
            flash(f"erros: {erros}")

    def meusAgendamentos(self, id_cliente):
        try:
            return render_template('pages/cliente/cliente-meus-agendamentos.html', agendamentos = self.__agendamentoService.consultar_agendamento_agendados(id_cliente))
            
        except Exception as erros:
                    flash(f"{erros}", EnumStatusMensagens.ERRO.value)
                    return  redirect(url_for('cliente.clientLoginPage'))

   
    def consultar_todos_clientes(self):
        return self.__clienteService.consultar_clientes_services()
   