from flask import session, redirect, url_for, flash, render_template
from sqlalchemy.exc import IntegrityError
from werkzeug.security import check_password_hash
from database import db
from enums import EnumStatusMensagens
from decimal import Decimal, InvalidOperation
from services_mvc import GestorServiceMVC, ServicoBarbearia
from execoes import ImagemErrorExcecao 

class ControladorGestor():
    
    def __init__(self):
        self.gestor_service_mvc = GestorServiceMVC()
        self.servicos_barbearia_service_mvc = ServicoBarbearia()
    
    def login(self, email:str, senha:str):
        
            try: 
                self.gestor_service_mvc.gestorRealizarLoginService(email,senha)   
                return redirect(url_for('gestor.gestorPainel'))
            
            except Exception as error:
                flash(f"{error}")
                return  redirect(url_for('gestor.gestorLoginPagina'))

    def cadastrarBarbeiro(photo:str, cpf:str, name:str, email:str, telephone:str, address:str, description:str):
        

    def cadastrarServico(self, foto, novo_descricao: str, novo_valor: str, novo_duracao:str ):
        
        try:
            self.servicos_barbearia_service_mvc.cadastrar_servico_barbearia(foto, novo_descricao, novo_valor, novo_duracao)
            return redirect(url_for('gestor.gestorAbaServicos'))
        
        except ImagemErrorExcecao as erros:
            flash(f"{erros}", EnumStatusMensagens.AVISO.value)
            return redirect(url_for('gestor.gestorServicoCadastrar'))
        
        except Exception as erros:
            flash(f"{erros}", EnumStatusMensagens.ERRO.value)
            return redirect(url_for('gestor.gestorServicoCadastrar'))
        
        
        
             
    def deletarServico(id_servico):
        try:
            servicos = Servicos()
           
            resultado = servicos.deletarServico(id_servico)

            if resultado:
                flash("Serviço de código ["+ str(id_servico) + "] deletado com sucesso!", EnumStatusMensagens.SUCESSO.value)
            
            db.session.commit()

        except Exception as error:
            db.session.rollback()
            print(f"{error}")
            flash("Não foi possivel deletar o serviço, consulte o suporte!", EnumStatusMensagens.ERRO.value)
        
        return redirect(url_for('gestor.gestorAbaServicos'))
  
    def editarServico(id: str, novo_foto_nome:str, nova_descricao: str, novo_valor: Decimal, nova_duracao:str, ativo:str):

        # Validação inicial simples
        rota_erro = 'gestor.gestorServicoEditarPagina'
        
        try:
           
            id_servico = int(id)
            status_ativo = int(ativo)

            if not nova_descricao.strip() or  novo_valor <= Decimal('0') or not nova_duracao.strip() or id_servico < 1:
                flash("Campos vazios! Verifique se os campos estão vazios!", EnumStatusMensagens.AVISO.value)
                return  redirect(url_for('gestor.gestorServicoCadastrar'))
          
            servico = Servicos().consultarIdServicoValido(id_servico)


            if servico is None:
                flash("Aviso: edição não efetuada, servico inexistente!", EnumStatusMensagens.AVISO.value)
                return redirect(url_for("gestor.gestorAbaServicos"))
                        
            duracao = int(nova_duracao)
          
            if (duracao < 0):
                flash("A duração devem ser maior que zero!", EnumStatusMensagens.AVISO.value)
                return  redirect(url_for(rota_erro))

            # atualizando os dados na sessão do Flask
            servicos = Servicos()
            
            servicos.id = id_servico
            servicos.descricao = nova_descricao
            servicos.valor = novo_valor
            servicos.duracao = duracao
            servicos.foto_nome = novo_foto_nome
            servicos.ativo = status_ativo         
            servicos.data_atualizacao = servicos.dataFormatada()
                        
            resultado_servico = servicos.atualizarServico()
    
            if resultado_servico.rowcount == 0:
                flash( 'Erro ao criar o serviço',EnumStatusMensagens.ERRO.value)
                return redirect(url_for(rota_erro,id_servico=id_servico))
                
            db.session.commit()

            flash( 'Servico atualizado com sucesso!',EnumStatusMensagens.SUCESSO.value)
            return redirect(url_for('gestor.gestorAbaServicos'))
           
        except IntegrityError as i:
            db.session.rollback()
            print(f"{i}")
            flash( "Erro ao cadastrar o serviço!" )
            return redirect(url_for(rota_erro,id_servico=id_servico))
        
        except (ValueError, TypeError) as error:
            print(f" error de tipo {error}")
            flash("Os campos Preço e duração só aceitam números!" )
            return redirect(url_for(rota_erro,id_servico=id_servico))
            
        except Exception as erro:
            print(f"{erro}")
            db.session.rollback()
            flash("Confira se digitou o campo ")
            return redirect(url_for(rota_erro,id_servico=id_servico))
            
    def consultar_servicos(self):
        return render_template('pages/gestor/gestor-painel-servicos-rp.html', listaServicos = self.servicos_barbearia_service_mvc.consultar_todos_servicos(), mensagens_status=EnumStatusMensagens)
             
