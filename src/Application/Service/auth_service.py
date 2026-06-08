from werkzeug.security import check_password_hash
import jwt
import datetime
import os
from Infrastructure.Model.user import User
from config.data_base import db

SECRET_KEY = os.getenv("SECRET_KEY", "fallback_inseguro")

class AuthService:

    @staticmethod
    def login(data):
        email = data.get("email")
        password = data.get("password")
    
        user = User.query.filter_by(email=email).first()

        if not user:
            raise Exception("Usuário não encontrado")

        if not check_password_hash(user.password, password):
            raise Exception("Senha inválida")

        if not user.status:
            raise Exception("Conta não ativada. Verifique seu WhatsApp.")

        payload = {
            "user_id": user.id,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=2)
        }

        token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

        return {
            "message": "Login realizado com sucesso",
            "token": token,
            "user": user.to_dict()
        }

    @staticmethod
    def verify_user(data):
        email = data.get("email")
        code = data.get("code")

        user = User.query.filter_by(email=email).first()

        if not user:
            raise Exception("Usuário não encontrado")

        if user.verification_code != code:
            raise Exception("Código inválido")

        user.status = True
        user.verification_code = None
        db.session.commit()

        return {"message": "Conta ativada com sucesso"}