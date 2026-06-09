import os
import uuid
from werkzeug.utils import secure_filename
from Infrastructure.Model.product import Product
from config.data_base import db

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

class ProductService:

    @staticmethod
    def create_product(seller_id, data, file=None):
        name = data.get("name")
        price = data.get("price")
        quantity = data.get("quantity")

        if not name or price is None or quantity is None:
            raise Exception("Campos obrigatórios: name, price, quantity")

        image_url = None
        if file and allowed_file(file.filename):
            ext = file.filename.rsplit('.', 1)[1].lower()
            filename = f"{uuid.uuid4().hex}.{ext}"
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            image_url = f"/uploads/{filename}"

        product = Product(
            seller_id=seller_id,
            name=name,
            price=float(price),
            quantity=int(quantity),
            image_url=image_url,
            status=True
        )

        db.session.add(product)
        db.session.commit()
        return product

    @staticmethod
    def list_products(seller_id):
        return Product.query.filter_by(seller_id=seller_id).all()

    @staticmethod
    def get_product(seller_id, product_id):
        product = Product.query.filter_by(id=product_id, seller_id=seller_id).first()
        if not product:
            raise Exception("Produto não encontrado")
        return product

    @staticmethod
    def update_product(seller_id, product_id, data, file=None):
        product = Product.query.filter_by(id=product_id, seller_id=seller_id).first()
        if not product:
            raise Exception("Produto não encontrado")

        product.name = data.get("name", product.name)
        product.price = float(data.get("price", product.price))
        product.quantity = int(data.get("quantity", product.quantity))

        if file and allowed_file(file.filename):
            ext = file.filename.rsplit('.', 1)[1].lower()
            filename = f"{uuid.uuid4().hex}.{ext}"
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            product.image_url = f"/uploads/{filename}"

        db.session.commit()
        return product

    @staticmethod
    def inactivate_product(seller_id, product_id):
        product = Product.query.filter_by(id=product_id, seller_id=seller_id).first()
        if not product:
            raise Exception("Produto não encontrado")
        product.status = False
        db.session.commit()
        return product
    
    @staticmethod
    def activate_product(seller_id, product_id):
        product = Product.query.filter_by(id=product_id, seller_id=seller_id).first()
        if not product:
            raise Exception("Produto não encontrado")
        
        product.status = True  # Define o status como ativo novamente
        db.session.commit()
        return product