from database import db

class BarberHasServicos(db.Model):
    __tablename__ = 'barbeiro_has_Servicos'

    # Chaves Primárias Compostas e Chaves Estrangeiras
    servicos_id = db.Column(
        db.Integer, 
        db.ForeignKey('servicos.id_servicos', onupdate='CASCADE', ondelete='CASCADE'), 
        primary_key=True, 
        nullable=False
    )
    barbeiro_id = db.Column(
        db.Integer, 
        db.ForeignKey('barbeiros.barbeiro_id', onupdate='CASCADE', ondelete='CASCADE'), 
        primary_key=True, 
        nullable=False
    )
    ativo = db.Column(db.Boolean, default=True, nullable=False)
