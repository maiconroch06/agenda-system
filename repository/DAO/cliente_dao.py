
from sqlalchemy import text
from database import db
from models.cliente import Cliente
from datetime import datetime


class ClienteDAO:

    @staticmethod
    def salvar(cliente: Cliente):
        sql_usuario = text("""
            INSERT INTO usuarios (
                id,
                nome_completo,
                telefone,
                cpf,
                email,
                senha,
                foto_nome,
                status_usuario,
                data_cadastro,
                data_atualizacao,
                fk_id_endereco
            ) VALUES (
                :id,
                :nome_completo,
                :telefone,
                :cpf,
                :email,
                :senha,
                :foto_nome,
                :status_usuario,
                :data_cadastro,
                :data_atualizacao,
                :fk_id_endereco
            )
        """)

        sql_cliente = text("""
            INSERT INTO clientes (
                id,
                data_ultimo_servico
            ) VALUES (
                :id,
                :data_ultimo_servico
            )
        """)

        parametros_usuario = {
            "id": cliente.id,
            "nome_completo": cliente.nome_completo,
            "telefone": cliente.telefone,
            "cpf": cliente.cpf,
            "email": cliente.email,
            "senha": cliente.senha,
            "foto_nome": cliente.foto_nome,
            "status_usuario": cliente.status_usuario,
            "data_cadastro": cliente.data_cadastro,
            "data_atualizacao": cliente.data_atualizacao,
            "fk_id_endereco": cliente.fk_id_endereco
        }

        parametros_cliente = {
            "id": cliente.id,
            "data_ultimo_servico": cliente.data_ultimo_servico
        }

        db.session.execute(sql_usuario, parametros_usuario)
        db.session.execute(sql_cliente, parametros_cliente)
        db.session.flush()

        return cliente.id

    @staticmethod
    def buscar_por_id(id_cliente: int):
        sql = text("""
            SELECT
                u.id,
                u.nome_completo,
                u.telefone,
                u.cpf,
                u.email,
                u.senha,
                u.foto_nome,
                u.status_usuario,
                u.data_cadastro,
                u.data_atualizacao,
                u.fk_id_endereco,
                c.data_ultimo_servico
            FROM usuarios u
            INNER JOIN clientes c ON c.id = u.id
            WHERE c.id = :id_cliente
        """)

        registro = db.session.execute(
            sql,
            {"id_cliente": id_cliente}
        ).mappings().first()

        if registro is None:
            return None

        return ClienteDAO._mapear(registro)

    @staticmethod
    def listar_todos():
        sql = text("""
            SELECT
                u.id,
                u.nome_completo,
                u.telefone,
                u.cpf,
                u.email,
                u.senha,
                u.foto_nome,
                u.status_usuario,
                u.data_cadastro,
                u.data_atualizacao,
                u.fk_id_endereco,
                c.data_ultimo_servico
            FROM usuarios u
            INNER JOIN clientes c ON c.id = u.id
            ORDER BY u.nome_completo
        """)

        registros = db.session.execute(sql).mappings().all()

        return [
            ClienteDAO._mapear(registro)
            for registro in registros
        ]

    @staticmethod
    def atualizar(cliente: Cliente):
        sql_usuario = text("""
            UPDATE usuarios
            SET
                nome_completo = :nome_completo,
                telefone = :telefone,
                cpf = :cpf,
                email = :email,
                senha = :senha,
                foto_nome = :foto_nome,
                status_usuario = :status_usuario,
                data_atualizacao = :data_atualizacao,
                fk_id_endereco = :fk_id_endereco
            WHERE id = :id
        """)

        sql_cliente = text("""
            UPDATE clientes
            SET data_ultimo_servico = :data_ultimo_servico
            WHERE id = :id
        """)

        parametros = {
            "id": cliente.id,
            "nome_completo": cliente.nome_completo,
            "telefone": cliente.telefone,
            "cpf": cliente.cpf,
            "email": cliente.email,
            "senha": cliente.senha,
            "foto_nome": cliente.foto_nome,
            "status_usuario": cliente.status_usuario,
            "data_atualizacao": cliente.data_atualizacao,
            "fk_id_endereco": cliente.fk_id_endereco,
            "data_ultimo_servico": cliente.data_ultimo_servico
        }

        resultado_usuario = db.session.execute(
            sql_usuario, parametros
        )

        if resultado_usuario.rowcount == 0:
            return False

        resultado_cliente = db.session.execute(
            sql_cliente, parametros
        )

        db.session.flush()

        return resultado_cliente.rowcount > 0

    @staticmethod
    def excluir(id_cliente: int):
        sql = text("""
            DELETE FROM clientes
            WHERE id = :id_cliente
        """)

        resultado = db.session.execute(
            sql,
            {"id_cliente": id_cliente}
        )

        if resultado.rowcount == 0:
            return False

        sql_usuario = text("""
            DELETE FROM usuarios
            WHERE id = :id_cliente
        """)

        db.session.execute(
            sql_usuario,
            {"id_cliente": id_cliente}
        )

        db.session.flush()

        return True

    @staticmethod
    def atualizar_data_ultimo_servico(
        id_cliente: int,
        data: datetime
    ):
        sql = text("""
            UPDATE clientes
            SET data_ultimo_servico = :data
            WHERE id = :id_cliente
        """)

        resultado = db.session.execute(sql, {
            "id_cliente": id_cliente,
            "data": data
        })

        db.session.flush()

        return resultado.rowcount > 0

    @staticmethod
    def _mapear(registro):
        return Cliente(
            id=registro["id"],
            nome_completo=registro["nome_completo"],
            telefone=registro["telefone"],
            cpf=registro["cpf"],
            email=registro["email"],
            senha=registro["senha"],
            foto_nome=registro["foto_nome"],
            status_usuario=bool(registro["status_usuario"]),
            data_cadastro=registro["data_cadastro"],
            data_atualizacao=registro["data_atualizacao"],
            fk_id_endereco=registro["fk_id_endereco"],
            data_ultimo_servico=registro["data_ultimo_servico"]
        )
