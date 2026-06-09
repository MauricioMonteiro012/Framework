from functools import wraps
from flask import request, jsonify
import jwt
from Infrastructure.Model.user import User
import os

SECRET_KEY = os.getenv("SECRET_KEY") or "sua_chave_secreta"

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization")

        if not token:
            return jsonify({"message": "Token ausente"}), 401

        try:
            token = token.split(" ")[1]
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])

            current_user = User.query.get(data["user_id"])

            if not current_user:
                return jsonify({"message": "Usuário não encontrado"}), 404

        except Exception as e:
            return jsonify({"message": "Token inválido"}), 401

        return f(current_user, *args, **kwargs)

    return decorated