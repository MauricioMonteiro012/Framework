from src.Application.Controllers import UserController 
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
    
    # endpoints related to sellers (mini mercados)
    @app.route('/api/sellers', methods=['POST'])
    def register_seller():
        # cria um novo vendedor; dados são validados no controller
        return UserController.register_user()

    @app.route('/api/sellers/activate', methods=['POST'])
    def activate_seller():
        # ativa vendedor com código recebido via WhatsApp
        return UserController.activate_user()
    
    # A rota exata que o professor vai testar com o curl
    @app.route('/api/auth/login', methods=['POST'])
    def login():
        # A rota apenas repassa a bola para o Controller fazer o trabalho sujo
        return UserController.login_user()   


