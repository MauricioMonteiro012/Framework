from Infrastructure.Model.product import Product
from Infrastructure.Model.sale import Sale
from config.data_base import db
from sqlalchemy import func


class DashboardService:

    @staticmethod
    def get_dashboard(seller_id):

        # Total de produtos ativos em estoque
        total_products = Product.query.filter_by(
            seller_id=seller_id, status=True
        ).count()

        # Valor total vendido
        total_revenue = db.session.query(
            func.sum(Sale.quantity * Sale.price_at_moment)
        ).join(Product).filter(Product.seller_id == seller_id).scalar() or 0

        # Produtos mais vendidos (top 5)
        top_products = db.session.query(
            Product.name,
            func.sum(Sale.quantity).label('total_sold')
        ).join(Sale, Sale.product_id == Product.id)\
         .filter(Product.seller_id == seller_id)\
         .group_by(Product.id)\
         .order_by(func.sum(Sale.quantity).desc())\
         .limit(5).all()

        # Histórico de vendas
        sales = Sale.query.join(Product).filter(
            Product.seller_id == seller_id
        ).order_by(Sale.date.desc()).limit(10).all()

        return {
            "total_products": total_products,
            "total_revenue": round(total_revenue, 2),
            "top_products": [
                {"name": p.name, "total_sold": p.total_sold}
                for p in top_products
            ],
            "recent_sales": [s.to_dict() for s in sales]
        }