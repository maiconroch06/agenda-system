
from sqlalchemy import text
from database import db
from models.gestor import Gestor


class GestorDAO:

    @staticmethod
    def salvar(gestor: Gestor):
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
            "id": gestor.id,
            "nome_completo": gestor.nome_completo,
            "telefone": gestor.telefone,
            "cpf": gestor.cpf,
            "email": gestor.email,
            "senha": gestor.senha,
            "foto_nome": gestor.foto_nome,
            "status_usuario": gestor.status_usuario,
            "data_cadastro": gestor.data_cadastro,
            "data_atualizacao": gestor.data_atualizacao,
            "fk_id_endereco": gestor.fk_id_endereco,
            "fk_cnpj_barbearia": gestor.fk_cnpj_barbearia
        }

        db.session.execute(sql_usuario, parametros)
        db.session.execute(sql_gestor, parametros)
        db.session.flush()

        return gestor.id

    @staticmethod
    def buscar_por_id(id_gestor: int):
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
            WHERE g.id = :id
        """)

        registro = db.session.execute(
            sql,
            {"id": id_gestor}
        ).mappings().first()

        if registro is None:
            return None

        return GestorDAO._mapear(registro)

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
                g.fk_cnpj_barbearia
            FROM usuarios u
            INNER JOIN gestor g ON g.id = u.id
            ORDER BY u.nome_completo
        """)

        registros = db.session.execute(sql).mappings().all()

        return [
            GestorDAO._mapear(registro)
            for registro in registros
        ]

    @staticmethod
    def listar_por_barbearia(cnpj: str):
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
            WHERE g.fk_cnpj_barbearia = :cnpj
            ORDER BY u.nome_completo
        """)

        registros = db.session.execute(
            sql,
            {"cnpj": cnpj}
        ).mappings().all()

        return [
            GestorDAO._mapear(registro)
            for registro in registros
        ]

    @staticmethod
    def atualizar(gestor: Gestor):
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

        db.session.flush()

        return resultado_gestor.rowcount > 0

    @staticmethod
    def excluir(id_gestor: int):
        sql_gestor = text("""
            DELETE FROM gestor
            WHERE id = :id
        """)

        resultado = db.session.execute(
            sql_gestor,
            {"id": id_gestor}
        )

        if resultado.rowcount == 0:
            return False

        sql_usuario = text("""
            DELETE FROM usuarios
            WHERE id = :id
        """)

        db.session.execute(
            sql_usuario,
            {"id": id_gestor}
        )

        db.session.flush()

        return True

    @staticmethod
    def _mapear(registro):
        return Gestor(
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
            fk_cnpj_barbearia=registro["fk_cnpj_barbearia"]
        )
