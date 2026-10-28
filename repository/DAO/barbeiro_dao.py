
from sqlalchemy import text
from database import db
from models.barbeiros import Barbeiro


class BarbeiroDAO:

    @staticmethod
    def salvar(barbeiro: Barbeiro):
        # Insere os dados gerais do usuário
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

        db.session.execute(sql_usuario, {
            "id": barbeiro.id,
            "nome_completo": barbeiro.nome_completo,
            "telefone": barbeiro.telefone,
            "cpf": barbeiro.cpf,
            "email": barbeiro.email,
            "senha": barbeiro.senha,
            "foto_nome": barbeiro.foto_nome,
            "status_usuario": barbeiro.status_usuario,
            "data_cadastro": barbeiro.data_cadastro,
            "data_atualizacao": barbeiro.data_atualizacao,
            "fk_id_endereco": barbeiro.fk_id_endereco
        })

        # Insere os dados específicos do barbeiro
        sql_barbeiro = text("""
            INSERT INTO barbeiros (
                id,
                data_liberacao,
                descricao,
                status_barbeiro,
                fk_id_agenda
            ) VALUES (
                :id,
                :data_liberacao,
                :descricao,
                :status_barbeiro,
                :fk_id_agenda
            )
        """)

        db.session.execute(sql_barbeiro, {
            "id": barbeiro.id,
            "data_liberacao": barbeiro.data_liberacao,
            "descricao": barbeiro.descricao,
            "status_barbeiro": barbeiro.status_barbeiro,
            "fk_id_agenda": barbeiro.fk_id_agenda
        })

        db.session.flush()
        return barbeiro.id

    @staticmethod
    def buscar_por_id(id_barbeiro: int):
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
                b.data_liberacao,
                b.descricao,
                b.status_barbeiro,
                b.fk_id_agenda
            FROM usuarios u
            INNER JOIN barbeiros b ON b.id = u.id
            WHERE b.id = :id
        """)

        registro = db.session.execute(
            sql,
            {"id": id_barbeiro}
        ).mappings().first()

        if registro is None:
            return None

        return BarbeiroDAO._mapear_barbeiro(registro)

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
                b.data_liberacao,
                b.descricao,
                b.status_barbeiro,
                b.fk_id_agenda
            FROM usuarios u
            INNER JOIN barbeiros b ON b.id = u.id
            ORDER BY u.nome_completo
        """)

        registros = db.session.execute(sql).mappings().all()

        return [
            BarbeiroDAO._mapear_barbeiro(registro)
            for registro in registros
        ]

    @staticmethod
    def atualizar(barbeiro: Barbeiro):
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

        db.session.execute(sql_usuario, {
            "id": barbeiro.id,
            "nome_completo": barbeiro.nome_completo,
            "telefone": barbeiro.telefone,
            "cpf": barbeiro.cpf,
            "email": barbeiro.email,
            "senha": barbeiro.senha,
            "foto_nome": barbeiro.foto_nome,
            "status_usuario": barbeiro.status_usuario,
            "data_atualizacao": barbeiro.data_atualizacao,
            "fk_id_endereco": barbeiro.fk_id_endereco
        })

        sql_barbeiro = text("""
            UPDATE barbeiros
            SET
                data_liberacao = :data_liberacao,
                descricao = :descricao,
                status_barbeiro = :status_barbeiro,
                fk_id_agenda = :fk_id_agenda
            WHERE id = :id
        """)

        resultado = db.session.execute(sql_barbeiro, {
            "id": barbeiro.id,
            "data_liberacao": barbeiro.data_liberacao,
            "descricao": barbeiro.descricao,
            "status_barbeiro": barbeiro.status_barbeiro,
            "fk_id_agenda": barbeiro.fk_id_agenda
        })

        db.session.flush()
        return resultado.rowcount > 0

    @staticmethod
    def excluir(id_barbeiro: int):
        sql = text("""
            DELETE FROM barbeiros
            WHERE id = :id
        """)

        resultado = db.session.execute(
            sql,
            {"id": id_barbeiro}
        )

        if resultado.rowcount == 0:
            return False

        # Exclui o usuário correspondente somente se permitido
        sql_usuario = text("""
            DELETE FROM usuarios
            WHERE id = :id
        """)

        db.session.execute(
            sql_usuario,
            {"id": id_barbeiro}
        )

        db.session.flush()
        return True

    @staticmethod
    def _mapear_barbeiro(registro):
        return Barbeiro(
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
            data_liberacao=registro["data_liberacao"],
            descricao=registro["descricao"],
            status_barbeiro=bool(registro["status_barbeiro"]),
            fk_id_agenda=registro["fk_id_agenda"]
        )
