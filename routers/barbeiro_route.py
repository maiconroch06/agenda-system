from flask import Blueprint, render_template, redirect, url_for

barbeiro = Blueprint('barbeiro', __name__, template_folder='templates')

@barbeiro.route('/')
def barberSource():
    return redirect('/')

@barbeiro.route('/login')
def barbeiroLogin():
    return render_template('pages/barbeiro/barbeiro-login.html')

@barbeiro.route('/painel')
def barbeiroPainel():
    return render_template('pages/barbeiro/barbeiro-painel-inicio-rp.html')

@barbeiro.route('/painel/agenda')
def barbeiroPainelAgenda():
    return render_template('pages/barbeiro/barbeiro-painel-agenda-rp.html')

@barbeiro.route('/painel/configuracao')
def barbeiroPainelConfiguracoes():
    return render_template('pages/barbeiro/barbeiro-painel-configuracao-rp.html')