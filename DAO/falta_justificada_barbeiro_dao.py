
from datetime import datetime

from sqlalchemy import text
from database import db
from models import FaltaJustificadaBarbeiro
from DAO.barbeiro_dao import BarbeiroDAO
from models.barbeiro import Barbeiro


class FaltaJustificadaBarbeiroDAO:

    def cadastrar(self,  falta_justificada: FaltaJustificadaBarbeiro):
        sql = text("""
            INSERT INTO falta_justificada_barbeiro (
                data_falta,
                horario_inicio_falta,
                horario_final_falta,
                motivo_falta,
                fk_barbeiro_falta_justificada
            ) VALUES (
                :data_falta,
                :horario_inicio_falta,
                :horario_final_falta,
                :motivo_falta,
                :fk_barbeiro_falta_justificada
            )
        """)

        resultado = db.session.execute(sql, {
            "data_falta": falta_justificada.data_falta,
            "horario_inicio_falta": falta_justificada.horario_inicio_falta,
            "horario_final_falta": falta_justificada.horario_final_falta,
            "motivo_falta": falta_justificada.motivo_falta,
            "fk_barbeiro_falta_justificada": falta_justificada.id_barbeiro
        })

        db.session.commit()

        return resultado.lastrowid > 0

    def consultar_todos_por_barbeiro(self, id_barbeiro: int):
        sql = text("""
            SELECT
                id_falta_justificada,
                data_falta,
                horario_inicio_falta,
                horario_final_falta,
                motivo_falta,
                fk_barbeiro_falta_justificada
            FROM falta_justificada_barbeiro
            WHERE fk_barbeiro_falta_justificada = :id_barbeiro
            ORDER BY data_falta DESC, horario_inicio_falta asc
        """)

        registros = db.session.execute(
            sql,
            {"id_barbeiro": id_barbeiro}
        ).mappings().all()

        return [
            self._mapear_falta(registro)
            for registro in registros
        ]

    def atualizar(self, falta: FaltaJustificadaBarbeiro):
        sql = text("""
            UPDATE falta_justificada_barbeiro
            SET
                data_falta = :data_falta,
                horario_inicio_falta = :horario_inicio_falta,
                horario_final_falta = :horario_final_falta,
                motivo_falta = :motivo_falta
            WHERE id_falta_justificada = :id_falta_justificada
        """)

        resultado = db.session.execute(sql, {
            "id_falta_justificada": falta.id_falta_justificada,
            "data_falta": falta.data_falta,
            "horario_inicio_falta": falta.horario_inicio_falta,
            "horario_final_falta": falta.horario_final_falta,
            "motivo_falta": falta.motivo_falta,
        })

        db.session.commit()

        return resultado.rowcount > 0

    def excluir(self, id_falta_justificada: int):
        sql = text("""
            DELETE FROM falta_justificada_barbeiro
            WHERE id_falta_justificada = :id_falta_justificada
        """)

        resultado = db.session.execute(
            sql,
            {"id_falta_justificada": id_falta_justificada}
        )

        db.session.commit()

        return resultado.rowcount > 0
    
    def verificar_falta_justificativa_existente_barbeiro_dao(self, falta_justificada):
        sql = text("""
            SELECT count(id_falta_justificada) 
            FROM falta_justificada_barbeiro
            where data_falta = :data_falta 
            and horario_final_falta >= :hora_inicial_falta
            AND horario_inicio_falta <= :horario_final_falta
            and fk_barbeiro_falta_justificada = :fk_barbeiro_falta_justificada;
        """)

        resultado = db.session.execute(
            sql,
            {
                "data_falta": falta_justificada.data_falta,
                "hora_inicial_falta": falta_justificada.horario_inicio_falta,
                "horario_final_falta": falta_justificada.horario_final_falta,
                "fk_barbeiro_falta_justificada": falta_justificada.id_barbeiro
                }
        )

        return resultado.scalar() > 0
    
    def verificar_atualizacao_falta_justificativa_existente_barbeiro_dao(self,  falta_justificada):
            sql = text("""
                SELECT count(id_falta_justificada) 
                FROM falta_justificada_barbeiro
                where data_falta = :data_falta 
                AND horario_final_falta >= :hora_inicial_falta
                AND horario_inicio_falta <= :horario_final_falta
                and id_falta_justificada != :id_falta_justificada and fk_barbeiro_falta_justificada = :fk_barbeiro_falta_justificada
            """)
    
            resultado = db.session.execute(
                sql,
                {   "id_falta_justificada":falta_justificada.id_falta_justificada,
                    "data_falta": falta_justificada.data_falta,
                    "hora_inicial_falta": falta_justificada.horario_inicio_falta,
                    "horario_final_falta": falta_justificada.horario_final_falta,
                    "fk_barbeiro_falta_justificada": falta_justificada.id_barbeiro
                    }
            )
    
            return resultado.scalar() > 0

    @staticmethod
    def consultar_faltas_por_periodo(data_inicio, data_fim):

        sql = text("""
            SELECT
                f.id_falta_justificada,
                f.data_falta,
                f.horario_inicio_falta,
                f.horario_final_falta,
                f.motivo_falta,
                f.fk_barbeiro_falta_justificada AS id_barbeiro

            FROM falta_justificada_barbeiro f

            INNER JOIN barbeiro b
                ON b.id_barbeiro = f.fk_barbeiro_falta_justificada

            INNER JOIN usuario u
                ON u.id_usuario = b.id_barbeiro

            WHERE f.data_falta BETWEEN :data_inicio AND :data_fim

            ORDER BY
                f.data_falta,
                f.horario_inicio_falta
        """)

        resultado = db.session.execute(
            sql,
            {
                "data_inicio": data_inicio,
                "data_fim": data_fim
            }
        ).mappings().all()

        return resultado
  
    def consultar_faltas_dos_barbeiros_ativo(self):
            sql = text("""
                    SELECT u.nome_completo, 
                    u.id_usuario,u.telefone,
                    u.foto_usuario, 
                    u.cpf, u.data_ultimo_acesso,
                    f.* 
                    FROM falta_justificada_barbeiro f 
                        right join barbeiro b 
                    on f.fk_barbeiro_falta_justificada = b.id_barbeiro 
                        inner join usuario u 
                    on u.id_usuario = b.id_barbeiro 
                        and b.status_barbeiro = :status
                    order by u.foto_usuario asc, f.data_falta asc, f.horario_inicio_falta asc
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
                    foto_usuario=linha["foto_usuario"], 
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
       
    def consultar_faltas_barbeiros_ativo_periodo(self, data_inicio_mes, data_final_mes):
            sql = text("""
                    SELECT u.nome_completo, 
                    u.id_usuario,u.telefone,
                    u.foto_usuario, 
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
                        by u.foto_usuario asc, f.data_falta asc, f.horario_inicio_falta asc
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
                    foto_usuario=linha["foto_usuario"], 
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
        
        
  
    def _mapear_falta(self, registro):
       
        return FaltaJustificadaBarbeiro(
            id_falta_justificada=registro["id_falta_justificada"],
            data_falta=registro["data_falta"],
            horario_inicio_falta=registro["horario_inicio_falta"],
            horario_final_falta=registro["horario_final_falta"],
            motivo_falta=registro["motivo_falta"],
           
        )
