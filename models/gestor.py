from database import db

class Gestor(db.Model):
    __tablename__ = 'gestor'

    
    id = db.Column(
        db.Integer, 
        db.ForeignKey('usuarios.id', onupdate='restrict', ondelete='restrict'), 
        primary_key=True, 
        nullable=False
    )

    # O parêntese do ForeignKey agora fecha DEPOIS do ondelete/onupdate
    fk_cnpj_barbearia = db.Column(
        db.String(14), 
        db.ForeignKey('barbearia.cnpj', onupdate='restrict', ondelete='restrict'), 
        nullable=False, 
        unique=True
    )

    # 2. Construtor para salvar na tabela clientes
    def __init__(self, cliente_id:int, cnpj: str):
            self.cliente_id = cliente_id 
            self.fk_cnpj_barbearia = cnpj
    
    # as consultas devem ser nas classes, pois cada tipo de usuario vai ter consultas com atributos e tabelas diferentes
    @classmethod
    def consultarGestorEmail(cls,email:str, cnpj:str):
        resultado = db.session.execute(
              db.text(
               """
               select * from gestor g join usuarios u  on u.id = g.id where u.email =:email and g.fk_cnpj_barbearia=:cnpj
                """    
              ),
              {"email":email, "cnpj":cnpj}
         )
        return resultado.mappings().first()
        


    @classmethod
    def inserirGestor(cls, id_gestor:int, cnpj:str):
       
        db.session.execute(
                db.text("""
                    INSERT INTO gestor
                    (
                        id,
                        fk_cnpj_barbearia
                    )
                    VALUES
                    (
                        :id,
                        :fk_cnpj_barbearia
                    )
                """),
                {
                    "id": id_gestor,
                    "fk_cnpj_barbearia": cnpj
                }
            )
        