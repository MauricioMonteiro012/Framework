from flask import request, jsonify, make_response
from src.Application.Service.user_service import UserService
from src.Application.Service.auth_service import AuthService


class UserController:

    @staticmethod
    def register_user():
        data = request.get_json()

        name = data.get('name')
        cnpj = data.get('cnpj')
        email = data.get('email')
        phone = data.get('phone')
        password = data.get('password')

        if not name or not cnpj or not email or not phone or not password:
            return make_response(jsonify({"erro": "Missing required fields"}), 400)

        user = UserService.create_user(name, cnpj, email, phone, password)

        return make_response(jsonify({
            "mensagem": "Seller cadastrado com sucesso",
            "usuario": user.to_dict()
        }), 200)

    @staticmethod
    def update_user(user_id):
        data = request.get_json()

        try:
            user = UserService.update_user(user_id, data)

            return jsonify({
                "mensagem": "Usuário atualizado com sucesso",
                "usuario": user.to_dict()
            }), 200

        except Exception as e:
            return jsonify({"erro": str(e)}), 400

    @staticmethod
    def get_me(current_user):
        return jsonify({
            "usuario": current_user.to_dict()
        }), 200