import os
from flask import Flask 
from database import create_database, db

app = Flask(__name__)

# Configura o app e inicializa o db.init_app(app)
create_database(app)

# IMPORTANTE: Importe os seus modelos aqui ANTES do create_all.
# Se você não importá-los, o SQLAlchemy não saberá que as tabelas existem e criará um banco vazio!
from models import User, Address

# ==========================================
# 1. CRIAÇÃO AUTOMÁTICA DAS TABELAS NO MYSQL
# ==========================================
with app.app_context():
    # Esse comando lê as classes e as cria no banco
    db.create_all()


# ==========================================
# 2. IMPORTS DOS BLUEPRINTS (Apenas APÓS criar o banco)
# ==========================================
from routers.public import publics
from routers.client import client
# from routers.login import user_login
# from routers.manager import manager


# ==========================================
# 3. REGISTRO DOS BLUEPRINTS
# ==========================================
app.register_blueprint(publics)
app.register_blueprint(client, url_prefix='/cliente')
# app.register_blueprint(user_login, url_prefix='/login')
# app.register_blueprint(manager, url_prefix='/gestor')
# app.register_blueprint(client, url_prefix='/cliente')

if __name__ == "__main__":
    app.run(debug=True)
