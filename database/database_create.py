from flask_sqlalchemy import SQLAlchemy
import pymysql

db = SQLAlchemy()

class Database_create:
    USUARIO = 'dev_barbearia'
    SENHA = '' 
    SERVIDOR = 'localhost'
    PORTA = 3306
    BANCO = 'databasetmsbarbearia'

    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{USUARIO}:{SENHA}@{SERVIDOR}:{PORTA}/{BANCO}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'teste321'

def create_database(app):
    
    #Para criar o banco o usuario dev_barbearia deve esta com os privilegios de root
        
    conexao = pymysql.connect(
        host=Database_create.SERVIDOR,
        user=Database_create.USUARIO,
        password=Database_create.SENHA,
        port= Database_create.PORTA
    )

    with conexao.cursor() as cursor:
        cursor.execute(
            f'CREATE DATABASE IF NOT EXISTS {Database_create.BANCO}'
        )

    conexao.close()
        
    # Carrega as configurações da classe para o Flask
    app.config.from_object(Database_create)
    
    # Inicializa o SQLAlchemy atrelando-o ao app
    db.init_app(app)