from Infrastructure.Model.sale import Sale
from Infrastructure.Model.product import Product
from config.data_base import db


class SaleService:

    @staticmethod
    def create_sale(seller_id, data):
        product_id = data.get("product_id")
        quantity = data.get("quantity")

        if not product_id or not quantity:
            raise Exception("Campos obrigatórios: product_id, quantity")

        product = Product.query.filter_by(id=product_id, seller_id=seller_id).first()

        if not product:
            raise Exception("Produto não encontrado")

        if not product.status:
            raise Exception("Produto inativo não pode ser vendido")

        if quantity > product.quantity:
            raise Exception(f"Estoque insuficiente. Disponível: {product.quantity}")

        sale = Sale(
            product_id=product.id,
            quantity=quantity,
            price_at_moment=product.price
        )

        product.quantity -= quantity

        db.session.add(sale)
        db.session.commit()

        return sale

    @staticmethod
    def list_sales(seller_id):
        sales = Sale.query.join(Product).filter(Product.seller_id == seller_id).all()
        return sales