from database import db

class HorariosBarbeiro(db.Model):
    __tablename__ = 'horarios_barbeiro'

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

    # Configuração do Índice Único Composto (Unique Index)
    __table_args__ = (
        db.UniqueConstraint(
           'fk_dia_da_semana', 
            'horario_abertura', 
            'horario_fechamento', 
            'data_mes', 
            'horario_descanso_inicio',
            'horario_descanso_fim',
            name='unique_horarios_barbeiro'
        ),
    )
