from src.Application.Controllers.user_controller import UserController 
from src.Application.Controllers.product_controller import ProductController
from flask import jsonify, make_response

def init_routes(app):    
    @app.route('/', methods=['GET'])
    def index():
        # rota base redireciona para health endpoint
        return make_response(jsonify({"mensagem": "API disponível em /api"}), 200)

    @app.route('/api', methods=['GET'])
    def health():
        return make_response(jsonify({
            "mensagem": "API - OK; Docker - Up",
        }), 200)
    
    @app.route('/api/sellers', methods=['POST'])
    def register_seller():
        # cria um novo vendedor; dados são validados no controller
        return UserController.register_user()

    @app.route('/api/sellers/activate', methods=['POST'])
    def activate_seller():
        # ativa vendedor com código recebido via WhatsApp
        return UserController.activate_user()
    
    @app.route('/api/auth/login', methods=['POST'])
    def login():
        return UserController.login_user()   

    @app.route('/api/products', methods=['POST'])
    def cad_products():
        # cadastrar produtos, apenas vendedores ativos podem cadastrar
        return ProductController.cad_products()
    
    @app.route('/api/products', methods=['GET'])
    def list_products():
        # lista todos os produtos cadastrados
        return ProductController.list_products()
      
    @app.route('/api/user/update', methods=['PUT'])
    def update_user_route():
        return UserController.update_profile()
    
    @app.route('/api/products/<int:product_id>', methods=['GET'])
    def get_product_details(product_id):
        return ProductController.get_product_details(product_id)

    @app.route('/api/products/<int:product_id>', methods=['PUT'])
    def edit_product(product_id):
        return ProductController.edit_product(product_id)

    @app.route('/api/products/<int:product_id>', methods=['DELETE'])
    def delete_product(product_id):
        return ProductController.inactivate_product(product_id)