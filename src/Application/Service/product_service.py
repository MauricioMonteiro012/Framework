from genericpath import exists
import random  
import string
from werkzeug.security import generate_password_hash, check_password_hash   
from src.Domain.product import ProductDomain
from src.Infrastructure.Model.product import Produto
from src.Infrastructure.Model.user import User
from src.config.data_base import db

class ProductService:
    @staticmethod
    def cad_products(nome, preco, qtd, img, user_id):
        
        user_exists = db.session.query(db.exists().where(User.id == user_id, User.status == "Ativo")).scalar()
        
        exists = Produto.query.filter_by(nome=nome, user_id=user_id).first()
        if exists:
            raise ValueError({"error": "Você já cadastrou um produto com esse nome"}, 400)
        
        if not user_exists:
            raise PermissionError("Usuário não encontrado ou inativo.")
        
        if not nome or preco < 0:
            raise ValueError("Dados inválidos para cadastro.")

        try:
            # 2. Criação da instância da model
            product = Produto(nome=nome, preco=preco, qtd=qtd, img=img, user_id=user_id)
            
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
        products = Produto.query.filter_by(user_id=user_id).all()
        return [ProductDomain(p.id, p.nome, p.preco, p.qtd, p.status, p.img, p.user_id).to_dict() for p in products]
    
    @staticmethod
    def get_product_details(product_id, user_id):
        # Busca o produto
        product = Produto.query.filter_by(id=product_id).first()
        
        if not product:
            raise ValueError("Produto não encontrado.")
        
        # Valida se o produto pertence ao usuário autenticado
        if product.user_id != user_id:
            raise PermissionError("Você não tem permissão para visualizar este produto.")
        
        return ProductDomain(product.id, product.nome, product.preco, product.qtd, product.status, product.img, product.user_id).to_dict()
    
    @staticmethod
    def edit_product(product_id, user_id, nome, preco, qtd, img):
        # Busca o produto
        product = Produto.query.filter_by(id=product_id).first()
        
        if not product:
            raise ValueError("Produto não encontrado.")
        
        # Valida se o produto pertence ao usuário autenticado
        if product.user_id != user_id:
            raise PermissionError("Você não tem permissão para editar este produto.")
        
        # Atualiza apenas os campos fornecidos
        if nome is not None:
            # Valida se já existe outro produto com o mesmo nome
            exists = Produto.query.filter_by(nome=nome, user_id=user_id).filter(Produto.id != product_id).first()
            if exists:
                raise ValueError("Você já cadastrou um produto com esse nome.")
            product.nome = nome
        
        if preco is not None:
            if preco < 0:
                raise ValueError("O preço não pode ser negativo.")
            product.preco = preco
        
        if qtd is not None:
            product.qtd = qtd
        
        if img is not None:
            product.img = img
        
        try:
            db.session.commit()
            return ProductDomain(product.id, product.nome, product.preco, product.qtd, product.status, product.img, product.user_id).to_dict()
        except Exception as e:
            db.session.rollback()
            raise e
    
    @staticmethod
    def inactivate_product(product_id, user_id):
        # Busca o produto
        product = Produto.query.filter_by(id=product_id).first()
        
        if not product:
            raise ValueError("Produto não encontrado.")
        
        # Valida se o produto pertence ao usuário autenticado
        if product.user_id != user_id:
            raise PermissionError("Você não tem permissão para inativar este produto.")
        
        # Inativa o produto
        product.status = 'Inativo'
        
        try:
            db.session.commit()
            return ProductDomain(product.id, product.nome, product.preco, product.qtd, product.status, product.img, product.user_id).to_dict()
        except Exception as e:
            db.session.rollback()
            raise e