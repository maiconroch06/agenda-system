import sqlite3
from contextlib import contextmanager
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
        sequencia=1,  
        complemento=None
    ):
        self.cep = cep
        self.cidade = cidade
        self.estado_sigla = estado_sigla
        self.logradouro = logradouro
        self.numero = numero
        self.bairro = bairro
        self.usuario_cpf = usuario_cpf
        self.sequencia = sequencia
        self.complemento = complemento

    # ============================================================
    # CONVERSÃO PARA DICIONÁRIO
    # ============================================================
    def to_dict(self):
        """
        Retorna os dados do endereço em formato de dicionário limpo.
        Útil para salvar em sessões HTTP ou retornar respostas em JSON.
        """
        return {
            'cep': self.cep,
            'cidade': self.cidade,
            'estado_sigla': self.estado_sigla,
            'logradouro': self.logradouro,
            'numero': self.numero,
            'bairro': self.bairro,
            'usuario_cpf': self.usuario_cpf,
            'sequencia': self.sequencia,
            'complemento': self.complemento
        }

    # ============================================================
    # GERENCIADOR DE CONEXÃO CENTRALIZADO
    # ============================================================

    @classmethod
    @contextmanager
    def abrir_banco(cls):
        """
        Gerencia automaticamente a abertura, commit e fechamento do banco SQLite.
        Ativa automaticamente as chaves estrangeiras (Foreign Keys).
        """
        db_path = current_app.config['DATABASE']
        conexao = sqlite3.connect(db_path, check_same_thread=False)
        conexao.row_factory = sqlite3.Row
        
        conexao.execute("PRAGMA foreign_keys = ON")
        
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
        """
        Cadastra um novo endereço usando o contexto automatizado.
        """
        with self.abrir_banco() as cursor:
            cursor.execute(
                '''
                INSERT INTO enderecos (
                    cep, cidade, estado_sigla, logradouro, numero, bairro, sequencia, complemento, usuario_cpf
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''',
                (
                    self.cep, self.cidade, self.estado_sigla, self.logradouro, self.numero, 
                    self.bairro, self.sequencia, self.complemento, self.usuario_cpf
                )
            )
            return self.sequencia

    # ============================================================
    # READ - BUSCAR POR CPF + SEQUÊNCIA
    # ============================================================

    @classmethod
    def buscar_por_cpf_e_sequencia(cls, usuario_cpf, sequencia):
        """
        Busca um endereço específico de um usuário baseado na PK composta.
        """
        with cls.abrir_banco() as cursor:
            cursor.execute(
                '''
                SELECT cep, cidade, estado_sigla, logradouro, numero, bairro, sequencia, complemento, usuario_cpf
                FROM enderecos
                WHERE usuario_cpf = ? AND sequencia = ?
                ''',
                (usuario_cpf, sequencia)
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
                usuario_cpf=endereco['usuario_cpf'],
                sequencia=endereco['sequencia'],
                complemento=endereco['complemento']
            )

    # ============================================================
    # READ - LISTAR ENDEREÇOS DO USUÁRIO
    # ============================================================

    @classmethod
    def listar_por_usuario(cls, usuario_cpf):
        """
        Lista todos os endereços vinculados a um determinado usuário.
        """
        with cls.abrir_banco() as cursor:
            cursor.execute(
                '''
                SELECT cep, cidade, estado_sigla, logradouro, numero, bairro, sequencia, complemento, usuario_cpf
                FROM enderecos
                WHERE usuario_cpf = ?
                ORDER BY sequencia ASC
                ''',
                (usuario_cpf,)
            )
            enderecos = cursor.fetchall()
            
            return [
                cls(
                    cep=e['cep'],
                    cidade=e['cidade'],
                    estado_sigla=e['estado_sigla'],
                    logradouro=e['logradouro'],
                    numero=e['numero'],
                    bairro=e['bairro'],
                    usuario_cpf=e['usuario_cpf'],
                    sequencia=e['sequencia'],
                    complemento=e['complemento']
                ) for e in enderecos
            ]

    # ============================================================
    # READ - LISTAR TODOS
    # ============================================================

    @classmethod
    def listar_todos(cls):
        """
        Lista absolutamente todos os endereços cadastrados no banco.
        """
        with cls.abrir_banco() as cursor:
            cursor.execute(
                '''
                SELECT cep, cidade, estado_sigla, logradouro, numero, bairro, sequencia, complemento, usuario_cpf
                FROM enderecos
                ORDER BY usuario_cpf ASC, sequencia ASC
                '''
            )
            enderecos = cursor.fetchall()
            
            return [
                cls(
                    cep=e['cep'],
                    cidade=e['cidade'],
                    estado_sigla=e['estado_sigla'],
                    logradouro=e['logradouro'],
                    numero=e['numero'],
                    bairro=e['bairro'],
                    usuario_cpf=e['usuario_cpf'],
                    sequencia=e['sequencia'],
                    complemento=e['complemento']
                ) for e in enderecos
            ]

    # ============================================================
    # UPDATE
    # ============================================================

    def atualizar(self):
        """
        Atualiza as informações do endereço com base na combinação única de CPF + Sequência.
        """
        with self.abrir_banco() as cursor:
            cursor.execute(
                '''
                UPDATE enderecos
                SET cep = ?, cidade = ?, estado_sigla = ?, logradouro = ?, numero = ?, bairro = ?, complemento = ?
                WHERE usuario_cpf = ? AND sequencia = ?
                ''',
                (
                    self.cep, self.cidade, self.estado_sigla, self.logradouro, self.numero, 
                    self.bairro, self.complemento, self.usuario_cpf, self.sequencia
                )
            )
            return cursor.rowcount > 0

    # ============================================================
    # DELETE
    # ============================================================

    @classmethod
    def excluir_por_cpf_e_sequencia(cls, usuario_cpf, sequencia):
        """
        Remove um endereço específico de um usuário.
        """
        with cls.abrir_banco() as cursor:
            cursor.execute(
                'DELETE FROM enderecos WHERE usuario_cpf = ? AND sequencia = ?',
                (usuario_cpf, sequencia)
            )
            return cursor.rowcount > 0