from database import db
from datetime import datetime, timezone

class Scheduling(db.Model):
    __tablename__ = 'agendamento'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    servico_id = db.Column(db.Integer, nullable=False)
    barbeiro_id = db.Column(db.Integer, nullable=False)
    barbearia_cnpj = db.Column(db.String(18), nullable=False)
    cliente_id = db.Column(db.Integer, nullable=False)
    data_agendamento = db.Column(db.Date, nullable=False)
    hora_inicio = db.Column(db.Time, nullable=False)
    hora_fim = db.Column(db.Time, nullable=False)
    status_agendamento = db.Column(db.Integer, nullable=False)
    data_cadastro = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    data_atualizacao = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    __table_args__ = (
        db.ForeignKeyConstraint(
            ['barbearia_cnpj', 'cliente_id'],
            ['clientes.barbearia_cnpj', 'clientes.cliente_id'],
            onupdate='CASCADE',
            ondelete='CASCADE',
            name='fk_agendamento_cliente'
        ),
        db.ForeignKeyConstraint(
            ['servico_id', 'barbeiro_id'],
            ['barbeiro_has_Servicos.servicos_id', 'barbeiro_has_Servicos.barbeiro_id'],
            onupdate='CASCADE',
            ondelete='CASCADE',
            name='fk_agendamento_barbeiro_servico'
        ),
    )