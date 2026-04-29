from flask import request, jsonify
from src.Application.Service.sale_service import SaleService
from src.Infrastructure.Security.jwt_handler import JWTHandler, token_required

class SaleController:
    @staticmethod
    @token_required
    def create_sale(current_user_id):
        try:
            data = request.get_json()

            product_id = data.get('product_id')
            quantity = data.get('quantity')

            if not product_id or not quantity:
                return jsonify({"error": "ID do produto e quantidade são obrigatórios"}), 400

            try:
                quantity = int(quantity)
                if quantity <= 0:
                    raise ValueError
            except ValueError:
                return jsonify({"error": "Quantidade deve ser um número inteiro positivo"}), 400

            # Chama o service
            result = SaleService.create_sale(product_id, quantity, current_user_id)

            return jsonify({"message": "Venda realizada com sucesso!", "venda": result}), 200

        except ValueError as ve:
            return jsonify({"error": str(ve)}), 400

        except PermissionError as pe:
            return jsonify({"error": str(pe)}), 403

        except Exception as e:
            print(f"Erro na venda: {e}")
            return jsonify({"error": "Erro interno no servidor"}), 500