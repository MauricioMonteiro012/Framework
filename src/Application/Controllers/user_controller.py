from flask import request, jsonify, make_response
from src.Application.Service.user_service import UserService

class UserController:
    @staticmethod
    def register_user():
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')

        if not name or not email or not password:
            return make_response(jsonify({"erro": "Missing required fields"}), 400)

        user = UserService.create_user(name, email, password)
        return make_response(jsonify({
            "mensagem": "User salvo com sucesso",
            "usuarios": user.to_dict()
        }), 200)



    @staticmethod
    def activate_user():
        data = request.get_json()
        email = data.get("email")

        if not email:
            return make_response(jsonify({"erro": "Email é obrigatório"}), 400)

        user = UserService.activate_user(email)

        return make_response(jsonify({
            "mensagem": "User ativado com sucesso"
        }), 200)
