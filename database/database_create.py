from flask_sqlalchemy import SQLAlchemy
import pymysql

db = SQLAlchemy()

class Database_create:
    USUARIO = 'dev_barbearia'
    SENHA = ''
    SERVIDOR = 'localhost'
    PORTA = 3306
    BANCO = 'databasetmsbarbearia'

    SQLALCHEMY_DATABASE_URI = (
        f'mysql+pymysql://{USUARIO}:{SENHA}'
        f'@{SERVIDOR}:{PORTA}/{BANCO}'
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'teste321'


def create_database(app):
    # Carrega as configurações no Flask
    app.config.from_object(Database_create)

    conexao = None

    try:
        # Conecta ao servidor MySQL, sem selecionar um banco específico
        conexao = pymysql.connect(
            host=Database_create.SERVIDOR,
            user=Database_create.USUARIO,
            password=Database_create.SENHA,
            port=Database_create.PORTA,
            connect_timeout=5
        )

        with conexao.cursor() as cursor:
            cursor.execute(
                """
                SELECT SCHEMA_NAME
                FROM INFORMATION_SCHEMA.SCHEMATA
                WHERE SCHEMA_NAME = %s
                """,
                (Database_create.BANCO,)
            )

            resultado = cursor.fetchone()

        # Verifica se o banco existe
        if resultado is None:
            raise RuntimeError(
                f"O banco de dados '{Database_create.BANCO}' não existe."
            )

        # Inicializa o SQLAlchemy somente se o banco existir
        db.init_app(app)

        return True

    except pymysql.err.OperationalError as erro:
        codigo_erro = erro.args[0] if erro.args else None

        if codigo_erro == 1045:
            raise RuntimeError(
                "Acesso negado ao MySQL. Verifique o usuário e a senha."
            ) from erro

        if codigo_erro == 2003:
            raise RuntimeError(
                "Não foi possível conectar ao servidor MySQL. "
                "Verifique se o serviço está em execução."
            ) from erro

        raise RuntimeError(
            f"Erro operacional ao conectar ao MySQL: {erro}"
        ) from erro

    except pymysql.MySQLError as erro:
        raise RuntimeError(
            f"Erro ao verificar o banco de dados: {erro}"
        ) from erro

    finally:
        if conexao is not None:
            conexao.close()
