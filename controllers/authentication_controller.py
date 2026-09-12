from models.User import User
from flask import Blueprint, session, redirect, url_for
from sqlalchemy.exc import IntegrityError
from models.Client import Client
from werkzeug.security import check_password_hash

class AuthenticationUser():
    
    def login(email:str, senha:str):
        # Validação inicial simples
                if not email or not senha:
                    session['erro'] = "Por favor, preencha todos os campos."
                    return redirect(url_for('cliente.clientLoginPage'))
                  
                # 3. Busca o usuário no MySQL através do método que você já criou na sua classe User
                usuario = User.buscar_por_email(email)
        
                # 4. Verifica se o usuário existe e se a senha confere
                # (Nota: Se futuramente usar criptografia com werkzeug, use check_password_hash aqui)
              
                if usuario:
                    if check_password_hash(usuario.senha_hash, senha):
                        # 5. Salva o ID e os dados completos na sessão (Agora incluindo o ID gerado pelo banco!)
                        session['dados_usuario'] = usuario.to_dict()
                        # Redireciona o cliente logado diretamente para a página de agendamentos
                        return redirect(url_for('cliente.clientAgendamentoServicos'))
                    else:
                        session['erro'] = senha                    
                        return redirect(url_for('cliente.clientLoginPage'))
                            
                else:
                    # Se o email não estiver cadastrado                  
                    session['erro'] = "ATENÇÃO: usuário não cadastrado.\nRealize o seu cadastro"
                    return redirect(url_for('cliente.clientLoginPage'))
                               
                    
                        
    def registerUser(user:User):
        # Salvando os dados na sessão do Flask
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
        session['dados_usuario'] = id_cliente
        return redirect(url_for('cliente.clientAgendamentoServicos'))