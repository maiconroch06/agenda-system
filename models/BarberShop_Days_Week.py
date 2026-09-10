from database import db

class BarberShopDaysWeek(db.Model):
    __tablename__ = 'barbearia_dias_da_semana'

    # Chave Primária Auto-incremental
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    barbearia_cnpj = db.Column(
        db.String(18), 
        db.ForeignKey('barbearias.cnpj', onupdate='NO ACTION', ondelete='NO ACTION'), 
        nullable=False
    )
    dia_da_semana_id = db.Column(
        db.Integer, 
        db.ForeignKey('dias_da_semana.id', onupdate='NO ACTION', ondelete='NO ACTION'), 
        nullable=False
    )
    
    horario_abertura = db.Column(db.Time, nullable=False)   
    horario_fechamento = db.Column(db.Time, nullable=False)
