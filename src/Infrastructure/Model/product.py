from src.config.data_base import db 

class Produto(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    preco = db.Column(db.String(18), nullable=False)  # Preço com formato R$ XXX,XX
    qtd = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(10), default='Ativo', nullable=False)  # 'Ativo' ou 'Inativo'
    img = db.Column(db.String(255), nullable=True)  # URL da imagem do produto

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "preco": self.preco,
            "qtd": self.qtd,
            "status": self.status,
            "img": self.img,
            "user_id": self.user_id
        }