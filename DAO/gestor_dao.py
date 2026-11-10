
from sqlalchemy import text
from database import db
from models import Gestor


class GestorDAO:
   
    def realizar_login_dao(self, email):
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
                g.fk_cnpj_barbearia
            FROM usuario u
            INNER JOIN gestor g ON g.id_gestor = u.id_usuario
            WHERE u.email = :email
        """)

        registro = db.session.execute(
            sql,
            {"email": email}
        ).mappings().first()       

        
        return dict(registro) if registro else None
   

