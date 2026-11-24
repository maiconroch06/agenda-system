from flask import flash, redirect, url_for
from enums.enum_status_mensagens import EnumStatusMensagens
from services_mvc import AgendaMensalService,  BarbeariaService

class ControladorAgendaMensal():
    __agenda_mensal_service = AgendaMensalService()
    
    @classmethod
    def consultar_todas_agendas_mensais_service(cls):
        try:
            return cls.__agenda_mensal_service.consultar_agenda_mensal_service()
        except Exception as erros:
            flash(f"Erro na consulta da agenda da barbearia {erros}", EnumStatusMensagens.ERRO.value)

    @classmethod
    def consultar_agendas_mensais_por_mes_service(cls):
        try:
            return cls.__agenda_mensal_service.consultar_agenda_mensal_service_por_mes()
        except Exception as erros:
            flash(f"Erro na consulta da agenda da barbearia {erros}", EnumStatusMensagens.ERRO.value)

    @classmethod
    def consultar_agendas_mensais_anual_service(cls):
        try:
            return cls.__agenda_mensal_service.consultar_agenda_mensal_service_anual()
        except Exception as erros:
            flash(f"Erro na consulta da agenda da barbearia {erros}", EnumStatusMensagens.ERRO.value)

    @classmethod
    def cadastrar_agenda_mensal_service(cls, nova_agenda_mensal):
        try:
           if cls.__agenda_mensal_service.cadastrar_agenda_mensal_service(nova_agenda_mensal, BarbeariaService.consultar_cnpj_barbearia()):
                flash("Agenda da barbearia cadastrada com sucesso", EnumStatusMensagens.SUCESSO.value)
        except Exception:
            flash(
                f"Erro ao tentar cadastrar a agenda da barbearia, já existe uma agenda mensal abrangendo a data inicio ou fim",
                EnumStatusMensagens.ERRO.value)

        return redirect(url_for("gestor.gestor_horario_funcionamento_barbearia"))

    @classmethod
    def atualizar_agenda_mensal_service(cls, nova_agenda_mensal):
        try:
            resultaodo= cls.__agenda_mensal_service.atualizar_agenda_mensal_service(nova_agenda_mensal)
            if resultaodo > 0:
                        flash(f"Agenda da barbearia atualizada com sucesso{resultaodo}", EnumStatusMensagens.SUCESSO.value)
        except Exception as erros:
            flash(f"Erro ao tentar atualizar a agenda da barbearia", EnumStatusMensagens.ERRO.value)
        
        return redirect(url_for("gestor.gestor_horario_funcionamento_barbearia"))
    
    @classmethod
    def excluir_agenda_mensal_service(cls, id_agenda_mensal):
        try:
            resultaodo = cls.__agenda_mensal_service.cadastrar_agenda_mensal_service(id_agenda_mensal)
            if resultaodo > 0:
                flash(f"Agenda da barbearia atualizada com sucesso{resultaodo}", EnumStatusMensagens.SUCESSO.value)
        except Exception as erros:
            flash(f"Erro ao tentar atualizar a agenda da barbearia {erros}", EnumStatusMensagens.ERRO.value)

        return redirect(url_for("gestor.gestor_horario_funcionamento_barbearia"))

    @classmethod
    def excluir_agenda_mensal_service(cls, agenda_mensal):
        try:
            resultado = cls.__agenda_mensal_service.cadastrar_agenda_mensal_service(agenda_mensal.id_agenda_mensal)
            if resultado > 0:
                status = "ativada" if agenda_mensal.status_agenda_mensal else "desativada"
                flash(f"Agenda mensal {status} com sucesso", EnumStatusMensagens.SUCESSO.value)
            else:
                flash(f"Agenda mensal não atualizado com sucesso", EnumStatusMensagens.ERRO.value)

        except Exception as erros:
            flash(f"Erro ao tentar alterar o status da agenda {erros}", EnumStatusMensagens.ERRO.value)

        return redirect(url_for("gestor.gestor_horario_funcionamento_barbearia"))
    
    @classmethod
    def atualizar_status_agenda_mensal_service(cls, agenda_mensal):
        try:
                resultado = cls.__agenda_mensal_service.atualizar_status_agenda_mensal_service(agenda_mensal)
                if resultado > 0:
                    status = "ativada" if agenda_mensal.status_agenda_mensal else "desativada"
                    flash(f"Agenda mensal [ {status} ] com sucesso", EnumStatusMensagens.SUCESSO.value)
                else:
                    flash(f"Agenda mensal não foi atualizada!", EnumStatusMensagens.ERRO.value)
    
        except Exception:
            flash(f"Erro ao tentar alterar o status da agenda", EnumStatusMensagens.ERRO.value)

        return redirect(url_for("gestor.gestor_horario_funcionamento_barbearia"))
    

