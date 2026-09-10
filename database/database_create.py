from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Database_create:
    USUARIO = 'dev_barbearia'
    SENHA = '' 
    SERVIDOR = 'localhost'
    PORTA = '3306'
    BANCO = 'databasetmsbarbearia'

    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{USUARIO}:{SENHA}@{SERVIDOR}:{PORTA}/{BANCO}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'teste321'

def create_database(app):
    # Carrega as configurações da classe para o Flask
    app.config.from_object(Database_create)
    
    # Inicializa o SQLAlchemy atrelando-o ao app
    db.init_app(app)