
from flask import Flask, session
from datetime import timedelta
from database import create_database
# from database.seed import initialize

app = Flask(__name__)

# 1. Verifica se o banco existe e configura o SQLAlchemy
try:
    create_database(app)
    print("Banco de dados verificado com sucesso.")

except RuntimeError as erro:
    print(f"ERRO AO INICIALIZAR O BANCO: {erro}")
    raise SystemExit(1)


# 2. Importa os modelos
from models import *


# 3. Inicializa os dados padrão
# Não cria tabelas automaticamente.
# with app.app_context():
#     initialize()


# 4. Importa os Blueprints
from routers.public_route import publics
from routers.cliente_route import cliente
from routers.gestor_route import gestor
from routers.barbeiro_route import barbeiro


# 5. Registra os Blueprints
app.register_blueprint(publics)
app.register_blueprint(cliente, url_prefix='/cliente')
app.register_blueprint(gestor, url_prefix='/gestor')
app.register_blueprint(barbeiro, url_prefix='/barbeiro')


# 6. Configurações da aplicação
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)
app.config['UPLOAD_FILES'] = r'static/assets/dados'


if __name__ == "__main__":
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )
