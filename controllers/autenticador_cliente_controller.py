from models.usuario import Usuario
from flask import  session, redirect, url_for
from sqlalchemy.exc import IntegrityError
from werkzeug.security import check_password_hash,generate_password_hash
from models.cliente import Cliente

class AutenticacaoCliente():
    
    def login(email:str, senha:str):
        # Validação inicial simples
        if not email or not senha:
            session['erro'] = "Por favor, preencha todos os campos."
            return redirect(url_for('cliente.clientLoginPage'))
            
        # 3. Busca o usuário no MySQL através do método que você já criou na sua classe User
        try:
            usuario = Cliente.buscarCLientePorEmail(email)
        except Exception as erro :
            print(f"{erro}")
            session['erro'] = "Erro ao tentar se comunicar com o banco de dados.\nContate o suporte"
            return  redirect(url_for('cliente.clientLoginPage'))

        # 4. Verifica se o usuário existe e se a senha confere
        # (Nota: Se futuramente usar criptografia com werkzeug, use check_password_hash aqui)
        
        if usuario:
            print(email)
            print(usuario.senha_hash)
            print(senha)
            print(check_password_hash(usuario.senha_hash, senha))
            if check_password_hash(usuario.senha_hash, senha):
                # 5. Salva o ID e os dados completos na sessão (Agora incluindo o ID gerado pelo banco!)
                session['dados_cliente'] = dict(usuario._mapping)
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
    def registrarCliente(usuario:Usuario):
        # Salvando os dados na sessão do Flask
        try:
            id_cliente = usuario.salvar()
        
            # salvar o usuario como cliente
            cliente = Cliente(
               id_cliente
            )

            id_cliente = cliente.salvar()

            if not cliente:
                session['erro'] = 'Erro ao criar o usuario'
                return redirect(url_for('cliente.clientRegisterPage'))
            
            session.permanent = True
            session['dados_cliente'] = usuario.to_dict()
       
        except IntegrityError as i:
            print(f"{i}")
            session['erro'] = "ATENÇÃO: e-mail já cadastrados no sistema" 
            return redirect(url_for('cliente.clientRegisterPage'))
        except Exception as erro:
            session['erro'] = str(erro)
            return redirect(url_for('cliente.clientRegisterPage'))
        
        return redirect(url_for('cliente.cadastroSucesso'))
    
   