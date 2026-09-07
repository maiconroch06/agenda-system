from database import db

class Address(db.Model):
    __tablename__ = 'enderecos'
    
    # 1. Definição das Colunas no MySQL (Mapeamento ORM)
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cep = db.Column(db.String(9), nullable=False)
    cidade = db.Column(db.String(100), nullable=False)
    estado_sigla = db.Column(db.String(2), nullable=False)
    logradouro = db.Column(db.Text, nullable=False)
    numero = db.Column(db.Integer, nullable=False)
    bairro = db.Column(db.String(100), nullable=False)
    sequencia = db.Column(db.String(50), default="1")
    complemento = db.Column(db.Text, nullable=True)
    
    # Chave Estrangeira vinculada à tabela 'usuarios' no campo 'cpf'
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id', ondelete="CASCADE"), nullable=False)

    # 2. Construtor original mantido (com suporte a argumentos opcionais/default)
    def __init__(self, cep, cidade, estado_sigla, logradouro, numero, bairro, usuario_id, sequencia="1", complemento=None):
        self.cep = cep
        self.cidade = cidade
        self.estado_sigla = estado_sigla
        self.logradouro = logradouro
        self.numero = numero
        self.bairro = bairro
        self.usuario_id = usuario_id
        self.sequencia = sequencia
        self.complemento = complemento

    def to_dict(self):
        return {
            'id': self.id,
            'cep': self.cep,
            'cidade': self.cidade,
            'estado_sigla': self.estado_sigla,
            'logradouro': self.logradouro,
            'numero': self.numero,
            'bairro': self.bairro,
            'usuario_id': self.usuario_id,
            'sequencia': self.sequencia,
            'complemento': self.complemento
        }

    # 3. Serialização para retornar nas rotas da API
    def to_dict(self):
        return {
            'id': self.id,
            'cep': self.cep,
            'cidade': self.cidade,
            'estado_sigla': self.estado_sigla,
            'logradouro': self.logradouro,
            'numero': self.numero,
            'bairro': self.bairro,
            'usuario_cpf': self.usuario_cpf,
            'sequencia': self.sequencia,
            'complemento': self.complemento
        }

    # ============================================================
    # MÉTODOS CRUD SUBSTITUÍDOS PELO ECOSSISTEMA DO SQLALCHEMY
    # ============================================================

    # CREATE
    def salvar(self):
        db.session.add(self)
        db.session.commit()
        return self.sequencia

    # READ - BUSCAR POR CPF + SEQUÊNCIA
    @classmethod
    def buscar_por_cpf_e_sequencia(cls, usuario_cpf, sequencia):
        return cls.query.filter_by(usuario_cpf=usuario_cpf, sequencia=sequencia).first()

    # READ - LISTAR ENDEREÇOS DO USUÁRIO
    @classmethod
    def listar_por_usuario(cls, usuario_cpf):
        return cls.query.filter_by(usuario_cpf=usuario_cpf).order_by(cls.sequencia.asc()).all()

    # READ - LISTAR TODOS
    @classmethod
    def listar_todos(cls):
        return cls.query.order_by(cls.usuario_cpf.asc(), cls.sequencia.asc()).all()

    # UPDATE
    def atualizar(self):
        # Como o objeto já foi modificado na rota, basta salvar a sessão corrente
        db.session.commit()
        return True

    # DELETE
    @classmethod
    def excluir_por_cpf_e_sequencia(cls, usuario_cpf, sequencia):
        endereco = cls.buscar_por_cpf_e_sequencia(usuario_cpf, sequencia)
        if endereco:
            db.session.delete(endereco)
            db.session.commit()
            return True
        return False
