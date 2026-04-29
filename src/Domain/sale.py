class SaleDomain:
    def __init__(self, id, product_id, quantity, price_at_sale, seller_id, sale_date):
        self.id = id
        self.product_id = product_id
        self.quantity = quantity
        self.price_at_sale = price_at_sale
        self.seller_id = seller_id
        self.sale_date = sale_date

    def to_dict(self):
        return {
            "id": self.id,
            "product_id": self.product_id,
            "quantity": self.quantity,
            "price_at_sale": self.price_at_sale,
            "seller_id": self.seller_id,
            "sale_date": self.sale_date.isoformat() if self.sale_date else None
        }