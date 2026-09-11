from models import User
from flask import Blueprint, render_template, session, request, redirect, url_for
from sqlalchemy.exc import IntegrityError


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
                if usuario and usuario.senha_hash == senha:
                    
                    # 5. Salva o ID e os dados completos na sessão (Agora incluindo o ID gerado pelo banco!)
                    session['dados_usuario'] = usuario.to_dict()
                    session['logado'] = True
                    
                    # Redireciona o cliente logado diretamente para a página de agendamentos
                    return redirect(url_for('cliente.clientAgendamentoServicos'))
                
                else:
                    # Se a senha estiver errada, recarrega mantendo o e-mail na tela
                    session['erro'] = "E-mail ou senha incorretos."
                    session['email'] = email   
                     
                    return redirect(url_for('cliente.clientLoginPage'))
                        
    def registerUser(user:User):
        # Salvando os dados na sessão do Flask
        user.salvar();
        session['dados_usuario'] = user.to_dict()
        print(session.get('dados_usuario'))
        return redirect(url_for('cliente.clientAgendamentoServicos'))