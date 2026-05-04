from src.Domain.sale import SaleDomain
from src.Domain.product import ProductDomain
from src.Infrastructure.Model.sale import Sale
from src.Infrastructure.Model.product import Produto
from src.Infrastructure.Model.user import User
from src.config.data_base import db

class SaleService:
    @staticmethod
    def create_sale(product_id, quantity, seller_id):
        # Verificar se o vendedor está ativo
        seller = User.query.filter_by(id=seller_id, status="Ativo").first()
        if not seller:
            raise PermissionError("Vendedor inativo ou não encontrado.")

        # Verificar se o produto existe e está ativo
        product = Produto.query.filter_by(id=product_id, status="Ativo").first()
        if not product:
            raise ValueError("Produto inativo ou não encontrado.")

        # Verificar quantidade em estoque
        try:
            stock = int(product.qtd)
        except ValueError:
            raise ValueError("Quantidade em estoque inválida.")

        if quantity > stock:
            raise ValueError("Quantidade solicitada maior que o estoque disponível.")

        # Preço no momento da venda
        price_at_sale = product.preco

        try:
            # Criar venda
            sale = Sale(product_id=product_id, quantity=quantity, price_at_sale=price_at_sale, seller_id=seller_id)
            db.session.add(sale)

            # Decrementar estoque
            product.qtd = str(stock - quantity)
            db.session.commit()

            # Retornar venda
            return SaleDomain(
                sale.id, sale.product_id, sale.quantity, sale.price_at_sale, sale.seller_id, sale.sale_date
            ).to_dict()

        except Exception as e:
            db.session.rollback()
            raise e