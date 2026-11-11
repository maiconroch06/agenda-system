
from sqlalchemy import text
from database import db
from models import Barbeiro, Endereco


class BarbeiroDAO:

    def cadastrar(self, barbeiro: Barbeiro):
        sql = text("""
            INSERT INTO barbeiro (
                id_barbeiro,
                data_liberacao,
                bio,
                especialidade,
                status_barbeiro,
                data_inicio_carreira
            ) VALUES (
                :id_barbeiro,
                :data_liberacao,
                :bio,
                :especialidade,
                :status_barbeiro,
                :data_inicio_carreira
            )
        """)

        db.session.execute(sql, {
            "id_barbeiro": barbeiro.id_usuario,
            "data_liberacao": barbeiro.data_liberacao,
            "bio": barbeiro.descricao,
            "especialidade": barbeiro.especialidade,
            "status_barbeiro": barbeiro.status_barbeiro,
            "data_inicio_carreira": barbeiro.data_inicio_carreira
        })

        db.session.commit()

        return barbeiro.id_usuario

    def buscar_por_id(self, id_barbeiro: int):
        sql = text("""
            SELECT
                u.id_usuario,
                u.nome_completo,
                u.telefone,
                u.cpf,
                u.email,
                u.senha,
                u.foto_nome_usuario,
                u.status_usuario,
                u.data_cadastro,
                u.data_atualizacao,

                b.id_barbeiro,
                b.data_liberacao,
                b.bio,
                b.especialidade,
                b.status_barbeiro,
                b.data_inicio_carreira,

                e.id_endereco,
                e.cep,
                e.cidade,
                e.uf,
                e.logradouro,
                e.numero,
                e.bairro,
                e.sequencia,
                e.complemento

            FROM usuario u

            INNER JOIN barbeiro b
                ON b.id_barbeiro = u.id_usuario

            LEFT JOIN endereco e
                ON e.id_endereco = u.fk_id_endereco

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
                u.foto_nome_usuario,
                u.status_usuario,
                u.data_cadastro,
                u.data_atualizacao,

                b.id_barbeiro,
                b.data_liberacao,
                b.bio,
                b.especialidade,
                b.status_barbeiro,
                b.data_inicio_carreira,

                e.id_endereco,
                e.cep,
                e.cidade,
                e.uf,
                e.logradouro,
                e.numero,
                e.bairro,
                e.sequencia,
                e.complemento

            FROM usuario u

            INNER JOIN barbeiro b
                ON b.id_barbeiro = u.id_usuario

            LEFT JOIN endereco e
                ON e.id_endereco = u.fk_id_endereco

            ORDER BY u.nome_completo
        """)

        registros = db.session.execute(sql).mappings().all()

        return [
            self._mapear_barbeiro(registro)
            for registro in registros
        ]

    def atualizar_informacoes_barbeiro(self, barbeiro: Barbeiro):
        sql = text("""
            UPDATE barbeiro
            SET
                data_liberacao = :data_liberacao,
                bio = :bio,
                especialidade = :especialidade,
                status_barbeiro = :status_barbeiro,
                data_inicio_carreira = :data_inicio_carreira

            WHERE id_barbeiro = :id_barbeiro
        """)

        resultado = db.session.execute(sql, {
            "id_barbeiro": barbeiro.id_usuario,
            "data_liberacao": barbeiro.data_liberacao,
            "bio": barbeiro.descricao,
            "especialidade": barbeiro.especialidade,
            "status_barbeiro": barbeiro.status_barbeiro,
            "data_inicio_carreira": barbeiro.data_inicio_carreira
        })

        db.session.commit()

        return resultado.rowcount > 0

    @staticmethod
    def _mapear_barbeiro(registro):

        endereco = None

        if registro["id_endereco"] is not None:
            endereco = Endereco(
                id_endereco=registro["id_endereco"],
                cep=registro["cep"],
                cidade=registro["cidade"],
                uf=registro["uf"],
                logradouro=registro["logradouro"],
                numero=registro["numero"],
                bairro=registro["bairro"],
                sequencia=registro["sequencia"],
                complemento=registro["complemento"]
            )

        return Barbeiro(
            id_usuario=registro["id_usuario"],
            nome_completo=registro["nome_completo"],
            telefone=registro["telefone"],
            cpf=registro["cpf"],
            email=registro["email"],
            senha=registro["senha"],
            foto_nome_usuario=registro["foto_nome_usuario"],
            status_usuario=bool(registro["status_usuario"]),
            data_cadastro=registro["data_cadastro"],
            data_atualizacao=registro["data_atualizacao"],

            data_liberacao=registro["data_liberacao"],
            descricao=registro["bio"],
            especialidade=registro["especialidade"],
            status_barbeiro=bool(registro["status_barbeiro"]),
            data_inicio_carreira=registro["data_inicio_carreira"],

            endereco=endereco
        )