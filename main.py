from flask import Flask, session
from datetime import timedelta
from database import create_database, db
from database.seed import initialize


app = Flask(__name__)

# Configura o app e inicializa o db.init_app(app)
create_database(app)

# IMPORTANTE: Importe os seus modelos aqui ANTES do create_all.
# Se você não importá-los, o SQLAlchemy não saberá que as tabelas existem e criará um banco vazio!
from models import *

# ==========================================
# 1. CRIAÇÃO AUTOMÁTICA DAS TABELAS NO MYSQL
# ==========================================
with app.app_context():
    # Esse comando lê as classes e as cria no banco
    db.create_all()
    # Populando banco com dados padrões
    initialize()
    


# ==========================================
# 2. IMPORTS DOS BLUEPRINTS (Apenas APÓS criar o banco)
# ==========================================
from routers.public_route import publics
from routers.cliente_route import cliente
# from routers.login import user_login
from routers.gestor_route import gestor
from routers.barbeiro_route import barbeiro


# ==========================================
# 3. REGISTRO DOS BLUEPRINTS
# ==========================================
app.register_blueprint(publics)
app.register_blueprint(cliente, url_prefix='/cliente')
app.register_blueprint(gestor, url_prefix='/gestor')
app.register_blueprint(barbeiro, url_prefix='/barbeiro')



app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
