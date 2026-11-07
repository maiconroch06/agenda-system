from flask import session, redirect, url_for, flash, render_template
from sqlalchemy.exc import IntegrityError
from werkzeug.security import check_password_hash
from database import db
from enums import EnumStatusMensagens
from services_mvc import GestorServiceMVC, ServicoBarbearia, BarbeiroService
from execoes import ImagemErrorExcecao 
from models import Barbeiro
from werkzeug.utils import secure_filename
from .controlador_cliente import ControladorCliente

class ControladorGestor():
    __gestor_service_mvc = GestorServiceMVC()
    __servicos_barbearia_service_mvc = ServicoBarbearia()
    __barbeiro_service_mvc = BarbeiroService()
    __controlador_cliente = ControladorCliente()
  
    
    @classmethod
    def login(cls, email:str, senha:str):
        
            try: 
                cls.__gestor_service_mvc.gestorRealizarLoginService(email,senha)   
                return redirect(url_for('gestor.gestorPainel'))
            
            except Exception as error:
                flash(f"{error}")
                return  redirect(url_for('gestor.gestorLoginPagina'))

    @classmethod
    def cadastrarBarbeiro(cls, barbeiro: Barbeiro, fotoTemp):
        try:
            
            barbeiro.id = cls.__barbeiro_service_mvc.cadastrarUsuarioService(barbeiro,secure_filename(fotoTemp.filename))
                        
            if cls.__barbeiro_service_mvc.salvar_dados_especificos(barbeiro, fotoTemp):  
                flash(f"Barbeiro {barbeiro.nome_completo.split(" ")[0]} cadastrado com sucesso.", EnumStatusMensagens.SUCESSO.value)  
                return redirect(url_for('gestor.gestorAbaBarbeiros'))
            
        except Exception as erros:
            flash(f"{erros}", EnumStatusMensagens.ERRO.value)
            
        return redirect(url_for('gestor.gestorBarbeiroPage'))

    @classmethod
    def cadastrarServico(cls, foto, novo_descricao: str, novo_valor: str, novo_duracao:str ):
        
        try:
            if cls.__servicos_barbearia_service_mvc.cadastrar_servico_barbearia(foto, novo_descricao, novo_valor, novo_duracao):
                return redirect(url_for('gestor.gestorAbaServicos'))
        
        except ImagemErrorExcecao as erros:
            flash(f"{erros}", EnumStatusMensagens.AVISO.value)
            return redirect(url_for('gestor.gestorServicoCadastrar'))
        
        except Exception as erros:
            flash(f"{erros}", EnumStatusMensagens.ERRO.value)
            return redirect(url_for('gestor.gestorServicoCadastrar'))
             
    @classmethod
    def deletarServico(cls, id_servico):
        try:
            cls.__servicos_barbearia_service_mvc.excluir_servico_barbearia(id_servico)   
        except Exception as error:
            flash(f"{error}")
            
        return redirect(url_for('gestor.gestorAbaServicos'))  
        
        
    @classmethod
    def editarServico(cls, id, imagem_form, img_padrao, imagem_anterior, descricao_servico, valor, duracao, ativo):
       
        try:
         
            cls.__servicos_barbearia_service_mvc.editar_servico_barbearia(id, imagem_form, img_padrao, imagem_anterior, descricao_servico, valor, duracao, ativo)
            flash(f"Servico {descricao_servico} atualizado com sucesso.", EnumStatusMensagens.SUCESSO.value)
        except Exception as erros:
            flash(f"{erros}", EnumStatusMensagens.ERRO.value)
            
        
        return redirect(url_for("gestor.gestorAbaServicos")) 
         
        
            
    @classmethod
    def consultar_servicos(cls):
        return render_template('pages/gestor/gestor-painel-servicos-rp.html', listaServicos = cls.__servicos_barbearia_service_mvc.consultar_todos_servicos(), mensagens_status=EnumStatusMensagens)
   
    @classmethod
    def consultar_clientes(cls):
        return render_template('pages/gestor/gestor-painel-clientes-rp.html', usuarios= cls.__controlador_cliente.consultar_todos_clientes(),  mensagens_status=EnumStatusMensagens)

