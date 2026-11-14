import re
import os

from flask import render_template, redirect, url_for, flash
from werkzeug.utils import secure_filename

from database import db
from datetime import datetime, timezone

from models.usuarios import Usuario
from models.endereco import Endereco
from models.barbeiros import Barbeiro
from enums import EnumStatusMensagens
from services_mvc import BarbeiroService
from .controlador_faltas_justificadas import FaltasJustificadaBarbeiro


class ControladorBarbeiro:

    __barbeiroService = BarbeiroService()

    
    @classmethod
    def login_barbeiro(cls, email:str, senha:str):
        try:
            cls.__barbeiroService.barbeiro_realizar_login_service(email,senha)   
            return redirect(url_for('barbeiro.barbeiroPainel'))
            
        except Exception as error:
            flash(f"{error}")
            return redirect(url_for('barbeiro.barbeiroLoginPagina'))

    @classmethod
    def consultar_todos_barbeiros(cls):
        return cls.__barbeiroService.consultar_barbeiros()
        #return render_template('pages/gestor/gestor-painel-barbeiros-rp.html', barbeiros = cls.__barbeiroService.consultar_barbeiros(), mensagens_status=EnumStatusMensagens)

    @classmethod
    def consultar_agendamentos_barbeiro(cls, barbeiro:dict):
        return cls.__barbeiroService.consultar_agendamentos_barbeiro(barbeiro)
    
    @classmethod
    def atualizar_endereco_barbeiro(cls, endereco):
        try:
            cls.__barbeiroService.atualizar_endereco(endereco)
            flash("Endereço alterado com sucesso", EnumStatusMensagens.SUCESSO.value)
        except Exception:
            flash("Não foi possivel alterar o endeceço, contate o suporte", EnumStatusMensagens.AVISO.value)
        
        return redirect(url_for('gestor.gestorAbaBarbeiros'))   
    
    @classmethod
    def atualizar_status_agendamento(cls, id_agendamento:int, status_agendamento:int):
        try:
            cls.__barbeiroService.alterar_status_agendamento(id_agendamento, status_agendamento)
            flash("Agendamento alterado com sucesso", EnumStatusMensagens.SUCESSO.value)
        except Exception as erros:
            flash(f"Não foi possivel alterar o status do agendamento, contate o suporte", EnumStatusMensagens.AVISO.value)
            flash(f"{erros}")
    
    @classmethod
    def atualizar_informacoes_barbeiro(cls, imagem_form, img_padrao, imagem_anterior, usuario):
        try:
           
            if cls.__barbeiroService.alterar_usuario_barbearia(imagem_form, img_padrao, imagem_anterior, usuario):
                
                return cls.__barbeiroService.alterar_barbeiro_barbearia(usuario)
            return None   
        except Exception :
            flash(f"Não foi possivel alterar o barbeiro, contate o suporte", EnumStatusMensagens.AVISO.value)
   
    @classmethod
    def consultar_faltas_do_barbeiro_ativos(cls):
        try: 
            return cls.__barbeiroService.consultar_faltas_por_barbeiro_ativo()
        except Exception :
           
            flash(f"Não foi possivel consultar as faltas dos barbeiros, contate o suporte", EnumStatusMensagens.AVISO.value)
            
    @classmethod
    def cadastrar_faltas_do_barbeiro_ativos(cls, id_barbeiro, falta_justificada, nome_barbeiro):
            try: 
               
                if FaltasJustificadaBarbeiro.cadastrar_falta_justificada_do_barbeiro(id_barbeiro, falta_justificada):
                    flash(f"Falta justificada do barbeiro {nome_barbeiro} cadastrado com sucesso", EnumStatusMensagens.SUCESSO.value)
                else:
                     flash(f"Não foi possivel cadastrar a falta justificada do barbeiro {nome_barbeiro}, pois ele ja tem um falta cadastrada com a mesma data e horario", EnumStatusMensagens.AVISO.value)       
                
            except Exception :
                flash(f"Não foi possivel cadastrar a falta justificada do barbeiro {nome_barbeiro}, contate o suporte", EnumStatusMensagens.ERRO.value)
                
            return redirect(url_for('gestor.gestor_fatas_justificadas_barbeiro'))
            
    @classmethod
    def excluir_faltas_do_barbeiro_ativos(cls, id_barbeiro, falta_justificada):
            try: 
               
                if FaltasJustificadaBarbeiro.excluir_falta_justificada_do_barbeiro( id_barbeiro, falta_justificada):
                    flash(f"Falta justificada da data: [ {falta_justificada.data_falta} | motivo: {falta_justificada.motivo_falta} ] excluida com sucesso", EnumStatusMensagens.SUCESSO.value)
            except Exception:
            
                flash(f"Não foi possivel excluir a falta justificada da data: [ {falta_justificada.data_falta} | motivo: {falta_justificada.motivo_falta} ], contate o suporte", EnumStatusMensagens.ERRO.value)
                
            return redirect(url_for('gestor.gestor_fatas_justificadas_barbeiro'))
        
    @classmethod
    def atualizar_faltas_do_barbeiro_ativos(cls, id_barbeiro, falta_justificada,nome_barbeiro):
        try:
            if FaltasJustificadaBarbeiro.atualizar_falta_justificada_do_barbeiro(id_barbeiro,falta_justificada):
                flash(f"Falta justificada da data: [ {falta_justificada.data_falta} | motivo: {falta_justificada.motivo_falta} ] atualizada com sucesso", EnumStatusMensagens.SUCESSO.value)
            else:
                flash(f"Falta justificada [ {falta_justificada.data_falta} | motivo: {falta_justificada.motivo_falta} ] não atualizada, já consta um registro de falta cadastrada com a mesma data e horario para  {nome_barbeiro}", EnumStatusMensagens.AVISO.value)       
                            
        except Exception as erros:
        
            flash(f"{erros} Não foi possivel atualizar a falta justificada da data: [ {falta_justificada.data_falta} | motivo: {falta_justificada.motivo_falta} ], contate o suporte", EnumStatusMensagens.ERRO.value)
            
        return redirect(url_for('gestor.gestor_fatas_justificadas_barbeiro'))

