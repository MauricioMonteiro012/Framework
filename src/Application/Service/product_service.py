import random  
import string
from werkzeug.security import generate_password_hash, check_password_hash   
from src.Domain.product import ProductDomain
from src.Infrastructure.Model.product import Product, User
from src.config.data_base import db

class ProductService:
    @staticmethod
    def cad_products(nome, preco, qtd, img, user_id):
        
        user_exists = db.session.query(db.exists().where(User.id == user_id, User.status == "Ativo")).scalar()
        
        if not user_exists:
            raise PermissionError("Usuário não encontrado ou inativo.")
        
        if not nome or preco < 0:
            raise ValueError("Dados inválidos para cadastro.")

        try:
            # 2. Criação da instância da model
            product = Product(nome=nome, preco=preco, qtd=qtd, img=img, user_id=user_id)
            
            db.session.add(product)
            db.session.commit()

            # 3. Retorno formatado pelo Domain
            return ProductDomain(
                product.id, product.nome, product.preco, 
                product.qtd, product.status, product.img, product.user_id
            ).to_dict()
            
        except Exception as e:
            db.session.rollback()
            # Logar o erro 'e' aqui seria ideal
            raise e
        
    @staticmethod
    def list_products(user_id):
        products = Product.query.filter_by(user_id=user_id).all()
        return [ProductDomain(p.id, p.nome, p.preco, p.qtd, p.status, p.img).to_dict() for p in products]