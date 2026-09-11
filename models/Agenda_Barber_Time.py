from database import db

class AgendaBarberTime(db.Model):
    __tablename__ = 'agenda_barbeiro_horarios'

    # Chave Primária Auto-incremental
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    barbeiro_id = db.Column(
        db.Integer, 
        db.ForeignKey('barbeiros.barbeiro_id', onupdate='NO ACTION', ondelete='NO ACTION'), 
        nullable=False
    )
    dias_da_semana_id = db.Column(
        db.Integer, 
        db.ForeignKey('dias_da_semana.id', onupdate='NO ACTION', ondelete='NO ACTION'), 
        nullable=False
    )
    
    horario_inicial = db.Column(db.Time, nullable=False) 
    horario_final = db.Column(db.Time, nullable=False)   
    numero_semana = db.Column(db.Integer, nullable=False)
    ano = db.Column(db.Integer, nullable=False)
    intervalo_descanso = db.Column(db.Integer, nullable=False)

    # Configuração do Índice Único Composto (Unique Index)
    __table_args__ = (
        db.UniqueConstraint(
            'barbeiro_id', 
            'dias_da_semana_id', 
            'horario_inicial', 
            'horario_final', 
            'numero_semana', 
            'ano',
            'intervalo_descanso',
            name='unique_agenda_barbeiro'
        ),
    )
