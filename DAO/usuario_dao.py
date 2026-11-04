
from sqlalchemy import text
from database import db
from models.usuarios import Usuario


class UsuarioDAO:

    @staticmethod
    def salvar(usuario: Usuario):
        sql = text("""
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

        db.session.execute(sql, {
            "id": usuario.id,
            "nome_completo": usuario.nome_completo,
            "telefone": usuario.telefone,
            "cpf": usuario.cpf,
            "email": usuario.email,
            "senha": usuario.senha,
            "foto_nome": usuario.foto_nome,
            "status_usuario": usuario.status_usuario,
            "data_cadastro": usuario.data_cadastro,
            "data_atualizacao": usuario.data_atualizacao,
            "fk_id_endereco": usuario.fk_id_endereco
        })

        db.session.flush()

        return usuario.id

    @staticmethod
    def buscar_por_id(id_usuario: int):
        sql = text("""
            SELECT
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
            FROM usuarios
            WHERE id = :id
        """)

        registro = db.session.execute(
            sql,
            {"id": id_usuario}
        ).mappings().first()

        if registro is None:
            return None

        return UsuarioDAO._mapear(registro)

    @staticmethod
    def buscar_por_email(email: str):
        sql = text("""
            SELECT
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
            FROM usuarios
            WHERE email = :email
        """)

        registro = db.session.execute(
            sql,
            {"email": email}
        ).mappings().first()

        if registro is None:
            return None

        return UsuarioDAO._mapear(registro)

    @staticmethod
    def buscar_por_cpf(cpf: str):
        sql = text("""
            SELECT
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
            FROM usuarios
            WHERE cpf = :cpf
        """)

        registro = db.session.execute(
            sql,
            {"cpf": cpf}
        ).mappings().first()

        if registro is None:
            return None

        return UsuarioDAO._mapear(registro)

    @staticmethod
    def listar_todos():
        sql = text("""
            SELECT
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
            FROM usuarios
            ORDER BY nome_completo
        """)

        registros = db.session.execute(sql).mappings().all()

        return [
            UsuarioDAO._mapear(registro)
            for registro in registros
        ]

    @staticmethod
    def listar_ativos():
        sql = text("""
            SELECT
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
            FROM usuarios
            WHERE status_usuario = :status
            ORDER BY nome_completo
        """)

        registros = db.session.execute(
            sql,
            {"status": True}
        ).mappings().all()

        return [
            UsuarioDAO._mapear(registro)
            for registro in registros
        ]

    @staticmethod
    def atualizar(usuario: Usuario):
        sql = text("""
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

        resultado = db.session.execute(sql, {
            "id": usuario.id,
            "nome_completo": usuario.nome_completo,
            "telefone": usuario.telefone,
            "cpf": usuario.cpf,
            "email": usuario.email,
            "senha": usuario.senha,
            "foto_nome": usuario.foto_nome,
            "status_usuario": usuario.status_usuario,
            "data_atualizacao": usuario.data_atualizacao,
            "fk_id_endereco": usuario.fk_id_endereco
        })

        db.session.flush()

        return resultado.rowcount > 0

    @staticmethod
    def alterar_status(id_usuario: int, status: bool):
        sql = text("""
            UPDATE usuarios
            SET status_usuario = :status
            WHERE id = :id
        """)

        resultado = db.session.execute(sql, {
            "id": id_usuario,
            "status": status
        })

        db.session.flush()

        return resultado.rowcount > 0

    @staticmethod
    def excluir(id_usuario: int):
        sql = text("""
            DELETE FROM usuarios
            WHERE id = :id
        """)

        resultado = db.session.execute(
            sql,
            {"id": id_usuario}
        )

        db.session.flush()

        return resultado.rowcount > 0

    @staticmethod
    def verificar_email_existente(
        email: str,
        id_ignorado: int = None
    ):
        sql = text("""
            SELECT 1
            FROM usuarios
            WHERE email = :email
              AND (:id_ignorado IS NULL OR id <> :id_ignorado)
            LIMIT 1
        """)

        resultado = db.session.execute(sql, {
            "email": email,
            "id_ignorado": id_ignorado
        }).first()

        return resultado is not None

    @staticmethod
    def verificar_cpf_existente(
        cpf: str,
        id_ignorado: int = None
    ):
        sql = text("""
            SELECT 1
            FROM usuarios
            WHERE cpf = :cpf
              AND (:id_ignorado IS NULL OR id <> :id_ignorado)
            LIMIT 1
        """)

        resultado = db.session.execute(sql, {
            "cpf": cpf,
            "id_ignorado": id_ignorado
        }).first()

        return resultado is not None

    @staticmethod
    def _mapear(registro):
        return Usuario(
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
            fk_id_endereco=registro["fk_id_endereco"]
        )
