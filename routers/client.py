from flask import Blueprint, render_template, redirect, url_for

client = Blueprint('client', __name__, template_folder='templates')

@client.route('/')
def clientSource():
    #redireciona para a raiz do site novamente
    return redirect('/')
 
@client.route('/login')
def clientLogin():
    return render_template('pages/client/client-login.html')
   
@client.route('/cadastro')
def clientRegister():
    return render_template('pages/client/client-register.html')

@client.route('/cadastro/finalizacao', methods=['GET','POST'])
def clientRegisterFinish():
    return render_template('pages/client/finish-register-restrict.html')
   
@client.route('/agendamento/servicos', methods=['GET','POST'])
def clientAgendamentoServicos():
   return render_template('pages/client/scheduling.html')

@client.route('/agendamentos', methods=['GET','POST'])
def clientAgendamento():
   return render_template('pages/client/scheduling-restrict.html')

