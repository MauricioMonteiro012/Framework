from flask import request, jsonify
from Application.Service.sale_service import SaleService


class SaleController:

    @staticmethod
    def create_sale(current_user):
        data = request.get_json()
        try:
            sale = SaleService.create_sale(current_user.id, data)
            return jsonify({
                "message": "Venda registrada com sucesso",
                "sale": sale.to_dict()
            }), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 400

    @staticmethod
    def list_sales(current_user):
        sales = SaleService.list_sales(current_user.id)
        return jsonify({
            "sales": [s.to_dict() for s in sales]
        }), 200