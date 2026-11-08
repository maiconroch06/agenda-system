
from sqlalchemy import text
from database import db
from models import Barbeiro


class BarbeiroDAO:
    
    def cadastrar(self, barbeiro: Barbeiro):
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

        reposta = db.session.execute(sql_barbeiro, {
            "id": barbeiro.id,
            "data_liberacao": barbeiro.data_liberacao,
            "descricao": barbeiro.descricao,
            "status_barbeiro": barbeiro.status_barbeiro,
            "fk_id_agenda": barbeiro.agenda.id
        })

        db.session.flush()
            
        return reposta.rowcount > 0

    
    def buscar_por_id(self, id_barbeiro: int):
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

    
    def consultar_todos(self):
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
                b.fk_id_agenda,
                e.*
            FROM usuarios u
                INNER JOIN barbeiros b 
                    ON b.id = u.id
                INNER JOIN enderecos e
                    on e.id = u.fk_id_endereco 
            ORDER BY u.nome_completo
        """)

        registros = db.session.execute(sql).mappings().all()

        return registros

   
    def atualizar_status_barbeiro(self,barbeiro:Barbeiro):
            sql_usuario = text("""
                UPDATE barbeiros
                SET
                descricao=:descricao,
                status_barbeiro=:status_barbeiro,
                WHERE id = :id
            """)
    
            resultado = db.session.execute(sql_usuario, {
                "id": barbeiro.id,
                "descricao": barbeiro.descricao,
                "status_barbeiro": barbeiro.status_barbeiro,
            })
    
            db.session.commit()
            return resultado.rowcount > 0

    def excluir_barbeiro(self, id_barbeiro: int):
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

    def _mapear_barbeiros(self, registro):
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
