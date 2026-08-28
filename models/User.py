import sqlite3
from flask import current_app


class User:
    def __init__(
        self,
        cpf,
        nome,
        sobrenome,
        telefone,
        email,
        senha,
        foto
    ):
        self.cpf = cpf
        self.nome = nome
        self.sobrenome = sobrenome
        self.telefone = telefone
        self.email = email
        self.senha = senha
        self.foto = foto

    # ============================================================
    # CONEXÃO COM O BANCO
    # ============================================================

    @staticmethod
    def conectar():
        """
        Cria uma conexão com o banco SQLite.
        O caminho do banco é obtido através da configuração
        DATABASE do Flask.
        """
        db_path = current_app.config['DATABASE']
        conexao = sqlite3.connect(
            db_path,
            check_same_thread=False
        )
        # Permite acessar as colunas pelo nome
        conexao.row_factory = sqlite3.Row
        return conexao

    # ============================================================
    # CREATE
    # ============================================================

    def salvar(self):
        """
        Cadastra um novo usuário.
        O CPF é a chave primária da tabela.
        Retorna:
            CPF do usuário cadastrado.
        Levanta:
            sqlite3.IntegrityError
            Caso o CPF ou e-mail já exista.
        """

        conexao = self.conectar()
        cursor = conexao.cursor()

        try:
            cursor.execute(
                '''
                INSERT INTO usuarios (
                    cpf,
                    nome,
                    sobrenome,
                    telefone,
                    email,
                    senha_hash,
                    foto_path
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
                ''',
                (
                    self.cpf,
                    self.nome,
                    self.sobrenome,
                    self.telefone,
                    self.email,
                    self.senha,
                    self.foto
                )
            )
            conexao.commit()
            return self.cpf

        except sqlite3.IntegrityError:
            conexao.rollback()
            raise

        finally:
            conexao.close()

    # ============================================================
    # READ - BUSCAR POR CPF
    # ============================================================

    @classmethod
    def buscar_por_cpf(cls, cpf):
        """
        Busca um usuário pelo CPF.
        Retorna:
            User -> usuário encontrado
            None -> usuário não encontrado
        """

        conexao = cls.conectar()
        cursor = conexao.cursor()

        try:
            cursor.execute(
                '''
                SELECT
                    cpf,
                    nome,
                    sobrenome,
                    telefone,
                    email,
                    senha_hash,
                    foto_path
                FROM usuarios
                WHERE cpf = ?
                ''',
                (cpf,)
            )
            usuario = cursor.fetchone()
            if usuario is None:
                return None
            return cls(
                cpf=usuario['cpf'],
                nome=usuario['nome'],
                sobrenome=usuario['sobrenome'],
                telefone=usuario['telefone'],
                email=usuario['email'],
                senha=usuario['senha_hash'],
                foto=usuario['foto_path']
            )

        finally:
            conexao.close()

    # ============================================================
    # READ - BUSCAR POR E-MAIL
    # ============================================================

    @classmethod
    def buscar_por_email(cls, email):
        """
        Busca um usuário pelo e-mail.
        Retorna:
            User -> usuário encontrado
            None -> usuário não encontrado
        """

        conexao = cls.conectar()
        cursor = conexao.cursor()

        try:
            cursor.execute(
                '''
                SELECT
                    cpf,
                    nome,
                    sobrenome,
                    telefone,
                    email,
                    senha_hash,
                    foto_path
                FROM usuarios
                WHERE email = ?
                ''',
                (email,)
            )
            usuario = cursor.fetchone()
            if usuario is None:
                return None

            return cls(
                cpf=usuario['cpf'],
                nome=usuario['nome'],
                sobrenome=usuario['sobrenome'],
                telefone=usuario['telefone'],
                email=usuario['email'],
                senha=usuario['senha_hash'],
                foto=usuario['foto_path']
            )

        finally:
            conexao.close()

    # ============================================================
    # READ - LISTAR TODOS
    # ============================================================

    @classmethod
    def listar_todos(cls):
        """
        Retorna todos os usuários cadastrados.
        Retorna:
            Lista de objetos User.
        """

        conexao = cls.conectar()
        cursor = conexao.cursor()

        try:
            cursor.execute(
                '''
                SELECT
                    cpf,
                    nome,
                    sobrenome,
                    telefone,
                    email,
                    senha_hash,
                    foto_path
                FROM usuarios
                ORDER BY nome ASC
                '''
            )

            usuarios = cursor.fetchall()
            lista = []

            for usuario in usuarios:
                lista.append(
                    cls(
                        cpf=usuario['cpf'],
                        nome=usuario['nome'],
                        sobrenome=usuario['sobrenome'],
                        telefone=usuario['telefone'],
                        email=usuario['email'],
                        senha=usuario['senha_hash'],
                        foto=usuario['foto_path']
                    )
                )
            return lista

        finally:
            conexao.close()

    # ============================================================
    # UPDATE
    # ============================================================

    def atualizar(self):
        """
        Atualiza os dados do usuário.
        O CPF é utilizado para localizar o registro
        e não é alterado.
        Retorna:
            True -> usuário atualizado
            False -> usuário não encontrado
        """

        conexao = self.conectar()
        cursor = conexao.cursor()

        try:
            cursor.execute(
                '''
                UPDATE usuarios
                SET
                    nome = ?,
                    sobrenome = ?,
                    telefone = ?,
                    email = ?,
                    senha_hash = ?,
                    foto_path = ?
                WHERE cpf = ?
                ''',
                (
                    self.nome,
                    self.sobrenome,
                    self.telefone,
                    self.email,
                    self.senha,
                    self.foto,
                    self.cpf
                )
            )
            conexao.commit()
            return cursor.rowcount > 0

        except sqlite3.IntegrityError:
            conexao.rollback()
            raise

        finally:
            conexao.close()

    # ============================================================
    # UPDATE - ATUALIZAÇÃO PARCIAL
    # ============================================================

    @classmethod
    def atualizar_por_cpf(cls, cpf, dados):
        """
        Atualiza apenas os campos enviados.
        O CPF é usado para localizar o usuário.
        O CPF não pode ser alterado através deste método.
        Exemplo:
            User.atualizar_por_cpf(
                '12345678900',
                {
                    'nome': 'João',
                    'telefone': '84999999999'
                }
            )

        Retorna:
            True -> usuário atualizado
            False -> nenhum campo válido ou usuário inexistente
        """
        campos_permitidos = {
            'nome',
            'sobrenome',
            'telefone',
            'email',
            'senha_hash',
            'foto_path'
        }

        campos = []
        valores = []
        for campo, valor in dados.items():

            if campo in campos_permitidos:
                campos.append(f'{campo} = ?')
                valores.append(valor)

        # Nenhum campo válido foi enviado
        if not campos:
            return False

        valores.append(cpf)
        conexao = cls.conectar()
        cursor = conexao.cursor()

        try:
            query = f'''
                UPDATE usuarios
                SET {', '.join(campos)}
                WHERE cpf = ?
            '''

            cursor.execute(query, valores)
            conexao.commit()
            return cursor.rowcount > 0

        except sqlite3.IntegrityError:
            conexao.rollback()
            raise

        finally:
            conexao.close()

    # ============================================================
    # DELETE - EXCLUIR POR CPF
    # ============================================================

    @classmethod
    def excluir_por_cpf(cls, cpf):
        """
        Exclui um usuário pelo CPF.
        Retorna:
            True -> usuário excluído
            False -> usuário não encontrado
        """

        conexao = cls.conectar()
        cursor = conexao.cursor()

        try:
            cursor.execute(
                '''
                DELETE FROM usuarios
                WHERE cpf = ?
                ''',
                (cpf,)
            )
            conexao.commit()
            return cursor.rowcount > 0

        finally:
            conexao.close()

    # ============================================================
    # VERIFICAR SE CPF EXISTE
    # ============================================================

    @classmethod
    def cpf_existe(cls, cpf):
        """
        Verifica se existe um usuário com determinado CPF.

        Retorna:
            True -> CPF existe
            False -> CPF não existe
        """

        conexao = cls.conectar()
        cursor = conexao.cursor()

        try:
            cursor.execute(
                '''
                SELECT 1
                FROM usuarios
                WHERE cpf = ?
                LIMIT 1
                ''',
                (cpf,)
            )
            return cursor.fetchone() is not None

        finally:
            conexao.close()

    # ============================================================
    # VERIFICAR SE E-MAIL EXISTE
    # ============================================================

    @classmethod
    def email_existe(cls, email):
        """
        Verifica se existe um usuário com determinado e-mail.
        Retorna:
            True -> e-mail existe
            False -> e-mail não existe
        """
        conexao = cls.conectar()
        cursor = conexao.cursor()
        try:
            cursor.execute(
                '''
                SELECT 1
                FROM usuarios
                WHERE email = ?
                LIMIT 1
                ''',
                (email,)
            )
            return cursor.fetchone() is not None
        finally:
            conexao.close()

    # ============================================================
    # CONVERTER PARA DICIONÁRIO
    # ============================================================

    def to_dict(self):
        """
        Converte o usuário para um dicionário.
        A senha NÃO é retornada por segurança.
        """
        return {
            'cpf': self.cpf,
            'nome': self.nome,
            'sobrenome': self.sobrenome,
            'telefone': self.telefone,
            'email': self.email,
            'foto': self.foto
        }

    # ============================================================
    # REPRESENTAÇÃO
    # ============================================================

    def __repr__(self):
        return (
            f'<User cpf={self.cpf} '
            f'nome={self.nome} '
            f'email={self.email}>'
        )
