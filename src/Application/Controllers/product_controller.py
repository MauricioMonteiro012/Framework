from flask import request, jsonify
from src.Application.Service.user_service import UserService
from src.Application.Service.product_service import ProductService
from src.Infrastructure.Security.jwt_handler import token_required

class ProductController:
    @staticmethod
    @token_required
    def cad_products(current_user_id):
        try:
            data = request.get_json()
           
            # Pegando os campos exatos do curl 
            nome = data.get('nome')
            preco = data.get('preco')
            qtd = data.get('qtd')
            img = data.get('img')
            user_id = current_user_id  # ID do usuário autenticado, passado pelo token_required
           
            if not nome or not preco or not qtd:
                 return jsonify({"error": "Nome, preço e quantidade são obrigatórios"}), 400

            # O Controller chama a regra de negócio do Service
            result = ProductService.cad_products(nome, preco, qtd, img, user_id)
           
            return jsonify({"message": "Produto cadastrado com sucesso!", "produto": result}), 200
           
        except ValueError as ve:
            # Tratamento de erro 1: Dados inválidos (Erro 400)
            return jsonify({"error": str(ve)}), 400
           
        except PermissionError as pe:
            # Tratamento de erro 2: Vendedor inativo (Erro 403)
            return jsonify({"error": str(pe)}), 403
           
        except Exception as e:
            # Tratamento de erro 3: Evita que o servidor caia
            print(f"Erro no cadastro de produto: {e}")
            return jsonify({"error": f"Erro interno no servidor {e}"}), 500
        
    @staticmethod
    @token_required
    def list_products(current_user_id):
        try:
            user_id = current_user_id 
            products = ProductService.list_products(user_id)
           
            return jsonify({"produtos": products}), 200
           
        except Exception as e:
            # Tratamento de erro: Evita que o servidor caia
            print(f"Erro ao listar produtos: {e}")
            return jsonify({"error": f"Erro interno no servidor {e}"}), 500