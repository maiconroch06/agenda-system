from models.User import User
from flask import  session, redirect, url_for
from sqlalchemy.exc import IntegrityError
from werkzeug.security import check_password_hash
from models.Client import Client

class AuthenticationUser():
    
    def login(email:str, senha:str):
        # Validação inicial simples
                if not email or not senha:
                    session['erro'] = "Por favor, preencha todos os campos."
                    return redirect(url_for('cliente.clientLoginPage'))
                  
                # 3. Busca o usuário no MySQL através do método que você já criou na sua classe User
                try:
                    user = User.buscar_por_email(email)
                except Exception as erro :
                    session['erro'] = "Erro ao tentar se comunicar com o banco de dados.\nContate o suporte"
                    return  redirect(url_for('cliente.clientLoginPage'))
        
                # 4. Verifica se o usuário existe e se a senha confere
                # (Nota: Se futuramente usar criptografia com werkzeug, use check_password_hash aqui)
              
                if user:
                    if check_password_hash(user.senha_hash, senha):
                        # 5. Salva o ID e os dados completos na sessão (Agora incluindo o ID gerado pelo banco!)
                        session['dados_cliente'] = dict(user._mapping)
                        # to_dict para dados salvos via ORM
                        # session['dados_cliente'] = user.to_dict()
                        # Redireciona o cliente logado diretamente para a página de agendamentos
                        return redirect(url_for('cliente.clientAgendamentoServicos'))
                    else:
                        session['erro'] = "ATENÇÃO: e-mail ou senha incorretos."                
                        return redirect(url_for('cliente.clientLoginPage'))
                            
                else:
                    # Se o email não estiver cadastrado                  
                    session['erro'] = "ATENÇÃO: usuário não cadastrado.\nRealize o seu cadastro"
                    return redirect(url_for('cliente.clientLoginPage'))
                               
                    
    
    #cadastro funcionando perfeitamente                    
    def registerUser(user:User):
        # Salvando os dados na sessão do Flask
        try:
            user.salvar()
        
            # salvar o usuario como cliente
            client = Client(
                user.to_dict().get('id')
            )

            id_cliente = client.salvar()

            if not client:
                session['erro'] = 'Erro ao criar o usuario'
                return redirect(url_for('cliente.clientRegisterPage'))
            
            session.permanent = True
            session['dados_cliente'] = user.to_dict()
        
        except IntegrityError:
            session['erro'] = "ATENÇÃO: e-mail já cadastraados no sistema"  
            return redirect(url_for('cliente.clientRegisterPage'))
        except Exception as erro:
            session['erro'] = str(erro)
            return redirect(url_for('cliente.clientRegisterPage'))
        
        return redirect(url_for('cliente.clientAgendamentoServicos'))
    
   