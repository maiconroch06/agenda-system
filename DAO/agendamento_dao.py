
from sqlalchemy import text
from database import db
from models import Agendamento, Barbeiro, Servico
from datetime import date, datetime
from enums import EnumStatusAgendamento
from utilitarios import FormatarHoras, FormatarTelefone, FormatarData

class AgendamentoDAO:

    @staticmethod
    def salvar(agendamento: Agendamento):

        sql = text("""
            INSERT INTO agendamento (
                data_agendamento,
                hora_inicio,
                hora_fim,
                status_agendamento,
                data_atualizacao,
                valor_total_servicos,
                fk_id_barbeiro,
                fk_id_cliente
            ) VALUES (
                :data_agendamento,
                :hora_inicio,
                :hora_fim,
                :status_agendamento,
                :data_atualizacao,
                :valor_total_servicos,
                :fk_id_barbeiro,
                :fk_id_cliente
            )
        """)

        parametros = {
            "data_agendamento": agendamento.data_agendamento,
            "hora_inicio": agendamento.hora_inicio,
            "hora_fim": agendamento.hora_fim,
            "status_agendamento": agendamento.status_agendamento,
            "data_atualizacao": agendamento.data_atualizacao,
            "valor_total_servicos": agendamento.valor_total_servicos,
            "fk_id_barbeiro": agendamento.barbeiro.id_usuario,
            "fk_id_cliente": agendamento.cliente.id_usuario
        }


        resultado = db.session.execute(sql, parametros)

        db.session.commit()

        return resultado.lastrowid 

    # Gerenciar conflito
    @staticmethod
    def verificar_conflito(
        id_barbeiro: int,
        data_agendamento,
        hora_inicio,
        hora_fim
    ):
        sql = text("""
            SELECT id_agendamento
            FROM agendamento
            WHERE fk_id_barbeiro = :id_barbeiro
            AND data_agendamento = :data_agendamento
            AND hora_inicio < :hora_fim
            AND hora_fim > :hora_inicio
            LIMIT 1
        """)

        resultado = db.session.execute(sql, {
            "id_barbeiro": id_barbeiro,
            "data_agendamento": data_agendamento,
            "hora_inicio": hora_inicio,
            "hora_fim": hora_fim
        }).first()

        return resultado is not None

    @staticmethod
    def buscarPorIdDao(id_agendamento: int):
        sql = text("""
            SELECT
                id_agendamento,
                data_agendamento,
                hora_inicio,
                hora_fim,
                status_agendamento,
                data_atualizacao,
                valor_total_servicos,
                fk_id_barbeiro,
                fk_id_cliente
            FROM agendamento
            WHERE id_agendamento = :id_agendamento
        """)

        resultado = db.session.execute(
            sql,
            {"id_agendamento": id_agendamento}
        ).mappings().first()

        if resultado is None:
            return None

        return AgendamentoDAO._mapear_agendamento(resultado)

    @staticmethod
    def consultarTodosOsAgendamentoDoCliente(id_cliente):
        sql = text("""
            SELECT
                -- Dados do agendamento
                a.id_agendamento,
                a.data_agendamento,
                a.hora_inicio,
                a.hora_fim,
                a.status_agendamento,
                a.data_atualizacao,
                a.fk_id_barbeiro,
                a.fk_id_cliente,
                a.motivo_cancelamento,
                a.valor_total_servicos,

                -- Dados do barbeiro
                b.id_barbeiro,
                u.nome_completo,
                u.email,
                u.telefone,
                u.cpf,
                u.data_ultimo_acesso,
                b.bio
            FROM agendamento a

            INNER JOIN barbeiro b
                ON a.fk_id_barbeiro = b.id_barbeiro

            INNER JOIN usuario u
                ON b.id_barbeiro = u.id_usuario

            WHERE a.fk_id_cliente = :fk_id_cliente

            ORDER BY a.data_agendamento ASC, a.hora_inicio ASC
        """)

        try:
            resultados = db.session.execute(
                sql,
                {
                    "fk_id_cliente": id_cliente
                }
            ).mappings().all()

            return [
                AgendamentoDAO._mapear_agendamento_todos_dados(registro)
                for registro in resultados
            ]
        except Exception as erros:
            print(f"{erros}")
            
    @staticmethod
    def consultarTodosOsAgendamentoDataAtual(data_hoje):
            sql = text("""
                
                SELECT
                    -- Dados do agendamento
                    a.id_agendamento,
                    a.data_agendamento,
                    TIME_FORMAT(a.hora_inicio, '%H:%i') hora_inicio,
                    TIME_FORMAT(a.hora_fim, '%H:%i') hora_fim,
                    a.status_agendamento,
                    a.data_atualizacao,
                    a.fk_id_barbeiro,
                    a.fk_id_cliente,
                    a.motivo_cancelamento,
                    a.valor_total_servicos,
                    
                    # Junta os nomes dos serviços em uma única linha (Ex: "Corte, Barba")
                    GROUP_CONCAT(s.descricao_servico SEPARATOR ', ') AS nome_servico,
                                           
                    -- Dados do barbeiro
                    b.id_barbeiro,
                    ub.nome_completo,
                    ub.foto_usuario,
                    ub.email,
                    ub.telefone,
                    ub.cpf,
                    ub.data_ultimo_acesso,
                    b.bio,

                    -- Dados do cliente
                    c.id_cliente,
                    uc.nome_completo AS nome_cliente,
                    uc.telefone AS telefone_cliente

                FROM agendamento a

                INNER JOIN barbeiro b
                    ON a.fk_id_barbeiro = b.id_barbeiro

                INNER JOIN cliente c
                    ON a.fk_id_cliente = c.id_cliente

                INNER JOIN usuario uc
                    ON c.id_cliente = uc.id_usuario

                INNER JOIN usuario ub
                    ON b.id_barbeiro = ub.id_usuario
                    
                LEFT JOIN agendamento_servicos ags
                    ON a.id_agendamento = ags.agendamento_id
                    
                LEFT JOIN servico s
                    ON ags.servico_id = s.id_servico

                WHERE a.data_agendamento = :data_hoje

                -- 5. Agrupa pelo ID do agendamento para não duplicar a linha
                GROUP BY a.id_agendamento
                
                ORDER BY a.data_agendamento ASC, a.hora_inicio ASC
                
                
                            """)
    
            
            resultados = db.session.execute(
                    sql,
                    {
                        "data_hoje": data_hoje
                    }
                ).mappings().all()
            
            return  [dict(registro) for registro in resultados]
         
    @staticmethod
    def consultarTotalAgendamentosCancelados(data_hoje):
        sql = text("""
            select count(id_agendamento) FROM databasetmsbarbearia.agendamento WHERE status_agendamento = 0 
            """)
        
        resultados = db.session.execute(
                sql,
                {
                    "data_hoje": data_hoje
                }
            )
        
        return resultados.scalar()
    
    @staticmethod
    def consultarMediaMensalAgendamentoDao(data_inicio, data_final):
            sql = text("""
                    select AVG(valor_total_servicos) 
                    FROM databasetmsbarbearia.agendamento where data_agendamento 
                    BETWEEN :data_inicio AND :data_final 
                    AND status_agendamento=3 
                """)
            
            resultados = db.session.execute(
                    sql,
                    {
                        "data_inicio": data_inicio,
                        "data_final": data_final
                    }
                )
            
            
            return resultados.scalar()
    
    @staticmethod
    def consultar_agendamento_filtros(barbeiro_id,status,servico_id,data_inicio,data_fim):
        sql = text("""
                    
                    SELECT
                        -- Dados do agendamento
                        a.id_agendamento,
                        a.data_agendamento,
                        TIME_FORMAT(a.hora_inicio, '%H:%i') hora_inicio,
                        TIME_FORMAT(a.hora_fim, '%H:%i') hora_fim,
                        a.status_agendamento,
                        a.data_atualizacao,
                        a.fk_id_barbeiro,
                        a.fk_id_cliente,
                        a.motivo_cancelamento,
                        a.valor_total_servicos,
                        
                        # Junta os nomes dos serviços em uma única linha (Ex: "Corte, Barba")
                        GROUP_CONCAT(s.descricao_servico SEPARATOR ', ') AS nome_servico,
                                               
                        # Dados do barbeiro
                        b.id_barbeiro,
                        ub.nome_completo,
                        ub.foto_usuario,
                        ub.email,
                        ub.telefone,
                        ub.cpf,
                        ub.data_ultimo_acesso,
                        b.bio,
    
                        # Dados do cliente
                        c.id_cliente,
                        uc.nome_completo AS nome_cliente,
                        uc.telefone AS telefone_cliente
    
                    FROM agendamento a
    
                    INNER JOIN barbeiro b
                        ON a.fk_id_barbeiro = b.id_barbeiro
    
                    INNER JOIN cliente c
                        ON a.fk_id_cliente = c.id_cliente
    
                    INNER JOIN usuario uc
                        ON c.id_cliente = uc.id_usuario
    
                    INNER JOIN usuario ub
                        ON b.id_barbeiro = ub.id_usuario
                        
                    LEFT JOIN agendamento_servicos ags
                        ON a.id_agendamento = ags.agendamento_id
                        
                    LEFT JOIN servico s
                        ON ags.servico_id = s.id_servico
    
                    WHERE
                       
                        a.data_agendamento BETWEEN :data_inicio AND :data_fim

                       
                        AND (
                            :id_barbeiro = -1
                            OR a.fk_id_barbeiro = :id_barbeiro
                        )

                       
                        AND (
                            :id_servico = -1
                            OR s.id_servico = :id_servico
                        )

    
                        AND (
                            :status_agendamento = -1
                            OR a.status_agendamento = :status_agendamento
                        )

                    # 5. Agrupa pelo ID do agendamento para não duplicar a linha
                    GROUP BY a.id_agendamento
                    
                    ORDER BY a.data_agendamento ASC, a.hora_inicio ASC
                    
                    
                                """)
        
        resultados = db.session.execute(sql, {
                        'data_inicio': data_inicio,
                        'data_fim': data_fim,
                        'id_barbeiro': barbeiro_id,
                        'id_servico': servico_id,
                        'status_agendamento': status
        }).mappings().all()
                
        return  [dict(registro) for registro in resultados]
    
    @staticmethod
    def listarPorClienteDao(id_cliente: int):
        sql = text("""
            SELECT
                id_agendamento,
                data_agendamento,
                hora_inicio,
                hora_fim,
                status_agendamento,
                data_atualizacao,
                fk_id_barbeiro,
                fk_id_cliente
            FROM agendamento
            WHERE fk_id_cliente = :id_cliente
            ORDER BY data_agendamento, hora_inicio
        """)

        resultados = db.session.execute(
            sql,
            {"id_cliente": id_cliente}
        ).mappings().all()

        return [
            AgendamentoDAO._mapear_agendamento(registro)
            for registro in resultados
        ]

    @staticmethod
    def listarPorBarbeiro(id_barbeiro:int):
        sql = text("""
            SELECT
                a.id_agendamento,
                a.fk_id_barbeiro,
                a.fk_id_cliente,
                a.status_agendamento,
                a.motivo_cancelamento,
                a.valor_total_servicos AS valor,
                
                # Junta os nomes dos serviços em uma única linha (Ex: "Corte, Barba")
                GROUP_CONCAT(s.descricao_servico SEPARATOR ', ') AS nome_servico,
                
                a.data_agendamento,
                a.hora_inicio,
                a.hora_fim,
                
                ub.nome_completo AS nome_barbeiro,
                uc.nome_completo AS nome_cliente,
                uc.telefone AS telefone_cliente
                
            FROM agendamento a

            JOIN barbeiro b
                ON a.fk_id_barbeiro = b.id_barbeiro
            JOIN usuario ub
                ON b.id_barbeiro = ub.id_usuario

            JOIN cliente c
                ON a.fk_id_cliente = c.id_cliente
            JOIN usuario uc
                ON c.id_cliente = uc.id_usuario

            LEFT JOIN agendamento_servicos ags
                ON a.id_agendamento = ags.agendamento_id

            LEFT JOIN servico s
                ON ags.servico_id = s.id_servico

            WHERE a.fk_id_barbeiro = :id_barbeiro
                AND b.status_barbeiro = 1

            -- 5. Agrupa pelo ID do agendamento para não duplicar a linha
            GROUP BY a.id_agendamento

        """)
        
        registros = db.session.execute(
            sql,
            {"id_barbeiro": id_barbeiro}
        ).mappings().all()
        
        print("TAMANHO DOS BARNEIOROS", len(registros))
        
        return [
            {
                "id": str(registro["id_agendamento"]),
                "barbeiro": registro["nome_barbeiro"],
                "data": FormatarData._formatar_data(registro["data_agendamento"]),
                "hora_inicio": FormatarHoras._formatar_hora(registro["hora_inicio"]),
                "hora_fim": FormatarHoras._formatar_hora(registro["hora_fim"]),
                "motivo_cancelamento": registro["motivo_cancelamento"],
                "cliente": registro["nome_cliente"],
                "telefone": FormatarTelefone._formatar_telefone(registro["telefone_cliente"]),
                "servico": registro["nome_servico"],
                "valor": float(registro["valor"] or 0),
                "status": registro["status_agendamento"],
            }
            for registro in registros
        ]

    @staticmethod
    def atualizarStatusagendamentoUsuarios(id_agendamento, status_agendamento, motivo_cancelamento):
        sql = text("""
            UPDATE agendamento
            SET
                motivo_cancelamento = :motivo_cancelamento,
                status_agendamento = :status_agendamento,
                data_atualizacao = :data_atualizacao
            WHERE id_agendamento =:id_agendamento        
        """)

        resultado = db.session.execute(sql, {
            "id_agendamento": id_agendamento,
            "motivo_cancelamento": motivo_cancelamento,
            "status_agendamento": status_agendamento,
            "data_atualizacao": datetime.now()     
        })

        db.session.commit()

        return resultado.rowcount > 0
    
    @staticmethod
    def atualizarStatusMotivoDoCancelamentoAgendaMensalDao(motivo_cancelamento, status_agendamento, agenda_mensal):
            sql = text("""
                UPDATE agendamento
                SET
                    motivo_cancelamento = :motivo_cancelamento,
                    status_agendamento = :status_agendamento,
                    data_atualizacao = :data_atualizacao
                WHERE data_agendamento between :data_inicial_agenda and :data_final_agenda
                and status_agendamento!=:status_agendamento_concluido
            """)
    
            resultado = db.session.execute(sql, {
                "motivo_cancelamento": motivo_cancelamento,
                "status_agendamento": status_agendamento,
                "data_atualizacao": datetime.now(),
                "data_inicial_agenda": agenda_mensal.data_inicial_mes,
                "data_final_agenda": agenda_mensal.data_final_mes,       
                "status_agendamento_concluido": EnumStatusAgendamento.CONCLUIDO.value       
            })
    
            db.session.commit()
    
            return resultado.rowcount > 0
    
    @staticmethod
    def atualizarStatusMotivoDoCancelamentoFaltasJustificadasDao(motivo_cancelamento, status_agendamento, falta_justifica):
        sql = text("""
            UPDATE agendamento
            SET
                motivo_cancelamento = :motivo_cancelamento,
                status_agendamento = :status_agendamento,
                data_atualizacao = :data_atualizacao
            WHERE 
            data_agendamento = :data_falta
            and fk_id_barbeiro = :id_barbeiro
            and hora_inicio >= :horario_inicio_falta
            and hora_fim <= :horario_final_falta
            and status_agendamento!=:status_agendamento_concluido
        """)

        resultado = db.session.execute(sql, {
            "motivo_cancelamento": motivo_cancelamento,
            "status_agendamento": status_agendamento,
            "data_atualizacao": datetime.now(),
            "data_falta": falta_justifica.data_falta,
            "id_barbeiro": falta_justifica.d_barbeiro,       
            "horario_inicio_falta": falta_justifica.horario_inicio_falta,       
            "horario_final_falta": falta_justifica.horario_final_falta,       
            "status_agendamento_concluido": EnumStatusAgendamento.CONCLUIDO.value       
        })

        db.session.commit()

        return resultado.rowcount > 0
    
    def atualizar_status_agendamento(id_agendamento:int, status_agendamento:int, data_hoje:str):
        sql = text("""
            UPDATE agendamento
            SET
                status_agendamento = :status_agendamento,
                data_atualizacao = NOW()
                
            WHERE id_agendamento = :id_agendamento
                AND data_agendamento = :data_hoje
        """)
        
        resultado = db.session.execute(sql, {
            "id_agendamento": id_agendamento,
            "status_agendamento": status_agendamento,
            "data_hoje": data_hoje
        })
        
        db.session.commit()

        return resultado.rowcount > 0
    
    def cancelar_agendamento(id_agendamento:int, data_hoje:str, motivo_cancelamento:str):
        sql = text("""
            UPDATE agendamento
            SET
                status_agendamento = 0,
                motivo_cancelamento = :motivo_cancelamento,
                data_atualizacao = NOW()
                
            WHERE id_agendamento = :id_agendamento
                AND data_agendamento = :data_hoje
        """)
        
        resultado = db.session.execute(sql, {
            "id_agendamento": id_agendamento,
            "motivo_cancelamento": motivo_cancelamento,
            "data_hoje": data_hoje
        })
        
        db.session.commit()

        return resultado.rowcount > 0

    @staticmethod
    def atualizar(agendamento: Agendamento):
        sql = text("""
            UPDATE agendamento
            SET
                data_agendamento = :data_agendamento,
                hora_inicio = :hora_inicio,
                hora_fim = :hora_fim,
                motivo_cancelamento = :motivo_cancelamento,
                status_agendamento = :status_agendamento,
                data_atualizacao = :data_atualizacao,
                fk_id_barbeiro = :fk_id_barbeiro,
                fk_id_cliente = :fk_id_cliente
            WHERE id_agendamento = :id_agendamento
        """)

        resultado = db.session.execute(sql, {
            "id_agendamento": agendamento.id_agendamento,
            "data_agendamento": agendamento.data_agendamento,
            "hora_inicio": agendamento.hora_inicio,
            "hora_fim": agendamento.hora_fim,
            "motivo_cancelamento": agendamento.motivo_cancelamento,
            "status_agendamento": agendamento.status_agendamento,
            "data_atualizacao": agendamento.data_atualizacao,
            "fk_id_barbeiro": agendamento.fk_id_barbeiro,
            "fk_id_cliente": agendamento.fk_id_cliente
        })

        db.session.commit()

        return resultado.rowcount > 0

    @staticmethod
    def excluirDao(id_agendamento: int):
        sql = text("""
            DELETE FROM agendamento
            WHERE id_agendamento = :id_agendamento
        """)

        resultado = db.session.execute(
            sql,
            {"id_agendamento": id_agendamento}
        )

        db.session.commit()

        return resultado.rowcount > 0

    @staticmethod
    def consultarAgendamentosPorPeriodoDAO(data_inicio, data_fim):

        sql = text("""
            SELECT
                a.id_agendamento,
                a.data_agendamento,
                a.hora_inicio,
                a.hora_fim,
                a.motivo_cancelamento,
                a.status_agendamento,
                a.valor_total_servicos,
                a.data_atualizacao,
                a.fk_id_barbeiro AS id_barbeiro,

                b.id_barbeiro,
                u.nome_completo,
                u.cpf,
                u.email,
                u.telefone,
                b.bio,
                u.data_ultimo_acesso

            FROM agendamento a

            INNER JOIN barbeiro b
                ON a.fk_id_barbeiro = b.id_barbeiro
            
            INNER JOIN usuario u
                ON b.id_barbeiro = u.id_usuario

            WHERE a.data_agendamento 
                BETWEEN :data_inicio AND :data_fim
                AND a.status_agendamento = 1
              
            ORDER BY
                a.data_agendamento,
                a.hora_inicio
        """)

        resultado = db.session.execute(
            sql,
            {
                "data_inicio": data_inicio,
                "data_fim": data_fim
            }
        ).mappings().all()

        return [
            AgendamentoDAO._mapear_agendamento_todos_dados(registro)
            for registro in resultado
        ]
        
    @staticmethod
    def consultarTotalAgendamentosPorPeriodoDao(data_inicio, data_final):
    
            sql = text("""
                SELECT
                    COUNT(id_agendamento)               
                FROM agendamento 
                WHERE data_agendamento BETWEEN :data_inicio AND :data_fim
        
            """)
    
            resultado = db.session.execute(
                sql,
                {
                    "data_inicio": data_inicio,
                    "data_fim": data_final
                }
            )
    
            return resultado.scalar() > 0 

    @staticmethod
    def clienteTemConflitoHorarioDao(
        id_cliente,
        data_agendamento,
        hora_inicio,
        hora_fim
    ):
        sql = text("""
            SELECT EXISTS (
                SELECT 1
                FROM agendamento a
                WHERE a.fk_id_cliente = :id_cliente
                  AND a.data_agendamento = :data_agendamento
                  AND a.hora_inicio < :hora_fim
                  AND a.hora_fim > :hora_inicio
                  AND a.status_agendamento = 1
            )
        """)

        resultado = db.session.execute(sql, {
            "id_cliente": id_cliente,
            "data_agendamento": data_agendamento,
            "hora_inicio": hora_inicio,
            "hora_fim": hora_fim
        }).scalar()

        return bool(resultado)

    @staticmethod
    def _mapear_agendamento_todos_dados(registro):

        barbeiro = Barbeiro(
            id_usuario=registro["id_barbeiro"],
            nome_completo=registro["nome_completo"],
            email=registro["email"],
            telefone=registro["telefone"],
            bio=registro["bio"],
            cpf=registro["cpf"],
            data_ultimo_acesso=registro["data_ultimo_acesso"]
        )

        #servico = Servico(
        #    id_servico=registro["id_servico"],
         #   descricao_servico=registro["descricao_servico"],
        #    valor=registro["valor"],
        #    duracao=registro["duracao"]
        #)

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

        return agendamento

    @staticmethod
    def _mapear_agendamento(registro):
        return Agendamento(
            id_agendamento=registro["id_agendamento"],
            data_agendamento=registro["data_agendamento"],
            hora_inicio=(datetime.min + registro["hora_inicio"]).time(),
            hora_fim=(datetime.min + registro["hora_fim"]).time(),
            motivo_cancelamento=registro["motivo_cancelamento"],
            status_agendamento=registro["status_agendamento"],
            data_atualizacao=registro["data_atualizacao"],
            valor_total_servicos = registro["valor_total_servicos"],
            barbeiro=None,
            cliente=None
        )

    # @staticmethod
    # def _mapear_agendamento(registro):
    #     return {
    #         "id_agendamento": str(registro["id_agendamento"]),
    #         "barbeiro": registro["nome_barbeiro"],
    #         "data": FormatarData._formatar_data(registro["data_agendamento"]),
    #         "hora_inico": FormatarHoras._formatar_hora(registro["hora_inicio"]),
    #         "hora_fim": FormatarHoras._formatar_hora(registro["hora_fim"]),
    #         "motivo_cancelamento": registro["motivo_cancelamento"],
    #         "cliente": registro["nome_cliente"],
    #         "telefone": FormatarTelefone._formatar_telefone(registro["telefone_cliente"]),
    #         "servico": registro["nome_servico"],
    #         "valor": float(registro["valor"] or 0),
    #         "status": registro["status_agendamento"],
    #     }