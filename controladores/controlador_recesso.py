from enums import EnumStatusMensagens
from services_mvc import RecessoService
from flask import flash, render_template, redirect, url_for

class ControladorRecesso:
    __recessoService = RecessoService()
    __RECESSO_CONSULTAR = "gestor.gestor_recesso_consultar"

    @classmethod
    def consultarRecessos(cls):
        try:
            return cls.__recessoService.consultar_recessos()
        except Exception as erros:
            flash(f"Erro consultar os recessos da barbearia {erros}", EnumStatusMensagens.ERRO.value)

    @classmethod
    def consultarRecessosMesAtual(cls):
        try:
            return cls.__recessoService.consultar_recessos_mes_atual_services()
        except Exception:
            flash(f"Erro consultar os recessos da barbearia ", EnumStatusMensagens.ERRO.value)

    @classmethod
    def consultarRecessosAnoAtual(cls):
        try:
            return cls.__recessoService.consultar_recessos_ano_atual_services()
        except Exception:
            flash(f"Erro consultar os recessos da barbearia", EnumStatusMensagens.ERRO.value)

    @classmethod
    def cadastrarRecesso(cls, recesso):
        try:
            if cls.__recessoService.cadastrar_recessos_services(recesso):
                flash(f"Recesso [ {recesso.descricao_recesso} ] cadastrado com sucesso.",
                      EnumStatusMensagens.SUCESSO.value)
        except Exception as error:
            flash(f"Erro cadastrar o recesso da barbearia {error}", EnumStatusMensagens.ERRO.value)

        return redirect(url_for(cls.__RECESSO_CONSULTAR))

    @classmethod
    def atualizarRecesso(cls, recesso):
        try:
            if cls.__recessoService.atualizar_recessos_services(recesso):
                flash(f"Recesso [ {recesso.descricao_recesso} ] atualizado com sucesso",
                      EnumStatusMensagens.SUCESSO.value)
        except Exception as erros:
            flash(f"Erro atualizar o recesso [ {recesso.descricao_recesso} ] {erros}da barbearia",
                  EnumStatusMensagens.ERRO.value)

        return redirect(url_for(cls.__RECESSO_CONSULTAR))

    @classmethod
    def excluirRecessos(cls, recesso):
        try:
            if cls.__recessoService.excluir_recessos_services(recesso.id_recesso):
                flash(f"Recesso [ {recesso.descricao_recesso} ] excluido com sucesso",
                      EnumStatusMensagens.SUCESSO.value)
        except Exception:
            flash(f"Erro ao tentar excluir o recesso [ {recesso.descricao_recesso} ] da barbearia",
                  EnumStatusMensagens.ERRO.value)

        return redirect(url_for(cls.__RECESSO_CONSULTAR))