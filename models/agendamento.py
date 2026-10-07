from database import db
from sqlalchemy.dialects.mysql import TINYINT

class Agendamento(db.Model):
    __tablename__ = 'agendamento'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    data_agendamento = db.Column(db.Date, nullable=False)
    hora_inicio = db.Column(db.Time, nullable=False)
    hora_fim = db.Column(db.Time, nullable=False)
    status_agendamento = db.Column(TINYINT(1), nullable=False)
    data_atualizacao = db.Column(db.DateTime,  nullable=False)
    fk_id_servico = db.Column(db.Integer, nullable=False)
    fk_id_barbeiro = db.Column(db.Integer, nullable=False)
    fk_id_cliente = db.Column(db.Integer, db.ForeignKey('clientes.id', onupdate='RESTRICT', ondelete='RESTRICT'), nullable=False)
  
    db.ForeignKeyConstraint(
        ['fk_id_servico', 'fk_id_barbeiro'],
        ['barbeiro_has_Servicos.id_servicos', 'barbeiro_has_Servicos.id_barbeiro'],
            onupdate='RESTRICT',
            ondelete='RESTRICT',
            name='fk_agendamento_barbeiro_servico'
        )