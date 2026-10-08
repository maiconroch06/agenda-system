from models.gestor import Gestor
from models.barbearia import Barbearia
from flask import Blueprint, session, redirect, url_for
from sqlalchemy.exc import IntegrityError
from werkzeug.security import check_password_hash

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
