
from sqlalchemy import text
from database import db
from models import Barbeiro, Endereco, Cliente, Servico, Agendamento


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
                u.data_atualizacao,
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
            "data_liberacao": barbeiro.data_liberacao,
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

    def consultar_agendamentos_barbeiro(self, id_barbeiro: int):
        sql = text("""
            # Consulta serviços ativos
            WITH servicos_ativos AS (
                SELECT 
                    id_servico,
                    descricao_servico AS nome_servico,
                    valor,
                    status_servico
                FROM servico
                
                WHERE status_servico = 1
            ),

            # Consulta barbeiros ativos
            barbeiros_ativos AS (
                SELECT
                    u.id_usuario,
                    b.id_barbeiro,
                    u.nome_completo AS nome_barbeiro,
                    u.status_usuario,
                    b.status_barbeiro
                FROM usuario u
                
                JOIN barbeiro b
                    ON u.id_usuario = b.id_barbeiro
                    
                WHERE b.status_barbeiro = 1
                    AND id_barbeiro = :id_barbeiro
            ),

            # Consulta clientes ativos
            clientes_ativos AS (
                SELECT
                    u.id_usuario,
                    c.id_cliente,
                    u.nome_completo AS nome_cliente,
                    u.telefone AS telefone_cliente,
                    u.status_usuario
                    
                FROM usuario u
                
                JOIN cliente c
                    ON u.id_usuario = c.id_cliente
            )

            # Consulta todos os agendamentos validos de um barbeiro - Exibição para o BARBEIRO
            SELECT
                # Chave primaria e estranjeiras
                a.id_agendamento,
                a.fk_id_servico,
                a.fk_id_barbeiro,
                a.fk_id_cliente,
                a.status_agendamento,
                # Informações serviço
                s.nome_servico,
                s.valor,
                # Informações data-hora agendamento
                a.data_agendamento,
                a.hora_inicio,
                a.hora_fim,
                # Informação barberio
                b.nome_barbeiro,
                # Informações cliete
                c.nome_cliente,
                c.telefone_cliente
                
            FROM agendamento a

            JOIN servicos_ativos s
                ON a.fk_id_servico = s.id_servico

            JOIN barbeiros_ativos b
                ON a.fk_id_barbeiro = b.id_barbeiro
                
            JOIN clientes_ativos c
                ON a.fk_id_cliente = c.id_cliente
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
            "hora": BarbeiroDAO._formatar_hora(registro["hora_inicio"]),
            "cliente": registro["nome_cliente"],
            "telefone": BarbeiroDAO._formatar_telefone(registro["telefone_cliente"]),
            "servico": registro["nome_servico"],
            "valor": float(registro["valor"] or 0),
            "status": registro["status_agendamento"]
        }
        return mapa_status.get(int(status_agendamento), "")
            