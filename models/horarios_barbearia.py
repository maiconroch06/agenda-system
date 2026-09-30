from database import db

class HorariosBarbearia(db.Model):
    __tablename__ = 'horarios_barbearia'

    # Chave Primária Auto-incremental
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    horario_abertura = db.Column(db.Time, nullable=False)   
    horario_fechamento = db.Column(db.Time, nullable=False)
    data_mes = db.Column(db.Date, nullable=False)
    horario_descanso_inicio = db.Column(db.Time, nullable=False)   
    horario_descanso_fim = db.Column(db.Time, nullable=False)

    fk_dia_da_semana = db.Column(
        db.Integer, 
        db.ForeignKey('dias_da_semana.id', onupdate='RESTRICT', ondelete='RESTRICT'), 
        nullable=False
    )
    
    
