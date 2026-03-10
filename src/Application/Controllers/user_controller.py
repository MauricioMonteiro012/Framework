from flask import request, jsonify, make_response
from src.Application.Service.user_service import UserService

class UserController:
    @staticmethod
    def register_user():
        data = request.get_json()
        name = data.get('name')
        cnpj = data.get('cnpj')
        email = data.get('email')
        celular = data.get('celular')
        password = data.get('password')

        if not all([name, cnpj, email, celular, password]):
            return make_response(jsonify({"erro": "Campos obrigatórios ausentes"}), 400)

        user = UserService.create_user(name, cnpj, email, celular, password)
        return make_response(jsonify({
            "mensagem": "Vendedor cadastrado com sucesso. Código enviado via WhatsApp.",
            "vendedor": user.to_dict()
        }), 201)
   
    @staticmethod
    def activate_user():
        data = request.get_json()
        celular = data.get('celular')
        codigo = data.get('codigo')

        if not celular or not codigo:
            return make_response(jsonify({"erro": "Celular e código obrigatórios"}), 400)

        if UserService.activate_user(celular, codigo):
            return make_response(jsonify({"mensagem": "Vendedor ativado com sucesso"}), 200)
        else:
            return make_response(jsonify({"erro": "Código inválido ou vendedor já ativo"}), 400)