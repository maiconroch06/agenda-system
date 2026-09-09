from flask import Blueprint, render_template, redirect, url_for

barber = Blueprint('barber', __name__, template_folder='templates')

@barber.route('/')
def barberSource():
    return redirect('/')

@barber.route('/login')
def barberLogin():
    return render_template('pages/barber/barber-login.html')

@barber.route('/painel')
def barberPanel():
    return render_template('pages/barber/barber-panel-restrict.html')