from database import db
from datetime import datetime, timezone

class User(db.Model):
    __tablename__ = 'usuarios'
    
    # 1. Mapeamento das Colunas no MySQL (Sem CPF)
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome_completo = db.Column(db.String(50), nullable=False)
    telefone = db.Column(db.String(15))
    email = db.Column(db.String(255), unique=True, nullable=False)
    senha_hash = db.Column(db.String(255), nullable=False)
    foto_path = db.Column(db.String(255))
    ativo = db.Column(db.Boolean, default=True, nullable=False)
    data_cadastro = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    data_atualizacao = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    # Correto: apontando para id_endereco
    endereco_id = db.Column(db.Integer, db.ForeignKey('enderecos.id_endereco'), nullable=True)


    # Relacionamento virtual apontando para a classe Address
    enderecos = db.relationship('Address', backref='usuarios', lazy=True)

    # 2. Construtor Ajustado para os dados do formulário (Sem CPF)
    def __init__(self, nome_completo, telefone, email, senha, foto):
        self.nome_completo = nome_completo
        self.telefone = telefone
        self.email = email
        self.senha_hash = senha   

    # 3. Serialização para a Sessão / Respostas JSON
    def to_dict(self):
        return {
            'id': self.id, 
            'nome_completo': self.nome_completo,
            'telefone': self.telefone,
            'email': self.email,
            'senha': self.senha_hash,  
        }

    # ============================================================
    # MÉTODOS CRUD OFICIAIS (CORRIGIDOS)
    # ============================================================

    # CREATE - Salva o usuário e retorna o ID auto-incremental gerado pelo MySQL
    def salvar(self):
        db.session.add(self)
        db.session.commit()
        return self.id 

    # READ - Busca o usuário diretamente pela Chave Primária (id)
    @classmethod
    def buscar_por_id(cls, id):
        return db.session.get(cls, id)

    # READ - 🔥 CORRIGIDO: Atualizado para a sintaxe moderna db.select
    @classmethod
    def buscar_por_email(cls, email):
        return db.session.scalar(db.select(cls).filter_by(email=email))

    # READ - 🔥 CORRIGIDO: Atualizado para a sintaxe moderna db.select e scalars().all()
    @classmethod
    def listar_todos(cls):
        stmt = db.select(cls).order_by(cls.nome_completo.asc())
        return db.session.scalars(stmt).all()

    # UPDATE - Confirma as alterações feitas no objeto
    def atualizar(self):
        db.session.commit()
        return True

    # DELETE - 🔥 CORRIGIDO: Mantém a segurança do cascade deletando o objeto da sessão
    @classmethod
    def excluir_por_id(cls, id):
        usuario = cls.buscar_por_id(id)
        if usuario:
            db.session.delete(usuario)
            db.session.commit()
            return True
        return False
