from flask import Blueprint, render_template, redirect, url_for

client = Blueprint('client', __name__, template_folder='templates')

@client.route('/')
def agendamento():
    return render_template('pages/client/scheduling.html')