from flask import request, jsonify
from Application.Service.product_service import ProductService

class ProductController:

    @staticmethod
    def create_product(current_user):
        file = request.files.get("image")
        data = request.form
        try:
            product = ProductService.create_product(current_user.id, data, file)
            return jsonify({"message": "Produto criado com sucesso", "product": product.to_dict()}), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 400

    @staticmethod
    def list_products(current_user):
        products = ProductService.list_products(current_user.id)
        return jsonify({"products": [p.to_dict() for p in products]}), 200

    @staticmethod
    def get_product(current_user, product_id):
        try:
            product = ProductService.get_product(current_user.id, product_id)
            return jsonify({"product": product.to_dict()}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 404

    @staticmethod
    def update_product(current_user, product_id):
        file = request.files.get("image")
        data = request.form
        try:
            product = ProductService.update_product(current_user.id, product_id, data, file)
            return jsonify({"message": "Produto atualizado com sucesso", "product": product.to_dict()}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 400

    @staticmethod
    def inactivate_product(current_user, product_id):
        try:
            product = ProductService.inactivate_product(current_user.id, product_id)
            return jsonify({"message": "Produto inativado com sucesso", "product": product.to_dict()}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 400