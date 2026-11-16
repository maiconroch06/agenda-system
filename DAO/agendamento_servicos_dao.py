from sqlalchemy import text
from database import db
from flask import flash
from models import Barbeiro, Agendamento, Servico, AgendamentoServicos
from datetime import datetime

class AgendamentoServicosDAO:

    @staticmethod
    def salvar(id_agendamento, id_servicos):
        sql = text("""
        INSERT INTO agendamento_servicos(
            agendamento_id,
            servico_id
        ) VALUES (
            :id_agendamento,
            :id_servico
        )          
        """)

        try:
            for id_servico in id_servicos:
                parametros = {
                    "id_agendamento": id_agendamento,
                    "id_servico": id_servico
                }
                db.session.execute(sql, parametros)

            db.session.commit()
        except Exception as erros:
            flash(f"{erros}")

        return True

    @staticmethod
    def consultar_dados_por_cliente(id_cliente):

        sql = text("""
            SELECT 
                a.id_agendamento,
                a.data_agendamento,
                a.hora_inicio,
                a.hora_fim,
                a.data_atualizacao,
                a.status_agendamento,
                a.motivo_cancelamento,

                b.id_barbeiro,
                u.nome_completo,
                u.telefone,
                u.cpf,
                u.email,
                b.bio,
                b.especialidade,

                s.id_servico,
                s.descricao_servico,
                s.valor,
                s.duracao,
                s.foto_nome_servico

            FROM agendamento a

            INNER JOIN barbeiro b
                ON a.fk_id_barbeiro = b.id_barbeiro

            INNER JOIN usuario u
                ON b.id_barbeiro = u.id_usuario

            INNER JOIN agendamento_servicos ass
                ON a.id_agendamento = ass.agendamento_id

            INNER JOIN servico s
                ON ass.servico_id = s.id_servico

            WHERE a.fk_id_cliente = :fk_id_cliente

            ORDER BY a.data_agendamento ASC, a.hora_inicio ASC;
        """)

        try:
            resultados = db.session.execute(
                sql,
                {"fk_id_cliente": id_cliente}
            ).mappings().all()

            agendamentos = {}

            for registro in resultados:

                id_agendamento = registro["id_agendamento"]

                # Cria os objetos utilizando o método de mapeamento
                item = AgendamentoServicosDAO._mapear_agendamento_todos_dados(
                    registro
                )

                if id_agendamento not in agendamentos:

                    # Primeiro registro desse agendamento
                    agendamentos[id_agendamento] = item

                else:

                    # Adiciona somente os serviços ao agrupamento existente
                    agendamentos[id_agendamento].servicos.extend(
                        item.servicos
                    )

            return list(agendamentos.values())

        except Exception:
            db.session.rollback()
            raise

    @staticmethod
    def _mapear_agendamento_todos_dados(registro):
    
            barbeiro = Barbeiro(
                id_usuario=registro["id_barbeiro"],
                nome_completo=registro["nome_completo"],
                email=registro["email"],
                telefone=registro["telefone"],
                bio=registro["bio"],
                cpf=registro["cpf"],
                data_atualizacao=registro["data_atualizacao"]
            )
    
            servico = Servico(
               id_servico=registro["id_servico"],
               descricao_servico=registro["descricao_servico"],
               valor=registro["valor"],
               duracao=registro["duracao"]
            )
    
            agendamento = Agendamento(
                id_agendamento=registro["id_agendamento"],
                data_agendamento=registro["data_agendamento"],
                hora_inicio=(datetime.min + registro["hora_inicio"]).time(),
                hora_fim=(datetime.min + registro["hora_fim"]).time(),
                motivo_cancelamento=registro["motivo_cancelamento"],
                status_agendamento=registro["status_agendamento"],
                data_atualizacao=registro["data_atualizacao"],
                barbeiro = barbeiro,
                cliente = None
            )

            agendamentoServicos = AgendamentoServicos(
                agendamento=agendamento,
                servicos=[servico]
            )
    
            return agendamentoServicos

