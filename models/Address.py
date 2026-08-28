import sqlite3
from flask import current_app


class Address:
    def __init__(
        self,
        cep,
        cidade,
        estado_sigla,
        logradouro,
        numero,
        bairro,
        usuario_cpf,
        sequencia=None,
        complemento=None
    ):
        self.cep = cep
        self.cidade = cidade
        self.estado_sigla = estado_sigla
        self.logradouro = logradouro
        self.numero = numero
        self.bairro = bairro
        self.sequencia = sequencia
        self.complemento = complemento
        self.usuario_cpf = usuario_cpf

    # ============================================================
    # CONEXÃO COM O BANCO
    # ============================================================

    @staticmethod
    def conectar():
        """
        Cria uma conexão com o banco SQLite.
        O caminho do banco é obtido através da configuração
        DATABASE do Flask.
        As chaves estrangeiras são ativadas nesta conexão.
        """

        db_path = current_app.config['DATABASE']

        conexao = sqlite3.connect(
            db_path,
            check_same_thread=False
        )

        # Permite acessar as colunas pelo nome
        conexao.row_factory = sqlite3.Row
        # Ativa as chaves estrangeiras
        conexao.execute("PRAGMA foreign_keys = ON")

        return conexao

    # ============================================================
    # CREATE
    # ============================================================

    def salvar(self):
        """
        Cadastra um novo endereço.
        Retorna:
            A sequência do endereço cadastrado.

        Levanta:
            sqlite3.IntegrityError
            Caso o usuário não exista ou a combinação
            CPF + sequência já exista.
        """

        conexao = self.conectar()
        cursor = conexao.cursor()

        try:
            cursor.execute(
                '''
                INSERT INTO enderecos (
                    cep,
                    cidade,
                    estado_sigla,
                    logradouro,
                    numero,
                    bairro,
                    sequencia,
                    complemento,
                    usuario_cpf
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''',
                (
                    self.cep,
                    self.cidade,
                    self.estado_sigla,
                    self.logradouro,
                    self.numero,
                    self.bairro,
                    self.sequencia,
                    self.complemento,
                    self.usuario_cpf
                )
            )
            conexao.commit()
            return self.sequencia

        except sqlite3.IntegrityError:
            conexao.rollback()
            raise

        finally:
            conexao.close()

    # ============================================================
    # READ - BUSCAR POR CPF + SEQUÊNCIA
    # ============================================================

    @classmethod
    def buscar_por_cpf_e_sequencia(cls, usuario_cpf, sequencia):
        """
        Busca um endereço específico de um usuário.
        A combinação:
            usuario_cpf + sequencia
        identifica o endereço.
        Retorna:
            Address -> endereço encontrado
            None -> endereço não encontrado
        """

        conexao = cls.conectar()
        cursor = conexao.cursor()

        try:
            cursor.execute(
                '''
                SELECT
                    cep,
                    cidade,
                    estado_sigla,
                    logradouro,
                    numero,
                    bairro,
                    sequencia,
                    complemento,
                    usuario_cpf
                FROM enderecos
                WHERE usuario_cpf = ?
                  AND sequencia = ?
                ''',
                (
                    usuario_cpf,
                    sequencia
                )
            )

            endereco = cursor.fetchone()

            if endereco is None:
                return None

            return cls(
                cep=endereco['cep'],
                cidade=endereco['cidade'],
                estado_sigla=endereco['estado_sigla'],
                logradouro=endereco['logradouro'],
                numero=endereco['numero'],
                bairro=endereco['bairro'],
                sequencia=endereco['sequencia'],
                complemento=endereco['complemento'],
                usuario_cpf=endereco['usuario_cpf']
            )

        finally:
            conexao.close()

    # ============================================================
    # READ - LISTAR ENDEREÇOS DO USUÁRIO
    # ============================================================

    @classmethod
    def listar_por_usuario(cls, usuario_cpf):
        """
        Lista todos os endereços de um determinado usuário.
        Retorna:
            Lista de objetos Address.
        """

        conexao = cls.conectar()
        cursor = conexao.cursor()

        try:
            cursor.execute(
                '''
                SELECT
                    cep,
                    cidade,
                    estado_sigla,
                    logradouro,
                    numero,
                    bairro,
                    sequencia,
                    complemento,
                    usuario_cpf
                FROM enderecos
                WHERE usuario_cpf = ?
                ORDER BY sequencia ASC
                ''',
                (usuario_cpf,)
            )

            enderecos = cursor.fetchall()

            lista = []

            for endereco in enderecos:
                lista.append(
                    cls(
                        cep=endereco['cep'],
                        cidade=endereco['cidade'],
                        estado_sigla=endereco['estado_sigla'],
                        logradouro=endereco['logradouro'],
                        numero=endereco['numero'],
                        bairro=endereco['bairro'],
                        sequencia=endereco['sequencia'],
                        complemento=endereco['complemento'],
                        usuario_cpf=endereco['usuario_cpf']
                    )
                )

            return lista

        finally:
            conexao.close()

    # ============================================================
    # READ - LISTAR TODOS
    # ============================================================

    @classmethod
    def listar_todos(cls):
        """
        Lista todos os endereços cadastrados.
        Retorna:
            Lista de objetos Address.
        """

        conexao = cls.conectar()
        cursor = conexao.cursor()

        try:
            cursor.execute(
                '''
                SELECT
                    cep,
                    cidade,
                    estado_sigla,
                    logradouro,
                    numero,
                    bairro,
                    sequencia,
                    complemento,
                    usuario_cpf
                FROM enderecos
                ORDER BY usuario_cpf ASC, sequencia ASC
                '''
            )

            enderecos = cursor.fetchall()

            lista = []

            for endereco in enderecos:
                lista.append(
                    cls(
                        cep=endereco['cep'],
                        cidade=endereco['cidade'],
                        estado_sigla=endereco['estado_sigla'],
                        logradouro=endereco['logradouro'],
                        numero=endereco['numero'],
                        bairro=endereco['bairro'],
                        sequencia=endereco['sequencia'],
                        complemento=endereco['complemento'],
                        usuario_cpf=endereco['usuario_cpf']
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
        Atualiza um endereço.
        O endereço é localizado através de:
            usuario_cpf + sequencia
        O CPF e a sequência não são alterados.
        Retorna:
            True -> endereço atualizado
            False -> endereço não encontrado
        """

        if self.sequencia is None:
            raise ValueError(
                'A sequência é obrigatória para atualizar um endereço.'
            )

        conexao = self.conectar()
        cursor = conexao.cursor()

        try:
            cursor.execute(
                '''
                UPDATE enderecos
                SET
                    cep = ?,
                    cidade = ?,
                    estado_sigla = ?,
                    logradouro = ?,
                    numero = ?,
                    bairro = ?,
                    complemento = ?
                WHERE usuario_cpf = ?
                  AND sequencia = ?
                ''',
                (
                    self.cep,
                    self.cidade,
                    self.estado_sigla,
                    self.logradouro,
                    self.numero,
                    self.bairro,
                    self.complemento,
                    self.usuario_cpf,
                    self.sequencia
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
    def atualizar_por_cpf_e_sequencia(
        cls,
        usuario_cpf,
        sequencia,
        dados
    ):
        """
        Atualiza apenas os campos enviados.
        O CPF e a sequência não podem ser alterados.
        Exemplo:

            Address.atualizar_por_cpf_e_sequencia(
                '12345678900',
                1,
                {
                    'cep': '59000000',
                    'numero': '200'
                }
            )
        Retorna:
            True -> endereço atualizado
            False -> nenhum campo válido ou endereço inexistente
        """

        campos_permitidos = {
            'cep',
            'cidade',
            'estado_sigla',
            'logradouro',
            'numero',
            'bairro',
            'complemento'
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

        valores.append(usuario_cpf)
        valores.append(sequencia)

        conexao = cls.conectar()
        cursor = conexao.cursor()

        try:
            query = f'''
                UPDATE enderecos
                SET {', '.join(campos)}
                WHERE usuario_cpf = ?
                  AND sequencia = ?
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
    # DELETE - EXCLUIR ENDEREÇO
    # ============================================================

    @classmethod
    def excluir_por_cpf_e_sequencia(
        cls,
        usuario_cpf,
        sequencia
    ):
        """
        Exclui um endereço específico de um usuário.
        Retorna:
            True -> endereço excluído
            False -> endereço não encontrado
        """

        conexao = cls.conectar()
        cursor = conexao.cursor()

        try:
            cursor.execute(
                '''
                DELETE FROM enderecos
                WHERE usuario_cpf = ?
                  AND sequencia = ?
                ''',
                (
                    usuario_cpf,
                    sequencia
                )
            )

            conexao.commit()

            return cursor.rowcount > 0

        finally:
            conexao.close()

    # ============================================================
    # DELETE - EXCLUIR TODOS OS ENDEREÇOS DO USUÁRIO
    # ============================================================

    @classmethod
    def excluir_por_usuario(cls, usuario_cpf):
        """
        Exclui todos os endereços pertencentes a um usuário.
        Retorna:
            Quantidade de endereços excluídos.
        """

        conexao = cls.conectar()
        cursor = conexao.cursor()

        try:
            cursor.execute(
                '''
                DELETE FROM enderecos
                WHERE usuario_cpf = ?
                ''',
                (usuario_cpf,)
            )

            conexao.commit()
            return cursor.rowcount

        finally:
            conexao.close()

    # ============================================================
    # VERIFICAR EXISTÊNCIA
    # ============================================================

    @classmethod
    def existe(cls, usuario_cpf, sequencia):
        """
        Verifica se um endereço existe.
        Retorna:
            True -> endereço existe
            False -> endereço não existe
        """

        conexao = cls.conectar()
        cursor = conexao.cursor()

        try:
            cursor.execute(
                '''
                SELECT 1
                FROM enderecos
                WHERE usuario_cpf = ?
                  AND sequencia = ?
                LIMIT 1
                ''',
                (
                    usuario_cpf,
                    sequencia
                )
            )
            return cursor.fetchone() is not None

        finally:
            conexao.close()

    # ============================================================
    # CONVERTER PARA DICIONÁRIO
    # ============================================================

    def to_dict(self):
        """
        Converte o endereço para um dicionário.
        """

        return {
            'cep': self.cep,
            'cidade': self.cidade,
            'estado_sigla': self.estado_sigla,
            'logradouro': self.logradouro,
            'numero': self.numero,
            'bairro': self.bairro,
            'sequencia': self.sequencia,
            'complemento': self.complemento,
            'usuario_cpf': self.usuario_cpf
        }

    # ============================================================
    # REPRESENTAÇÃO
    # ============================================================

    def __repr__(self):
        return (
            f'<Address '
            f'usuario_cpf={self.usuario_cpf} '
            f'sequencia={self.sequencia} '
            f'cep={self.cep}>'
        )
