from flask import request, jsonify, make_response
from src.Application.Service.user_service import UserService
from src.Infrastructure.Security.jwt_handler import JWTHandler, token_required

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

        user, activation_code, sent = UserService.create_user(name, cnpj, email, celular, password)
        response = {
            "mensagem": "Vendedor cadastrado com sucesso.",
            "vendedor": user.to_dict()
        }
        if not sent:
            response["mensagem"] = "Vendedor cadastrado, mas não foi possível enviar o código via WhatsApp."
            response["activation_code"] = activation_code
        return make_response(jsonify(response), 201)
   
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
    def register_user_web():
        name = request.form.get('name')
        cnpj = request.form.get('cnpj')
        email = request.form.get('email')
        celular = request.form.get('celular')
        password = request.form.get('password')

        if not all([name, cnpj, email, celular, password]):
            return {"success": False, "message": "Todos os campos são obrigatórios."}

        try:
            user, activation_code, sent = UserService.create_user(name, cnpj, email, celular, password)
            if sent:
                return {"success": True, "message": "Cadastro realizado com sucesso. Código enviado via WhatsApp."}
            return {"success": True, "message": f"Cadastro realizado, mas não foi possível enviar o código via WhatsApp. Código: {activation_code}"}
        except Exception as e:
            return {"success": False, "message": str(e)}

    @staticmethod
    def activate_user_web():
        email = request.form.get('email')
        celular = request.form.get('celular')
        codigo = request.form.get('codigo')

        if not email or not celular or not codigo:
            return {"success": False, "message": "Email, celular e código são obrigatórios."}

        if UserService.activate_user(celular, codigo, email):
            return {"success": True, "message": "Conta ativada com sucesso."}
        return {"success": False, "message": "Código inválido ou conta já ativa."}

    @staticmethod
    def login_user_web():
        identifier = request.form.get('identifier')
        password = request.form.get('password')

        if not identifier or not password:
            return {"success": False, "message": "Email/Celular e senha são obrigatórios."}
        try:
            token = UserService.login(identifier, password)
            return {"success": True, "message": "Login realizado com sucesso.", "token": token}
        except Exception as e:
            return {"success": False, "message": str(e)}
        
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
