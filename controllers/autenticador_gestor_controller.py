from models.gestor import Gestor
from models.servicos import Servicos
from models.barbearia import Barbearia
from flask import Blueprint, session, redirect, url_for, flash
from sqlalchemy.exc import IntegrityError
from werkzeug.security import check_password_hash
from database import db

class AutenticadorGestor():
    
    def login(email:str, senha:str):
        # Validação inicial simples
        if not email or not senha:
            session['erro'] = "Por favor, preencha todos os campos."
            return redirect(url_for('gestor.gestorLoginPagina'))
            
        # 3. Busca o usuário no MySQL através do método que você já criou na sua classe Usuario
        try:
            gestor = Gestor.consultarGestorEmail(email,Barbearia.getCNPJ())
            
        except Exception as erro :
            print(f"{erro}")
            session['erro'] = "Erro ao tentar se comunicar com o banco de dados.\nContate o suporte"
            return  redirect(url_for('gestor.gestorLoginPagina'))

        # 4. Verifica se o usuário existe e se a senha confere
        # (Nota: Se futuramente usar criptografia com werkzeug, use check_password_hash aqui)
        
        if gestor:
            if check_password_hash(gestor["senha_hash"], senha):
                # 5. Salva o ID e os dados completos na sessão (Agora incluindo o ID gerado pelo banco!)
                session['dados_gestor'] = dict(gestor)
                # to_dict para dados salvos via ORM
                # session['dados_usuario'] = user.to_dict()
                # Redireciona o cliente logado diretamente para a página de agendamentos
                return redirect(url_for('gestor.gestorPainel'))
            else:
                session['erro'] = "ATENÇÃO: e-mail ou senha incorretos." 
                        
                return redirect(url_for('gestor.gestorLoginPagina'))
                    
        else:
            # Se o email não estiver cadastrado                  
            session['erro'] = "ATENÇÃO: usuário não cadastrado.\nRealize o seu cadastro"
            return redirect(url_for('gestor.gestorLoginPagina'))
<<<<<<< HEAD

    def cadastrarBarbeiro(photo:str, cpf:str, name:str, email:str, telephone:str, address:str, description:str):
        # Validação inicial simples
        if not photo or not cpf or not name or not email or not telephone or not address or not description:
            session['erro'] = "Por favor, preencha todos os campos."
            return redirect(url_for('gestor.gestorBarbeiroCadastro'))
        return "<h1>Deu Certo</h1>"

    def cadastrarServico(novo_foto_nome:str, novo_descricao: str, novo_valor: str, novo_duracao:str ):
        # Validação inicial simples
        if not novo_descricao.strip() or not novo_valor.strip() or not novo_duracao.strip():
            flash("Campos vazios! Verifique se os campos estão vazios!")
            return  redirect(url_for('gestor.gestorServicoCadastrar'))

        session['dados-servicos'] = {
            'duracao':novo_duracao,
            'nome': novo_descricao,
            'valor': novo_valor
        }

        print(novo_valor)
        try:
            valor = float(novo_valor)
            duracao = int(novo_duracao)

            if (valor < -1) or (duracao < -1):
                flash("Os valores de preco e duração devem ser maiores que zero!")
                return  redirect(url_for('gestor.gestorServicoCadastrar'))
         
            # Salvando os dados na sessão do Flask
        
            servicos = Servicos()
            servicos.descricao = novo_descricao
            servicos.foto_nome = novo_foto_nome
            servicos.valor = valor
            servicos.duracao = duracao
                
            resultado_servico = servicos.salvarServico()

            if not resultado_servico:
                flash( 'Erro ao criar o serviço')
                return redirect(url_for('gestor.gestorServicoCadastrar'))
            
            db.session.commit()
            session.pop('dados-servicos')
       
        except IntegrityError as i:
            db.session.rollback()
            

            print(f"{i}")
            flash( "Erro ao cadastrar o serviço!" )
            return redirect(url_for('gestor.gestorServicoCadastrar'))
        except (ValueError, TypeError):
            flash("Os campos Preço e duração só aceitam números!" )
            return redirect(url_for('gestor.gestorServicoCadastrar'))
        
        except Exception as erro:
            print(f"{erro}")
            db.session.rollback()

            flash("Confira se digitou o campo ")
            return redirect(url_for('gestor.gestorServicoCadastrar'))
        
        return redirect(url_for('gestor.gestorAbaServicos'))

    def deletarServico(id_servico):
        try:
            servicos = Servicos()
           
            resultado = servicos.deletarServico(id_servico)

            if resultado:
                flash("Serviço de código ["+ str(id_servico) + "] deletado com sucesso!")
            
            db.session.commit()

        except Exception as error:
            db.session.rollback()
            print(f"{error}")
            flash("Não foi possivel deletar o serviço, consulte o suporte!")
        
        return redirect(url_for('gestor.gestorAbaServicos'))
  
    def editarServico(servico_atualizado:Servicos):
        # Validação inicial simples
        if not servico_atualizado.descricao.strip() or not servico_atualizado.valor.strip() or not servico_atualizado.duracao.strip():
            flash("Campos vazios! Verifique se os campos estão vazios!")
            return  redirect(url_for('gestor.gestorServicoCadastrar'))
    
        session['dados-servicos'] = {
                'duracao':new_duracao,
                'nome': new_descricao,
                'valor': new_valor
        }
    
        print(new_valor)
        try:
            valor = float(new_valor)
            duracao = int(new_duracao)
    
            if (valor < -1) or (duracao < -1):
                flash("Os valores de preco e duração devem ser maiores que zero!")
                return  redirect(url_for('gestor.gestorServicoCadastrar'))
             
            # atualizando os dados na sessão do Flask
            
            servicos = Servicos()
            servicos.descricao = new_descricao
            servicos.foto_nome = new_foto_nome
            servicos.valor = valor
            servicos.duracao = duracao
                    
            resultado_servico = servicos.salvarServico()
    
            if not resultado_servico:
                flash( 'Erro ao criar o serviço')
                return redirect(url_for('gestor.gestorServicoCadastrar'))
                
            db.session.commit()
            session.pop('dados-servicos')
           
        except IntegrityError as i:
            db.session.rollback()
                
    
            print(f"{i}")
            flash( "Erro ao cadastrar o serviço!" )
            return redirect(url_for('gestor.gestorServicoCadastrar'))
        except (ValueError, TypeError):
            flash("Os campos Preço e duração só aceitam números!" )
            return redirect(url_for('gestor.gestorServicoCadastrar'))
            
        except Exception as erro:
            print(f"{erro}")
            db.session.rollback()
    
            flash("Confira se digitou o campo ")
            return redirect(url_for('gestor.gestorServicoCadastrar'))
            
        return redirect(url_for('gestor.gestorAbaServicos'))    
=======
>>>>>>> feature-backend
