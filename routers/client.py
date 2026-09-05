from flask import Blueprint, render_template, redirect, url_for

client = Blueprint('client', __name__, template_folder='templates')

@client.route('/')
def clientSignUpLogin():
    return render_template('pages/registers/user-login.html')
   

@client.route('/cadastro')
def clientRegister():
    return render_template('pages/register/user-register.html')
   # return render_template('pages/client/scheduling.html')
   
@client.route('/agendamento/servicos')
def clientAgendamentoServicos():
   return render_template('pages/client/scheduling.html')

@client.route('/agendamentos')
def clientAgendamento():
   return render_template('pages/client/scheduling.html')