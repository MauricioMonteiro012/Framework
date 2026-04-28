from src.config.data_base import db 

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    cnpj = db.Column(db.String(18), unique=True, nullable=False)  # CNPJ com formato XX.XXX.XXX/XXXX-XX
    email = db.Column(db.String(100), unique=True, nullable=False)
    celular = db.Column(db.String(15), nullable=False)  # Formato +55XXXXXXXXXX
    password = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(10), default='Inativo', nullable=False)  # 'Ativo' ou 'Inativo'
    activation_code = db.Column(db.String(4), nullable=True)  # Código de 4 dígitos para ativação
    
    produtos = db.relationship('Produto', backref='user', lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "cnpj": self.cnpj,
            "email": self.email,
            "celular": self.celular,
            "status": self.status
        }