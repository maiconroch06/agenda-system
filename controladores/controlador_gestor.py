from flask import session, redirect, url_for, flash, render_template
from sqlalchemy.exc import IntegrityError
from werkzeug.security import check_password_hash
from database import db
from enums import EnumStatusMensagens, EnumNomesPastaImagem
from services_mvc import GestorServiceMVC, ServicoBarbearia, BarbeiroService
from execoes import ImagemErrorExcecao 
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
    __servicos_barbearia_service_mvc = ServicoBarbearia()
    __barbeiro_service_mvc = BarbeiroService()
    __controlador_cliente = ControladorCliente()
    __controlador_barbeiro = ControladorBarbeiro()
    __controlador_agendamento = ControladorAgendamento()
 
    @classmethod
    def login_gestor(cls, email:str, senha:str):
        try:
            cls.__gestor_service_mvc.gestor_realizar_login_service(email,senha)   
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
                if cls.__controlador_barbeiro.atualizar_informacoes_barbeiro(imagem_form, img_padrao, imagem_anterior, barbeiro):   
                    flash(f"As infomações do barbeiro {barbeiro.nome_completo} foi alterada com sucesso!",EnumStatusMensagens.SUCESSO.value)
            except Exception:
                flash(f"Nenhuma informação do babeiro foi feita!", EnumStatusMensagens.ERRO.value)
                
            return redirect(url_for('gestor.gestorAbaBarbeiros'))  

    @classmethod
    def cadastrarServico(cls, foto, novo_descricao: str, novo_valor: str, novo_duracao:str ):
        
        try:
            if cls.__servicos_barbearia_service_mvc.cadastrar_servico_barbearia(foto, novo_descricao, novo_valor, novo_duracao):
                return redirect(url_for('gestor.gestorAbaServicos'))
        
        except ImagemErrorExcecao as erros:
            flash(f"{erros}", EnumStatusMensagens.AVISO.value)
            return redirect(url_for('gestor.gestorAbaServicos'))
        
        except Exception as erros:
            flash(f"{erros}", EnumStatusMensagens.ERRO.value)
            return redirect(url_for('gestor.gestorAbaServicos'))
             
    @classmethod
    def excluir_servico(cls, id_servico, foto_nome):
        try:
            cls.__servicos_barbearia_service_mvc.excluir_servico_barbearia(id_servico,foto_nome ) 
            flash(f"O servico foi excluido com sucesso!", EnumStatusMensagens.SUCESSO.value)  
        except Exception as error:
            flash(f"{error}", EnumStatusMensagens.ERRO.value)
            
        return redirect(url_for('gestor.gestorAbaServicos'))  
           
    @classmethod
    def editarServico(cls, id, imagem_form, img_padrao, imagem_anterior, descricao_servico, valor, duracao, ativo):
       
        try:
         
            cls.__servicos_barbearia_service_mvc.editar_servico_barbearia(id, imagem_form, img_padrao, imagem_anterior, descricao_servico, valor, duracao, ativo)
            flash(f"Servico {descricao_servico} atualizado com sucesso.", EnumStatusMensagens.SUCESSO.value)
        except Exception as erros:
           print(f"erro ao tentar atualizar a agenda: {erros}")       
        
        return redirect(url_for("gestor.gestorAbaServicos")) 
             
            
    @classmethod
    def consultar_servicos(cls):
            return render_template('pages/gestor/gestor-painel-servicos-rp.html', listaServicos = ControladorServico.consultar_todos_os_servicos(), mensagens_status=EnumStatusMensagens)
   
    @classmethod
    def consultar_clientes(cls):
        return render_template('pages/gestor/gestor-painel-clientes-rp.html', lista_clientes= cls.__controlador_cliente.consultar_todos_clientes(),  mensagens_status=EnumStatusMensagens)

    @classmethod
    def consultar_agendamentos(cls, status_agendamento):
        return render_template('pages/gestor/gestor-painel-inicio-rp.html', agendamentos = cls.__controlador_agendamento.consultar_agendamento(status_agendamento)) 
    
    
    @classmethod
    def consultar_horario_funcionamento(cls, id_barbearia):
        return ControladorHorarioFuncionamento.consultar_horario_funcionamento(id_barbearia)
    
    @classmethod
    def atualizar_horario_funcionamento_barbearia(cls, horario_funcionamento_barbearia):
            
            try:
                ControladorHorarioFuncionamento.atualizar_horario_funcionamento(horario_funcionamento_barbearia)
                flash("Horario de funcionmento da barbearia atualziado com sucesso", EnumStatusMensagens.SUCESSO.value)
            except Exception :
                flash(f"Erro ao tentar atualizar o horario de funcionmento da barbearia", EnumStatusMensagens.ERRO.value)
            
            return redirect(url_for("gestor.gestor_horario_funcionamento_barbearia"))   
        
    @classmethod
    def cadastrar_agenda_mensal_barbearia(cls, agenda_barbearia):        
        try:
            ControladorAgendaMensal.cadastrar_agenda_mensal_service(agenda_barbearia)
            flash("Agenda da barbearia cadastrada com sucesso", EnumStatusMensagens.SUCESSO.value)
        except Exception as erros:
            print(f"Erro ao tentar cadastrar a agenda da barbearia", EnumStatusMensagens.ERRO.value)
        
        return redirect(url_for("gestor.gestor_horario_funcionamento_barbearia"))       
     
    @classmethod
    def atualizar_agenda_mensal_barbearia(cls, agenda_barbearia):        
        try:
            ControladorAgendaMensal.atualizar_agenda_mensal_service(agenda_barbearia)
            flash("Agenda da barbearia atualizada com sucesso", EnumStatusMensagens.SUCESSO.value)
        except Exception as erros:
            flash(f"Erro ao tentar atualizar a agenda da barbearia {erros}", EnumStatusMensagens.ERRO.value)
        
        return redirect(url_for("gestor.gestor_horario_funcionamento_barbearia"))       
     
     
        
    @classmethod
    def consultar_agenda_mensal_barbearia(cls):        
        try:
            return ControladorAgendaMensal.consultar_todas_agenda_mensal_service()
        except Exception as erros:
            flash(f"Erro na consulta da agenda da barbearia {erros}", EnumStatusMensagens.ERRO.value)     