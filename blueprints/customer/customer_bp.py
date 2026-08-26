from flask import Blueprint, render_template, redirect, url_for

customer_bp = Blueprint('customer', __name__, template_folder='templates')

@customer_bp.route('/')
def agendamento():
    return render_template('cunstoner/page-etapas-agendamento.html')