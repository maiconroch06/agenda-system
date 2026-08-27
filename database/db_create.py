import sqlite3

def create_database(app, os,):
    app.secret_key = os.getenv('SECRET_KEY', 'teste321')

    # ==========================================
    # 1. CRIAÇÃO AUTOMÁTICA DO BANCO E TABELAS (Executa Primeiro)
    # ==========================================
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DATABASE_PATH = os.path.join(BASE_DIR, 'banco.db')

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
