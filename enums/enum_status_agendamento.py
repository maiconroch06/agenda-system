from enum import Enum


class EnumStatusAgendamento(Enum):
    """Docstring for MyEnum."""
    CANCELADO = 0
    SERVICO_AGENDADO = 1
    FINALIZADO = 2
    EM_ANDAMENTO = 3
    