from models import Cliente
from flask import  session, redirect, url_for, flash, render_template
from models import Cliente, Agendamento
from database import db
from services_mvc import ClienteService, ServicoService, AgendaMensalService, BarbeariaService, BarbeiroService, AgendamentoService, AgendamentoServicosService
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
        self.__agendamentoServicosService = AgendamentoServicosService()
    
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
            return redirect(url_for('cliente.clientAgendamentoServicos'))

    def cadastrarAgendamento(self, agendamento: Agendamento, id_servicos, id_barbeiro):
        try:
            agendamento.barbeiro= self.__barbeiroService.buscar_barbeiro_id(id_barbeiro)
            id_agendamento = self.__agendamentoService.cadastrar_agendamento(agendamento)
            self.__agendamentoServicosService.salvar_agendamento_servicos(id_agendamento, id_servicos)

            print(f"Ids servicos: {id_servicos} id_agendamento: {id_agendamento}")
            flash(f"Agendamento feito com sucesso", EnumStatusMensagens.SUCESSO.value)
            return redirect(url_for('cliente.clientMeusAgendamentos'))

        except Exception as erros:
            flash(f"erros: {erros}", EnumStatusMensagens.ERRO.value)
            return redirect(url_for('cliente.clientLoginPage'))

    def meusAgendamentos(self, id_cliente):
        try:
            agendamentos = (
                self.__agendamentoServicosService
                .consultar_agendamentos_por_cliente(id_cliente)
            )

            print(agendamentos)

            total_proximos = sum(
                1 for item in agendamentos
                if item.agendamento.status_agendamento in (1, 2)
            )

            total_concluidos = sum(
                1 for item in agendamentos
                if item.agendamento.status_agendamento == 3
            )

            return render_template(
                'pages/cliente/cliente-meus-agendamentos.html',
                agendamentos=agendamentos,
                total_proximos=total_proximos,
                total_concluidos=total_concluidos
            )
            
        except Exception as erros:
            flash(f"{erros}", EnumStatusMensagens.ERRO.value)
            return redirect(url_for('cliente.clientLoginPage'))

   
    def consultar_todos_clientes(self):
        return self.__clienteService.consultar_clientes_services()
    
    def consultar_cliente_nome(self, nome_completo):
        return self.__clienteService.consultar_cliente_nome_services(nome_completo)
   
    def excluir_cliente(self, id_usuario, foto_nome, nome_pasta):
        return self.__clienteService.excluir_usuario_barbearia(id_usuario, foto_nome, nome_pasta)
    
    def atualziar_cliente(self, cliente):
            return self.__clienteService.alterar_usuario_barbearia(None, None,cliente.foto_nome_usuario,  cliente)
   