from flask import Blueprint, render_template, redirect, url_for, request, jsonify

auth_bp = Blueprint('auth', __name__, template_folder='templates')

@auth_bp.route('/')
def userAuth():
    return render_template('auth/all-authentication.html')

# Exemplo de banco de dados simulado
USUARIOS_DB = [
    {
        "usuario": "admin@email.com", 
        "senha_hash": "123", # Hash da senha do usuário
        "tipo": "admin"
    }
]

@auth_bp.route('/login', methods=['POST'])
def login():

    usuario = request.form.get('all-authentication-usuario', '').strip()
    senha = request.form.get('all-authentication-senha', '')
    
    erros = {}

    if usuario == USUARIOS_DB[0]["usuario"] and senha == USUARIOS_DB[0]["senha_hash"]:
        return render_template('companies/company-panel.html')
