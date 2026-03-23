import jwt
import datetime
import os
from functools import wraps
from flask import request, jsonify

# A chave secreta virá do ficheiro .env
JWT_SECRET = os.getenv('JWT_SECRET_KEY', 'chave_secreta_padrao')

class JWTHandler:
    @staticmethod
    def generate_token(user_id):
        payload = {
            'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=1), # Expira em 24h
            'iat': datetime.datetime.now(datetime.timezone.utc),
            'sub': user_id
        }
        return jwt.encode(payload, JWT_SECRET, algorithm='HS256')

# Decorator para proteger as rotas
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'error': 'Token ausente. Acesso negado!'}), 401
        try:
            token = token.replace("Bearer ", "")
            data = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
            current_user_id = data['sub']
        except Exception as e:
            # Tratamento de exceção se o token for inválido ou expirar
            return jsonify({'error': 'Token inválido ou expirado!'}), 401
        return f(current_user_id, *args, **kwargs)
    return decorated