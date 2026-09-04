import os
from flask import Flask 
from database import create_database 

app = Flask(__name__)

create_database(app,os)

# ==========================================
# 2. IMPORTS DOS BLUEPRINTS (Apenas APÓS criar o banco)
# ==========================================
from routers.register import user_register
from routers.login import user_login
from routers.public import publics
from routers.client import client_bp

# ==========================================
# 3. REGISTRO DOS BLUEPRINTS
# ==========================================
app.register_blueprint(user_register, url_prefix='/register')
app.register_blueprint(user_login, url_prefix='/login')
app.register_blueprint(publics)
app.register_blueprint(client, url_prefix='/client')

if __name__ == "__main__":
    app.run(debug=True)
