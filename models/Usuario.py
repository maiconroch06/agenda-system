import sqlite3
from flask import current_app

class Usuario:
    def __init__(self, cpf, nome, sobrenome, telefone, email, senha, foto):
        self.cpf = cpf
        self.nome = nome
        self.sobrenome = sobrenome
        self.telefone = telefone
        self.email = email
        self.senha = senha  
        self.foto = foto

    def salvar(self):  
        """Insere o usuário no banco de dados SQLite usando o contexto do Flask."""
        # Busca o caminho absoluto exato configurado no main.py
        db_path = current_app.config['DATABASE']
        
        conexao = sqlite3.connect(db_path, check_same_thread=False)
        cursor = conexao.cursor()

        cursor.execute('''
            INSERT INTO usuarios (cpf, nome, sobrenome, telefone, email, senha_hash, foto_path)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (self.cpf, self.nome, self.sobrenome, self.telefone, self.email, self.senha, self.foto))

        conexao.commit()
        conexao.close()
