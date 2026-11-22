from services_mvc import  ServicoBarbearia
from enums import EnumStatusMensagens
from flask import flash, redirect, url_for, render_template
from sqlalchemy.exc import IntegrityError
from execoes import ImagemErrorExcecao

class ControladorServico:
    __servicos_barbearia_service_mvc = ServicoBarbearia()
    __GESTOR_ABAS_SERVICOS = "gestor.gestorAbaServicos"
    
    @classmethod
    def consultar_servicos_resumido(cls):
        return cls.__servicos_barbearia_service_mvc.consultar_todos_servicos_resumo()
    

    @classmethod
    def consultar_todos_os_servicos(cls):
        return cls.__servicos_barbearia_service_mvc.consultar_todos_servicos()
            
    @classmethod
    def consultar_servico_nome(cls, nome_servico):
        return cls.__servicos_barbearia_service_mvc.consultar_servico_nome(nome_servico)

    @classmethod
    def editarServico(cls, id, imagem_form, img_padrao, imagem_anterior, descricao_servico, valor, duracao, ativo):
        try:

            cls.__servicos_barbearia_service_mvc.editar_servico_barbearia(id, imagem_form, img_padrao, imagem_anterior,
                                                                          descricao_servico, valor, duracao, ativo)
            flash(f"Servico {descricao_servico} atualizado com sucesso.", EnumStatusMensagens.SUCESSO.value)
        except Exception as erros:
            print(f"erro ao tentar atualizar a agenda: {erros}")

        return redirect(url_for(cls.__GESTOR_ABAS_SERVICOS))


    @classmethod
    def excluir_servico(cls, id_servico, foto_nome, nome_servico):
        try:
            cls.__servicos_barbearia_service_mvc.excluir_servico_barbearia(id_servico, foto_nome)
            flash(f"O servico foi excluido com sucesso!", EnumStatusMensagens.SUCESSO.value)

        except IntegrityError:
            flash(f"O serviço [ {nome_servico}] não pode ser excluido, pois ele pertence a um agendamento.",
                  EnumStatusMensagens.ERRO.value)
        except Exception:
            flash(f"Erro o excluir o serviço [ {nome_servico}], contate o suporte", EnumStatusMensagens.ERRO.value)

        return redirect(url_for(cls.__GESTOR_ABAS_SERVICOS))

    @classmethod
    def cadastrarServico(cls, foto, novo_descricao: str, novo_valor: str, novo_duracao: str):

        try:
            if cls.__servicos_barbearia_service_mvc.cadastrar_servico_barbearia(foto, novo_descricao, novo_valor,
                                                                                novo_duracao):
                return redirect(url_for(cls.__GESTOR_ABAS_SERVICOS))

        except ImagemErrorExcecao as erros:
            flash(f"{erros}", EnumStatusMensagens.AVISO.value)
            return redirect(url_for(cls.__GESTOR_ABAS_SERVICOS))

        except Exception as erros:
            flash(f"{erros}", EnumStatusMensagens.ERRO.value)
            return redirect(url_for(cls.__GESTOR_ABAS_SERVICOS))

    @classmethod
    def consultar_servicos(cls):
        return render_template('pages/gestor/gestor-painel-servicos-rp.html', modo=0,
                               listaServicos=ControladorServico.consultar_todos_os_servicos(),
                               mensagens_status=EnumStatusMensagens)

    @classmethod
    def consultar_servico_nome(cls, nome_servico):
        return render_template('pages/gestor/gestor-painel-servicos-rp.html', nome_servico=nome_servico, modo=1,
                               listaServicos=cls.__servicos_barbearia_service_mvc.consultar_servico_nome(nome_servico),
                               mensagens_status=EnumStatusMensagens)