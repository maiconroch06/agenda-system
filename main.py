import os
import sqlite3
from flask import Flask 

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'teste321')

# ==========================================
# 1. CRIAÇÃO AUTOMÁTICA DO BANCO E TABELAS (Executa Primeiro)
# ==========================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_PATH = os.path.join(BASE_DIR, 'database', 'banco.db')

# Salva o caminho dentro da configuração oficial do Flask
app.config['DATABASE'] = DATABASE_PATH

# Garante que a pasta database exista fisicamente
os.makedirs(os.path.dirname(DATABASE_PATH), exist_ok=True)

# Cria e estrutura o banco imediatamente
conexao = sqlite3.connect(DATABASE_PATH, check_same_thread=False)
cursor = conexao.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS usuarios (
        cpf VARCHAR(14) PRIMARY KEY NOT NULL,
        nome TEXT NOT NULL,
        sobrenome TEXT NOT NULL,
        telefone VARCHAR(15),
        email VARCHAR(255) NOT NULL UNIQUE,
        senha_hash TEXT NOT NULL,
        foto_path TEXT
    )
''')

# Habilita o suporte a chaves estrangeiras
cursor.execute("PRAGMA foreign_keys = ON;")

cursor.execute('''
    CREATE TABLE IF NOT EXISTS enderecos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cep VARCHAR(9) NOT NULL,
        cidade VARCHAR(100) NOT NULL,
        estado_sigla VARCHAR(2) NOT NULL,
        logradouro TEXT NOT NULL,
        numero INTEGER NOT NULL,
        bairro VARCHAR(100) NOT NULL,
        sequencia TEXT,
        complemento TEXT,
        usuario_cpf VARCHAR(14) NOT NULL,
        FOREIGN KEY (usuario_cpf) REFERENCES usuarios (cpf) ON DELETE CASCADE
    )
''')
conexao.commit()
conexao.close()

# ==========================================
# 2. IMPORTS DOS BLUEPRINTS (Apenas APÓS criar o banco)
# ==========================================
from routers.register import user_register
from routers.public import publics
from routers.customer_bp import customer_bp


# ==========================================
# 3. REGISTRO DOS BLUEPRINTS
# ==========================================
app.register_blueprint(user_register, url_prefix='/register')
app.register_blueprint(publics)
app.register_blueprint(customer_bp, url_prefix='/customer')

if __name__ == "__main__":
    app.run(debug=True)
