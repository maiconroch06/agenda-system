from flask import Blueprint, render_template

publics = Blueprint('public', __name__)

@publics.route('/')
def homePage():
    return render_template('index.html')

@publics.route('/tipo-usuario')
def category():
    return render_template('category-user.html')

# ROTAS APENAS DE DESENVOLVIMENTO (FRONT) #