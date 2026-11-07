
from sqlalchemy import text
from database import db
from models import Servico


class ServicoDAO:

    
    def cadastrar_servico(self, servico: Servico):
        sql = text("""
            INSERT INTO servicos (
                descricao,
                valor,
                duracao,
                foto_nome,
                status_servico,
                data_cadastro,
                data_atualizacao
            ) VALUES (
                :descricao,
                :valor,
                :duracao,
                :foto_nome,
                :status_servico,
                :data_cadastro,
                :data_atualizacao
            )
        """)

        resposta = db.session.execute(sql, {
            "id": servico.id,
            "descricao": servico.descricao,
            "valor": servico.valor,
            "duracao": servico.duracao,
            "foto_nome": servico.foto_nome,
            "status_servico": servico.status_servico,
            "data_cadastro": servico.data_cadastro,
            "data_atualizacao": servico.data_atualizacao
        })

        db.session.commit()

        return resposta.lastrowid > 0

   
    def consultar_servico_id(self,id_servico: int):
        sql = text("""
            SELECT
                id,
                descricao,
                valor,
                duracao,
                foto_nome,
                status_servico,
                data_cadastro,
                data_atualizacao
            FROM servicos
            WHERE id = :id
        """)

        registro = db.session.execute(
            sql,
            {"id": id_servico}
        ).mappings().first()

        

        return dict(registro) if registro else None

    
    def consultar_todos_os_servicos(self):
        sql = text("""
            SELECT
                id,
                descricao,
                valor,
                duracao,
                foto_nome,
                status_servico,
                data_cadastro,
                data_atualizacao
            FROM servicos
            ORDER BY descricao
        """)

        registros = db.session.execute(sql).mappings().all()

        return registros

    
    def consultar_servicos_status(self, status_servicos:bool):
        sql = text("""
            SELECT
                id,
                descricao,
                valor,
                duracao,
                foto_nome,
                status_servico,
                data_cadastro,
                data_atualizacao
            FROM servicos
            WHERE status_servico = :status
            ORDER BY descricao
        """)

        registros = db.session.execute(
            sql,
            {"status": status_servicos}
        ).mappings().all()

        return dict(registros) if registros else None

   
    def atualizar(self, servico: Servico):
        sql = text("""
            UPDATE servicos
            SET
                descricao = :descricao,
                valor = :valor,
                duracao = :duracao,
                foto_nome = :foto_nome,
                status_servico = :status_servico,
                data_atualizacao = :data_atualizacao
            WHERE id = :id
        """)

        resultado = db.session.execute(sql, {
            "id": servico.id,
            "descricao": servico.descricao,
            "valor": servico.valor,
            "duracao": servico.duracao,
            "foto_nome": servico.foto_nome,
            "status_servico": servico.status_servico,
            "data_atualizacao": servico.data_atualizacao
        })

        db.session.commit()

        return resultado.rowcount > 0

  
    def ativar(self, id_servico: int, data_atualizacao):
        sql = text("""
            UPDATE servicos
            SET
                status_servico = :status,
                data_atualizacao = :data_atualizacao
            WHERE id = :id
        """)

        resultado = db.session.execute(sql, {
            "id": id_servico,
            "status": True,
            "data_atualizacao": data_atualizacao
        })

        db.session.commit()

        return resultado.rowcount > 0

    
    def desativar(self, id_servico: int, data_atualizacao):
        sql = text("""
            UPDATE servicos
            SET
                status_servico = :status,
                data_atualizacao = :data_atualizacao
            WHERE id = :id
        """)

        resultado = db.session.execute(sql, {
            "id": id_servico,
            "status": False,
            "data_atualizacao": data_atualizacao
        })

        db.session.commit()

        return resultado.rowcount > 0

  
    def excluir(self, id_servico: int):
        sql = text("""
            DELETE FROM servicos
            WHERE id = :id
        """)

        resultado = db.session.execute(
            sql,
            {"id": id_servico}
        )

        db.session.commit()

        return resultado.rowcount > 0
