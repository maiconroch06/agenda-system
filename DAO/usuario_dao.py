
from sqlalchemy import text
from database import db
from models.usuarios import Usuario


class UsuarioDAO:

    def cadastrar(self, usuario: Usuario):
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

        resposta_id_usuario = db.session.execute(sql, {
            "id": None,
            "nome_completo": usuario.nome_completo,
            "telefone": usuario.telefone,
            "cpf": usuario.cpf,
            "email": usuario.email,
            "senha": usuario.senha,
            "foto_nome": usuario.foto_nome,
            "status_usuario": usuario.status_usuario,
            "data_cadastro": usuario.data_cadastro,
            "data_atualizacao": usuario.data_atualizacao,
            "fk_id_endereco": usuario.endereco.id if usuario.endereco is not None else None
        })

        db.session.flush()
        
        #retorna o ultimo id inserido no banco;
        return resposta_id_usuario.lastrowid 


    def buscar_por_id(self, id_usuario: int):
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


    def buscar_por_email(self, email: str):
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


    def buscar_por_cpf(self, cpf: str):
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


    def consultar_todos_usuarios(self, ):
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


    def contultar_usuarios_ativos(self, ):
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


    def atualizar_usuarios_sem_senha(self, usuario: Usuario):
        sql = text("""
            UPDATE usuarios
            SET
                nome_completo = :nome_completo,
                telefone = :telefone,
                cpf = :cpf,
                email = :email,
                foto_nome = :foto_nome,
                data_atualizacao = :data_atualizacao
            WHERE id = :id
        """)

        resultado = db.session.execute(sql, {
            "id": usuario.id,
            "nome_completo": usuario.nome_completo,
            "telefone": usuario.telefone,
            "cpf": usuario.cpf,
            "email": usuario.email,
            "foto_nome": usuario.foto_nome,
            "data_atualizacao": usuario.data_atualizacao,
        })

        db.session.flush()

        return resultado.rowcount > 0
    
    def atualizar_usuarios_com_senha(self, usuario: Usuario):
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


    def alterar_status(self, id_usuario: int, status: bool):
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


    def excluir(self, id_usuario: int):
        sql = text("""
            DELETE FROM usuarios
            WHERE id = :id
        """)

        resultado = db.session.execute(
            sql,
            {"id": id_usuario}
        )
        
            
        db.session.commit()

        return resultado.rowcount > 0


    def verificar_email_existente(self, 
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


    def verificar_cpf_existente(self, 
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


    def _mapear(self, registro):
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
