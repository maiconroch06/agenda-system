from flask import Blueprint, render_template, redirect, url_for

barbeiro = Blueprint('barbeiro', __name__, template_folder='templates')

@barbeiro.route('/')
def barberSource():
    return redirect('/')

@barbeiro.route('/login')
def barberLogin():
    return render_template('pages/barbeiro/barbeiro-login.html')

@barbeiro.route('/painel')
def barberPanel():
    return render_template('pages/barbeiro/barbeiro-panel-rp.html')