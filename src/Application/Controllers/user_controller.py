from flask import request, jsonify, make_response
from src.Application.Service.user_service import UserService
from src.Infrastructure.Security.jwt_handler import JWTHandler

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
        email = data.get('email')
        celular = data.get('celular')
        codigo = data.get('codigo')

        if not celular or not codigo or not email:
            return make_response(jsonify({"erro": "Celular, código e email obrigatórios"}), 400)

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
        
    @staticmethod
    def update_profile():
            try:
                user_id = JWTHandler.get_user_id_from_token(request.headers.get('Authorization'))
                
                data = request.get_json()
                UserService.update_user(user_id, data)
                
                return jsonify({"message": "Dados atualizados com sucesso!"}), 200
            except Exception as e:
                return jsonify({"error": str(e)}), 400
