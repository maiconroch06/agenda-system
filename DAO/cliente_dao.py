
from sqlalchemy import text
from database import db
from models import Cliente
from datetime import datetime


class ClienteDAO:

    def cadastrar(self, id_cliente: int, data_ultimo_servico: datetime = None):
        sql = text("""
            INSERT INTO cliente (
                id_cliente,
                data_ultimo_servico
            ) VALUES (
                :id_cliente,
                :data_ultimo_servico
            )
        """)

        resultado = db.session.execute(sql, {
            "id_cliente": id_cliente,
            "data_ultimo_servico": data_ultimo_servico
        })

        db.session.commit()

        return resultado.rowcount > 0

    def consultarClienteId(self, id_cliente: int):
        sql = text("""
            SELECT
                u.id_usuario,
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
                c.id_cliente,
                c.data_ultimo_servico
            FROM usuario u
            INNER JOIN cliente c
                ON c.id_cliente = u.id_usuario
            WHERE c.id_cliente = :id_cliente
        """)

        registro = db.session.execute(
            sql,
            {"id_cliente": id_cliente}
        ).mappings().first()

        if registro is None:
            return None

        return dict(registro)

    def login_cliente_email(self, email: str):
        sql = text("""
            SELECT
                u.id_usuario,
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
                c.id_cliente,
                c.data_ultimo_servico
            FROM usuario u
            INNER JOIN cliente c
                ON c.id_cliente = u.id_usuario
            WHERE u.email = :email
        """)

        registro = db.session.execute(
            sql,
            {"email": email}
        ).mappings().first()

        if registro is None:
            return None

        return dict(registro)

    def consultar_clientes_services(self):
        sql = text("""
            SELECT
                u.id_usuario,
                u.nome_completo,
                u.telefone,
                c.data_ultimo_servico
            FROM usuario u
            INNER JOIN cliente c
                ON c.id_cliente = u.id_usuario
            ORDER BY u.nome_completo
        """)

        registros = db.session.execute(sql).mappings().all()

        return [dict(registro) for registro in registros]

    def atualizar(self, cliente: Cliente):
        sql_usuario = text("""
            UPDATE usuario
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
            WHERE id_usuario = :id_usuario
        """)

        sql_cliente = text("""
            UPDATE cliente
            SET
                data_ultimo_servico = :data_ultimo_servico
            WHERE id_cliente = :id_cliente
        """)

        parametros = {
            "id_usuario": cliente.id_cliente,
            "id_cliente": cliente.id_cliente,
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

        db.session.commit()

        return resultado_cliente.rowcount > 0

    def atualizar_data_ultimo_servico(
        self,
        id_cliente: int,
        data: datetime
    ):
        sql = text("""
            UPDATE cliente
            SET data_ultimo_servico = :data
            WHERE id_cliente = :id_cliente
        """)

        resultado = db.session.execute(sql, {
            "id_cliente": id_cliente,
            "data": data
        })

        db.session.commit()

        return resultado.rowcount > 0
