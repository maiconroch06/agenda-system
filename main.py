import os
from flask import Flask 
from database import create_database 

app = Flask(__name__)

create_database(app,os)

# ==========================================
# 2. IMPORTS DOS BLUEPRINTS (Apenas APÓS criar o banco)
# ==========================================
from routers.public import publics
from routers.client import client
from routers.manager import manager
from routers.barber import barber
from routers.login import user_login

# ==========================================
# 3. REGISTRO DOS BLUEPRINTS
# ==========================================
app.register_blueprint(publics)
app.register_blueprint(client, url_prefix='/cliente')
app.register_blueprint(manager, url_prefix='/gestor')
app.register_blueprint(barber, url_prefix='/barbeiro')
app.register_blueprint(user_login, url_prefix='/login')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
