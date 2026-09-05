from flask import Blueprint, render_template, redirect, url_for

client = Blueprint('client', __name__, template_folder='templates')

@client.route('/')
def clientSignUpLogin():
    return "página inexistente ainda, deve ser colocado por exemplo uma pagina login e/ou cadastro"
   #return render_template('pages/client/scheduling.html')
   

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