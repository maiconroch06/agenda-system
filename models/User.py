import sqlite3
from contextlib import contextmanager
from flask import current_app


class User:
    # CONSTRUTOR FLEXÍVEL: CPF no final e opcional
    def __init__(self, nome, sobrenome, telefone, email, senha, foto, cpf=None):
        self.cpf = cpf
        self.nome = nome
        self.sobrenome = sobrenome
        self.telefone = telefone
        self.email = email
        self.senha = senha
        self.foto = foto

    def to_dict(self):
        return {
            'cpf': self.cpf,
            'nome': self.nome,
            'sobrenome': self.sobrenome,
            'telefone': self.telefone,
            'email': self.email,
            'senha': self.senha,
            'foto': self.foto
        }

    # ============================================================
    # GERENCIADOR DE CONEXÃO CENTRALIZADO
    # ============================================================

    @classmethod
    @contextmanager
    def abrir_banco(cls):
        db_path = current_app.config['DATABASE']
        conexao = sqlite3.connect(db_path, check_same_thread=False)
        conexao.row_factory = sqlite3.Row
        cursor = conexao.cursor()
        try:
            yield cursor  
            conexao.commit()  
        except sqlite3.IntegrityError:
            conexao.rollback()  
            raise
        finally:
            conexao.close()  

    # ============================================================
    # CREATE
    # ============================================================

    def salvar(self):
        with self.abrir_banco() as cursor:
            cursor.execute(
                '''
                INSERT INTO usuarios (
                    cpf, nome, sobrenome, telefone, email, senha_hash, foto_path
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
                ''',
                (self.cpf, self.nome, self.sobrenome, self.telefone, self.email, self.senha, self.foto)
            )
            return self.cpf

    # ============================================================
    # READ - BUSCAR POR CPF
    # ============================================================

    @classmethod
    def buscar_por_cpf(cls, cpf):
        with cls.abrir_banco() as cursor:
            cursor.execute(
                '''
                SELECT cpf, nome, sobrenome, telefone, email, senha_hash, foto_path
                FROM usuarios WHERE cpf = ?
                ''',
                (cpf,)
            )
            usuario = cursor.fetchone()
            if usuario is None:
                return None
                
            # CORREÇÃO: Usando argumentos explicitamente nomeados para evitar desalinhamento
            return cls(
                nome=usuario['nome'],
                sobrenome=usuario['sobrenome'],
                telefone=usuario['telefone'],
                email=usuario['email'],
                senha=usuario['senha_hash'],
                foto=usuario['foto_path'],
                cpf=usuario['cpf']
            )

    # ============================================================
    # READ - BUSCAR POR E-MAIL
    # ============================================================

    @classmethod
    def buscar_por_email(cls, email):
        with cls.abrir_banco() as cursor:
            cursor.execute(
                '''
                SELECT cpf, nome, sobrenome, telefone, email, senha_hash, foto_path
                FROM usuarios WHERE email = ?
                ''',
                (email,)
            )
            usuario = cursor.fetchone()
            if usuario is None:
                return None

            # CORREÇÃO: Usando argumentos explicitamente nomeados
            return cls(
                nome=usuario['nome'],
                sobrenome=usuario['sobrenome'],
                telefone=usuario['telefone'],
                email=usuario['email'],
                senha=usuario['senha_hash'],
                foto=usuario['foto_path'],
                cpf=usuario['cpf']
            )

    # ============================================================
    # READ - LISTAR TODOS
    # ============================================================

    @classmethod
    def listar_todos(cls):
        with cls.abrir_banco() as cursor:
            cursor.execute(
                '''
                SELECT cpf, nome, sobrenome, telefone, email, senha_hash, foto_path
                FROM usuarios ORDER BY nome ASC
                '''
            )
            usuarios = cursor.fetchall()
            
            # CORREÇÃO: Alinhando os parâmetros nomeados na listagem por list comprehension
            return [
                cls(
                    nome=u['nome'],
                    sobrenome=u['sobrenome'],
                    telefone=u['telefone'],
                    email=u['email'],
                    senha=u['senha_hash'],
                    foto=u['foto_path'],
                    cpf=u['cpf']
                ) for u in usuarios
            ]

    # ============================================================
    # UPDATE
    # ============================================================

    def atualizar(self):
        if not self.cpf:
            return False

        with self.abrir_banco() as cursor:
            cursor.execute(
                '''
                UPDATE usuarios
                SET nome = ?, sobrenome = ?, telefone = ?, email = ?, senha_hash = ?, foto_path = ?
                WHERE cpf = ?
                ''',
                (self.nome, self.sobrenome, self.telefone, self.email, self.senha, self.foto, self.cpf)
            )
            return cursor.rowcount > 0

    # ============================================================
    # DELETE
    # ============================================================

    @classmethod
    def excluir_por_cpf(cls, cpf):
        with cls.abrir_banco() as cursor:
            cursor.execute('DELETE FROM usuarios WHERE cpf = ?', (cpf,))
            return cursor.rowcount > 0