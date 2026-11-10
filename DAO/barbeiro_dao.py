
from sqlalchemy import text
from database import db
from models import Barbeiro


class BarbeiroDAO:

    def cadastrar(self, barbeiro: Barbeiro):
        sql = text("""
            INSERT INTO barbeiros (
                id_barbeiro,
                data_liberacao,
                descricao,
                status_barbeiro,
                fk_id_agenda
            ) VALUES (
                :id_barbeiro,
                :data_liberacao,
                :descricao,
                :status_barbeiro,
                :fk_id_agenda
            )
        """)

        db.session.execute(sql, {
            "id_barbeiro": barbeiro.id_barbeiro,
            "data_liberacao": barbeiro.data_liberacao,
            "descricao": barbeiro.descricao,
            "status_barbeiro": barbeiro.status_barbeiro,
            "fk_id_agenda": barbeiro.agenda.id_agenda
        })

        db.session.flush()

        return barbeiro.id_barbeiro

    def buscar_por_id(self, id_barbeiro: int):
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
                b.id_barbeiro,
                b.data_liberacao,
                b.descricao,
                b.status_barbeiro,
                b.fk_id_agenda
            FROM usuarios u
            INNER JOIN barbeiros b
                ON b.id_barbeiro = u.id_usuario
            WHERE b.id_barbeiro = :id_barbeiro
        """)

        registro = db.session.execute(
            sql,
            {"id_barbeiro": id_barbeiro}
        ).mappings().first()

        if registro is None:
            return None

        return self._mapear_barbeiro(registro)

    def consultar_todos(self):
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
                b.id_barbeiro,
                b.data_liberacao,
                b.descricao,
                b.status_barbeiro,
                b.fk_id_agenda
            FROM usuarios u
            INNER JOIN barbeiros b
                ON b.id_barbeiro = u.id_usuario
            ORDER BY u.nome_completo
        """)

        registros = db.session.execute(sql).mappings().all()

        return [
            self._mapear_barbeiro(registro)
            for registro in registros
        ]

    def atualizar_informacoes_barbeiro(self, barbeiro: Barbeiro):
        sql = text("""
            UPDATE barbeiros
            SET
                data_liberacao = :data_liberacao,
                descricao = :descricao,
                status_barbeiro = :status_barbeiro,
                fk_id_agenda = :fk_id_agenda
            WHERE id_barbeiro = :id_barbeiro
        """)

        resultado = db.session.execute(sql, {
            "id_barbeiro": barbeiro.id_barbeiro,
            "data_liberacao": barbeiro.data_liberacao,
            "descricao": barbeiro.descricao,
            "status_barbeiro": barbeiro.status_barbeiro,
            "fk_id_agenda": barbeiro.agenda.id_agenda
        })

        db.session.flush()

        return resultado.rowcount > 0

    def excluir_barbeiro(self, id_barbeiro: int):
        sql_barbeiro = text("""
            DELETE FROM barbeiros
            WHERE id_barbeiro = :id_barbeiro
        """)

        resultado = db.session.execute(
            sql_barbeiro,
            {"id_barbeiro": id_barbeiro}
        )

        if resultado.rowcount == 0:
            return False

        sql_usuario = text("""
            DELETE FROM usuarios
            WHERE id_usuario = :id_usuario
        """)

        db.session.execute(
            sql_usuario,
            {"id_usuario": id_barbeiro}
        )

        db.session.flush()

        return True

    @staticmethod
    def _mapear_barbeiro(registro):
        return Barbeiro(
            id_barbeiro=registro["id_barbeiro"],
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
