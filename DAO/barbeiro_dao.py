
from sqlalchemy import text
from database import db
from models import Barbeiro, Endereco, FaltaJustificadaBarbeiro
from utilitarios import FormatarHoras, FormatarTelefone
from datetime import datetime, timezone

class BarbeiroDAO:

    def realizar_login_dao(self, email: str):
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
                u.data_ultimo_acesso,
                b.id_barbeiro,
                b.data_liberacao,
                b.bio,
                b.especialidade,
                b.status_barbeiro,
                b.data_inicio_carreira
            FROM usuario u INNER JOIN barbeiro b
            ON b.id_barbeiro = u.id_usuario
            WHERE u.email = :email
            
        """)

        registro = db.session.execute(
            sql,
            {"email": email}
        ).mappings().first()

        if registro is None:
            return None

        return dict(registro)
    
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
            "data_liberacao": datetime.now(timezone.utc),
            "bio": barbeiro.bio,
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
                u.data_ultimo_acesso,

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
                u.data_ultimo_acesso,

                b.id_barbeiro,
                b.data_liberacao,
                b.bio,
                b.especialidade,
                b.status_barbeiro,
                TIMESTAMPDIFF(YEAR, b.data_inicio_carreira, CURDATE()) data_inicio_carreira,

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
        
    def consultar_barbeiro_nome(self, nome_barbeiro):
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
                    u.data_ultimo_acesso,
    
                    b.id_barbeiro,
                    b.data_liberacao,
                    b.bio,
                    b.especialidade,
                    b.status_barbeiro,
                    TIMESTAMPDIFF(YEAR, b.data_inicio_carreira, CURDATE()) data_inicio_carreira,
    
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
                WHERE u.nome_completo LIKE :nome_completo 
                ORDER BY u.nome_completo
            """)
    
            registros = db.session.execute(sql,{"nome_completo":f"%{nome_barbeiro}%"}).mappings().all()
    
            print("TOTAL de barbeiros", len(registros))
            
            return [
                self._mapear_barbeiro(registro)
                for registro in registros
            ]

    def consultar_todos_ativos(self):
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
                u.data_ultimo_acesso,

                b.id_barbeiro,
                b.data_liberacao,
                b.bio,
                b.especialidade,
                b.status_barbeiro,
                TIMESTAMPDIFF(
                    YEAR,
                    b.data_inicio_carreira,
                    CURDATE()
                ) AS data_inicio_carreira,

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

            WHERE
                u.status_usuario = 1
                AND b.status_barbeiro = 1

            ORDER BY u.nome_completo
        """)

        registros = db.session.execute(sql).mappings().all()

        return [
            self._mapear_barbeiro(registro)
            for registro in registros
        ]
    
    def consultar_agendamentos_barbeiro(self, id_barbeiro: int):
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
        
        return [
            self._mapear_agendamento(registro)
            for registro in registros
        ]

    def atualizar_informacoes_barbeiro(self, barbeiro: Barbeiro):
        sql = text("""
            UPDATE barbeiro
            SET
                bio = :bio,
                especialidade = :especialidade,
                status_barbeiro = :status_barbeiro,
                data_inicio_carreira = :data_inicio_carreira

            WHERE id_barbeiro = :id_barbeiro
        """)

        resultado = db.session.execute(sql, {
            "id_barbeiro": barbeiro.id_usuario,
            "data_liberacao": barbeiro.data_liberacao,
            "bio": barbeiro.bio,
            "especialidade": barbeiro.especialidade,
            "status_barbeiro": barbeiro.status_barbeiro,
            "data_inicio_carreira": barbeiro.data_inicio_carreira
        })

        db.session.commit()

        return resultado.rowcount > 0
    
    def atualizar_status_agendamento(self, id_agendamento:int, status_agendamento:int, data_hoje:str):
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

    def consultar_faltas_dos_barbeiros_ativo(self):
        sql = text("""
                SELECT u.nome_completo, 
                u.id_usuario,u.telefone,
                u.foto_nome_usuario, 
                u.cpf, u.data_ultimo_acesso,
                f.* 
                FROM falta_justificada_barbeiro f 
                    right join barbeiro b 
                on f.fk_barbeiro_falta_justificada = b.id_barbeiro 
                    inner join usuario u 
                on u.id_usuario = b.id_barbeiro 
                    and b.status_barbeiro = :status
                order by u.foto_nome_usuario asc, f.data_falta asc, f.horario_inicio_falta asc
                   """)
        
        resultado = db.session.execute(sql,{
            "status": True
        }).mappings().all()
         
        # uso dic pois a complexidade na busca é o(1)
        barbeiro_map: dict[int,Barbeiro]={}
            
        for linha in resultado:
            
            id_usuario_barbeiro = linha["id_usuario"]
            
            if id_usuario_barbeiro not in barbeiro_map:
                barbeiro_map[id_usuario_barbeiro] = Barbeiro(
                id_usuario=id_usuario_barbeiro,    
                nome_completo=linha["nome_completo"],
                telefone=linha["telefone"],
                cpf=linha["cpf"],
                data_ultimo_acesso=linha["data_ultimo_acesso"],
                foto_nome_usuario=linha["foto_nome_usuario"], 
                faltas_justificadas=[]     
            )
            
            if linha["id_falta_justificada"] is not None:
                barbeiro_map[id_usuario_barbeiro].faltas_justificadas.append(
                    FaltaJustificadaBarbeiro(
                        id_falta_justificada=linha["id_falta_justificada"],
                        data_falta=linha["data_falta"],
                        horario_inicio_falta=(datetime.min + linha["horario_inicio_falta"]).time(),
                        horario_final_falta=(datetime.min + linha["horario_final_falta"]).time(),
                        motivo_falta=linha["motivo_falta"] 
                    )
                )
            
        return list(barbeiro_map.values())
   
    def consultar_faltas_mensais_barbeiros_ativo(self, data_inicio_mes, data_final_mes):
        sql = text("""
                SELECT u.nome_completo, 
                u.id_usuario,u.telefone,
                u.foto_nome_usuario, 
                u.cpf, u.data_ultimo_acesso,
                f.* 
                FROM falta_justificada_barbeiro f 
                    right join barbeiro b 
                on f.fk_barbeiro_falta_justificada = b.id_barbeiro 
                    inner join usuario u 
                on u.id_usuario = b.id_barbeiro 
                    and b.status_barbeiro = :status
                WHERE 
                    f.data_falta BETWEEN :data_inicio_mes AND :data_final_mes
                order 
                    by u.foto_nome_usuario asc, f.data_falta asc, f.horario_inicio_falta asc
                """)
                            
        resultado = db.session.execute(sql,{
            "status": True,
            "data_inicio_mes": data_inicio_mes,
            "data_final_mes": data_final_mes
        }).mappings().all()
         
        # uso dic pois a complexidade na busca é o(1)
        barbeiro_map: dict[int,Barbeiro]={}
            
        for linha in resultado:
            
            id_usuario_barbeiro = linha["id_usuario"]
            
            if id_usuario_barbeiro not in barbeiro_map:
                barbeiro_map[id_usuario_barbeiro] = Barbeiro(
                id_usuario=id_usuario_barbeiro,    
                nome_completo=linha["nome_completo"],
                telefone=linha["telefone"],
                cpf=linha["cpf"],
                data_ultimo_acesso=linha["data_ultimo_acesso"],
                foto_nome_usuario=linha["foto_nome_usuario"], 
                faltas_justificadas=[]     
            )
            
            if linha["id_falta_justificada"] is not None:
                barbeiro_map[id_usuario_barbeiro].faltas_justificadas.append(
                    FaltaJustificadaBarbeiro(
                        id_falta_justificada=linha["id_falta_justificada"],
                        data_falta=linha["data_falta"],
                        horario_inicio_falta=(datetime.min + linha["horario_inicio_falta"]).time(),
                        horario_final_falta=(datetime.min + linha["horario_final_falta"]).time(),
                        motivo_falta=linha["motivo_falta"] 
                    )
                )
            
        return list(barbeiro_map.values())
                    
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
            data_ultimo_acesso=registro["data_ultimo_acesso"],

            data_liberacao=registro["data_liberacao"],
            bio=registro["bio"],
            especialidade=registro["especialidade"],
            status_barbeiro=bool(registro["status_barbeiro"]),
            data_inicio_carreira=registro["data_inicio_carreira"],

            endereco=endereco
        )

    @staticmethod
    def _mapear_agendamento(registro):
        return {
            "id": str(registro["id_agendamento"]),
            "barbeiro": registro["nome_barbeiro"],
            "data": str(registro["data_agendamento"]),
            "hora": FormatarHoras._formatar_hora(registro["hora_inicio"]),
            "cliente": registro["nome_cliente"],
            "telefone": FormatarTelefone._formatar_telefone(registro["telefone_cliente"]),
            "servico": registro["nome_servico"],
            "valor": float(registro["valor"] or 0),
            "status": registro["status_agendamento"]
        }
        