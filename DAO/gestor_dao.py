
from sqlalchemy import text
from database import db
from models import Gestor


class GestorDAO:
   
    def cadastrar(self, id:int, id_barbearia:int):
        sql_gestor = text("""
            INSERT INTO gestor (
                id,
                fk_cnpj_barbearia
            ) VALUES (
                :id,
                :fk_cnpj_barbearia
            )
        """)

        parametros = {
            "id": id,
            "fk_cnpj_barbearia": id_barbearia
        }

        resposta = db.session.execute(sql_gestor, parametros)
    

        return resposta.lastrowid

    def realizar_login_dao(self, email):
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
                g.fk_cnpj_barbearia
            FROM usuarios u
            INNER JOIN gestor g ON g.id = u.id
            WHERE u.email = :email
        """)

        registro = db.session.execute(
            sql,
            {"email": email}
        ).mappings().first()       

        
        return dict(registro) if registro else None

  
    def consultarGestores(self):
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
                g.fk_cnpj_barbearia
            FROM usuarios u
            INNER JOIN gestor g ON g.id = u.id
            ORDER BY u.nome_completo
        """)

        registros = db.session.execute(sql).mappings().all()

        return dict(registros) if registros else None

    
    def atualizar(self, gestor: Gestor):
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
            WHERE id = :id
        """)

        sql_gestor = text("""
            UPDATE gestor
            SET fk_cnpj_barbearia = :fk_cnpj_barbearia
            WHERE id = :id
        """)

        parametros = {
            "id": gestor.id,
            "nome_completo": gestor.nome_completo,
            "telefone": gestor.telefone,
            "cpf": gestor.cpf,
            "email": gestor.email,
            "senha": gestor.senha,
            "foto_nome": gestor.foto_nome,
            "status_usuario": gestor.status_usuario,
            "data_atualizacao": gestor.data_atualizacao,
            "fk_id_endereco": gestor.fk_id_endereco,
            "fk_cnpj_barbearia": gestor.fk_cnpj_barbearia
        }

        resultado_usuario = db.session.execute(
            sql_usuario, parametros
        )

        if resultado_usuario.rowcount == 0:
            return False

        resultado_gestor = db.session.execute(
            sql_gestor, parametros
        )

        db.session.commit()

        return resultado_gestor.rowcount > 0

