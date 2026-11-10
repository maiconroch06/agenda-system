
from sqlalchemy import text
from database import db
from models import Cliente
from datetime import datetime
from flask import flash





class ClienteDAO:

    
    def cadastrar(self, id:int, dataUltimoServico:datetime | None):
        
        sql_cliente = text("""
            INSERT INTO clientes (
                id_cliente,
                data_ultimo_servico
            ) VALUES (
                :id_cliente,
                :data_ultimo_servico
            )
        """)

        parametros_cliente = {
            "id_cliente": id_cliente,
            "data_ultimo_servico": dataUltimoServico
        }

        resposta_insert_cliente = db.session.execute(sql_cliente, parametros_cliente)
        db.session.flush()

        return resposta_insert_cliente.rowcount > 0

    
    def consultarClienteId(self, id_cliente: int):
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

        return dict(registro)

    def login_cliente_email(self, email):
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
                c.data_ultimo_servico
            FROM usuarios u
            INNER JOIN clientes c ON c.id_cliente = u.id_usuario
            WHERE u.email = :email
        """)

        registro = db.session.execute(
            sql,
            {"email": email}
        ).mappings().first()
         
        if registro is None:
            flash(f"Email não cadastrado. Verifique se digitou o email correto!")
            raise Exception()
        
        return dict(registro)
    
    def consultar_clientes_services(self):
        sql = text("""
            SELECT
                u.id_usuario,
                u.nome_completo,
                u.telefone,
				c.data_ultimo_servico
            FROM usuario u
            INNER JOIN cliente c ON c.id_cliente = u.id_usuario
            ORDER BY u.nome_completo
        """)

        registros = db.session.execute(sql).mappings().all()

        return registros

   
    def atualizar(self, cliente: Cliente):
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

    
    def excluir(self, id_cliente: int):
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

   
    def atualizar_data_ultimo_servico(
        self,
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


