from flask import request, jsonify
from src.Application.Service.user_service import UserService

class UserController:
    # ... (outros métodos que já existem, como create_user, etc) ...

    @staticmethod
    def login_user():
        try:
            data = request.get_json()
           
            # Pegando os campos exatos do curl do professor
            email = data.get('email')
            senha = data.get('senha')
           
            if not email or not senha:
                 return jsonify({"error": "E-mail e senha são obrigatórios"}), 400

        if UserService.activate_user(celular, codigo, email):
            return make_response(jsonify({"mensagem": "Vendedor ativado com sucesso"}), 200)
        else:
            return make_response(jsonify({"erro": "Código inválido ou vendedor já ativo"}), 400)
        
    @staticmethod
    def login_user():
        try:
            data = request.get_json()
           
            # Pegando os campos exatos do curl do professor
            email = data.get('email')
            senha = data.get('senha')
           
            if not email or not senha:
                 return jsonify({"error": "E-mail e senha são obrigatórios"}), 400

            # O Controller chama a regra de negócio do Service
            token = UserService.login(email, senha)
           
            return jsonify({"message": "Login efetuado com sucesso!", "token": token}), 200
           
        except ValueError as ve:
            # Tratamento de erro 1: Senha ou email errados (Erro 401)
            return jsonify({"error": str(ve)}), 401
           
        except PermissionError as pe:
            # Tratamento de erro 2: Usuário inativo no zap (Erro 403)
            return jsonify({"error": str(pe)}), 403
           
        except Exception as e:
            # Tratamento de erro 3: Evita que o servidor caia
            print(f"Erro no login: {e}")
            return jsonify({"error": "Erro interno no servidor."}), 500
