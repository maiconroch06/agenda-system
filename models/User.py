from database import db

class User(db.Model):
    __tablename__ = 'usuarios'
    
    # 1. Mapeamento das Colunas no MySQL (Sem CPF)
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(50), nullable=False)
    telefone = db.Column(db.String(15))
    email = db.Column(db.String(255), unique=True, nullable=False)
    senha_hash = db.Column(db.String(255), nullable=False)
    foto_path = db.Column(db.String(255))

    # Relacionamento virtual apontando para a classe Address
    enderecos = db.relationship('Address', backref='usuario', lazy=True, cascade="all, delete-orphan")

    # 2. Construtor Ajustado para os dados do formulário (Sem CPF)
    def __init__(self, nome, telefone, email, senha, foto):
        self.nome = nome
        self.telefone = telefone
        self.email = email
        self.senha_hash = senha  
        self.foto_path = foto    

    # 3. Serialização para a Sessão / Respostas JSON
    def to_dict(self):
        return {
            'id': self.id, 
            'nome': self.nome,
            'telefone': self.telefone,
            'email': self.email,
            'senha': self.senha_hash,  
            'foto_path': self.foto_path,
        }

    # ============================================================
    # MÉTODOS CRUD OFICIAIS (APENAS POR ID E E-MAIL)
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

    # READ - Busca por E-mail (Essencial para a rota de Login posterior)
    @classmethod
    def buscar_por_email(cls, email):
        return cls.query.filter_by(email=email).first()

    # READ - Lista todos os usuários por ordem alfabética
    @classmethod
    def listar_todos(cls):
        return cls.query.order_by(cls.nome.asc()).all()

    # UPDATE - Confirma as alterações feitas no objeto
    def atualizar(self):
        db.session.commit()
        return True

    # DELETE - Remove o usuário do banco usando o ID
    @classmethod
    def excluir_por_id(cls, id):
        usuario = cls.buscar_por_id(id)
        if usuario:
            db.session.delete(usuario)
            db.session.commit()
            return True
        return False
