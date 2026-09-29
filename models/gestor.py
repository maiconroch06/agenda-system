from database import db
from .Barbearia import Barbearia


class Gestor(db.Model):
    __tablename__ = 'gestor'

    
    id = db.Column(
        db.Integer, 
        db.ForeignKey('usuarios.id', onupdate='CASCADE', ondelete='CASCADE'), 
        primary_key=True, 
        nullable=False
    )

    # O parêntese do ForeignKey agora fecha DEPOIS do ondelete/onupdate
    fk_cnpj_barbearia = db.Column(
        db.String(14), 
        db.ForeignKey('fk_cnpj_barbearia', onupdate='CASCADE', ondelete='CASCADE'), 
        nullable=False
    )

    # 2. Construtor para salvar na tabela clientes
    def __init__(self, cliente_id:int, cnpj: str):
            self.cliente_id = cliente_id 
            self.fk_cnpj_barbearia = cnpj
            


    # CREATE - Salva o usuário e retorna o ID auto-incremental gerado pelo MySQL
    def salvar(self):
        db.session.add(self)
        db.session.commit()
        return self.cliente_id


    @classmethod
    def inserirGestor(cls, id_gestor:int, cnpj:str):
            
            gestor = db.session.scalars(db.select(cls)).first()
            
            if  gestor is None:

                gestor = cls(
                    id= id_gestor,
                    fk_cnpj_barbearia= cnpj,  
                )

                db.session.add(gestor)
                db.session.commit()
                    
            return gestor.id