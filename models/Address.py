import sqlite3
from flask import current_app

class Endereco:
    def __init__(self, cep, cidade, estado_sigla, logradouro, numero, bairro, usuario_cpf, sequencia=None, complemento=None):
        self.cep = cep
        self.cidade = cidade
        self.estado_sigla = estado_sigla
        self.logradouro = logradouro
        self.numero = numero
        self.bairro = bairro
        self.sequencia = sequencia
        self.complemento = complemento
        self.usuario_cpf = usuario_cpf  

    def salvar(self):
        """Insere o endereço no banco de dados SQLite usando o contexto do Flask."""
        db_path = current_app.config['DATABASE']
        
        conexao = sqlite3.connect(db_path, check_same_thread=False)
        cursor = conexao.cursor()

        # Garante chaves estrangeiras ativas nesta conexão
        cursor.execute("PRAGMA foreign_keys = ON;")

        cursor.execute('''
            INSERT INTO enderecos (
                cep, cidade, estado_sigla, logradouro, numero, bairro, sequencia, complemento, usuario_cpf
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            self.cep, self.cidade, self.estado_sigla, self.logradouro, 
            self.numero, self.bairro, self.sequencia, self.complemento, self.usuario_cpf
        ))

        conexao.commit()
        conexao.close()
