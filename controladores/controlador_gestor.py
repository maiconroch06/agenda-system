from calendar import c

from flask import session, redirect, url_for, flash, render_template
from werkzeug.security import check_password_hash
from database import db
from enums import EnumStatusMensagens, EnumNomesPastaImagem
from services_mvc import GestorServiceMVC, BarbeiroService
from models import Barbeiro
from werkzeug.utils import secure_filename
from .controlador_cliente import ControladorCliente
from .controlador_agendamento import ControladorAgendamento
from .controlador_barbeiro import ControladorBarbeiro
from .controlador_servicos import ControladorServico
from .Controlador_horarios_funcionamento import ControladorHorarioFuncionamento
from .controlador_agenda_mensal import ControladorAgendaMensal


class ControladorGestor():
    __gestor_service_mvc = GestorServiceMVC()
    __barbeiro_service_mvc = BarbeiroService()
    __controlador_cliente = ControladorCliente()
    __controlador_barbeiro = ControladorBarbeiro()
    __controlador_agendamento = ControladorAgendamento()
 
    @classmethod
    def login_gestor(cls, email:str, senha:str):
        try:
            cls.__gestor_service_mvc.gestor_realizar_login_service(email,senha)
            if cls.__gestor_service_mvc.atualizarUltimoAcesso(session.get('dados_gestor',{}).get("id_usuario")):
                return redirect(url_for('gestor.gestorPainel'))
        
        except Exception as error:
            flash(f"{error}")
            return  redirect(url_for('gestor.gestorLoginPagina'))

    @classmethod
    def cadastrarBarbeiro(cls, barbeiro: Barbeiro, fotoTemp):
        try:
            barbeiro.id_usuario = cls.__barbeiro_service_mvc.cadastrarUsuarioService(barbeiro,secure_filename(fotoTemp.filename))        
            if cls.__barbeiro_service_mvc.salvar_dados_especificos(barbeiro, fotoTemp):  
                flash(f"Barbeiro {barbeiro.nome_completo.split(' ')[0]} cadastrado com sucesso.", EnumStatusMensagens.SUCESSO.value)  
                return redirect(url_for('gestor.gestorAbaBarbeiros'))
            
        except Exception as erros:
            flash(f"{erros}", EnumStatusMensagens.ERRO.value)
            
        return redirect(url_for('gestor.gestorBarbeiroPage'))
    
    
    @classmethod
    def excluir_barbeiro(cls, id_barbeiro, foto_nome):
            try:
                cls.__barbeiro_service_mvc.excluir_usuario_barbearia(id_barbeiro,foto_nome,EnumNomesPastaImagem.IMAGENS_BARBEIRO)   
                flash(f"O barbeiro foi excluído com sucesso!",EnumStatusMensagens.SUCESSO.value)
            except Exception:
                flash(f"O barbeiro não foi excluido!", EnumStatusMensagens.ERRO.value)
                
            return redirect(url_for('gestor.gestorAbaBarbeiros'))  
    
    @classmethod
    def atualizar_barbeiro(cls, imagem_form, img_padrao, imagem_anterior, barbeiro):
        try:                            
            if not cls.__controlador_barbeiro.atualizar_informacoes_barbeiro(imagem_form, img_padrao, imagem_anterior, barbeiro):
                    flash(f"Erro ao atualizar o barbeiro", EnumStatusMensagens.ERRO.value)      
        except Exception:
            flash(f"Nenhuma informação do babeiro foi atualizada.", EnumStatusMensagens.ERRO.value)
            
        return redirect(url_for('gestor.gestorAbaBarbeiros'))

    @classmethod
    def consultar_clientes(cls):
        return render_template('pages/gestor/gestor-painel-clientes-rp.html', lista_clientes= cls.__controlador_cliente.consultar_todos_clientes(), modo=0, mensagens_status=EnumStatusMensagens)
   
    @classmethod
    def consultar_cliente_nome(cls,nome_cliente):
        return render_template('pages/gestor/gestor-painel-clientes-rp.html',nome_cliente=nome_cliente, lista_clientes= cls.__controlador_cliente.consultar_cliente_nome(nome_cliente), modo=1, mensagens_status=EnumStatusMensagens)

    @classmethod
    def consultar_agendamentos(cls, status_agendamento):
        return render_template('pages/gestor/gestor-painel-inicio-rp.html', agendamentos = cls.__controlador_agendamento.consultar_agendamento(status_agendamento)) 
    
    @classmethod
    def consultar_agendamentos_data_hoje(cls, data_hoje):
        return render_template('pages/gestor/gestor-painel-inicio-rp.html', agendamentos_flask = cls.__controlador_agendamento.consultar_agendamento_dia(data_hoje),
                               total_cancelados = cls.__controlador_agendamento.consultar_total_agendamento_cancelado_por_dia(data_hoje),
                               ticket_medio_mensal=ControladorAgendamento.consultar_valor_ticket_medio_mensal_agendamento(), capacidade_atendimento=ControladorHorarioFuncionamento.consultar_capacidade_realizar_servicos_dia()) 
        
    @classmethod
    def consultar_horario_funcionamento(cls, id_barbearia):
        return ControladorHorarioFuncionamento.consultar_horario_funcionamento(id_barbearia)
   
    @classmethod
    def atualizar_horario_funcionamento_barbearia(cls, horario_funcionamento_barbearia):
            
            try:
                ControladorHorarioFuncionamento.atualizar_horario_funcionamento(horario_funcionamento_barbearia)
                flash("Horario de funcionmento da barbearia atualizado com sucesso", EnumStatusMensagens.SUCESSO.value)
            except Exception :
                flash(f"Erro ao tentar atualizar o horario de funcionmento da barbearia", EnumStatusMensagens.ERRO.value)
            
            return redirect(url_for("gestor.gestor_horario_funcionamento_barbearia"))

    @classmethod
    def excluir_cliente_barbearia(cls,  id_usuario, foto_nome, nome_cliente):
        try:
            if  cls.__controlador_cliente.excluir_cliente(id_usuario,foto_nome,EnumNomesPastaImagem.IMAGENS_CLIENTE):
                flash(f"Cliente [ {nome_cliente} ] excluido com sucesso", EnumStatusMensagens.SUCESSO.value)
        except Exception:
            flash(f"Erro ao tentar excluir o cliente [ {nome_cliente} ] da barbearia", EnumStatusMensagens.ERRO.value)

        return redirect(url_for("gestor.gestorExibirClientes"))

    @classmethod
    def atualizar_cliente_barbearia(cls, cliente):
        try:
            if  cls.__controlador_cliente.atualizar_cliente(cliente):
                db.session.commit()
                flash(f"Cliente [ {cliente.nome_completo} ] atualizado com sucesso", EnumStatusMensagens.SUCESSO.value)
        except Exception:
            flash(f"Erro ao tentar atualizar o cliente [ {cliente.nome_completo} ] da barbearia", EnumStatusMensagens.ERRO.value)

        return redirect(url_for("gestor.gestorExibirClientes"))
    
   
    
    
           