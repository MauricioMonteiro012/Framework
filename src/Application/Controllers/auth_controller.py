from flask import request, jsonify
from Application.Service.auth_service import AuthService

class AuthController:

    @staticmethod
    def login():
        data = request.get_json()
        try:
            result = AuthService.login(data)
            return jsonify(result), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 400

    @staticmethod
    def verify():
        data = request.get_json()
        try:
            result = AuthService.verify_user(data)
            return jsonify(result), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 400