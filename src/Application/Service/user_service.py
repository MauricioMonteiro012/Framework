import random
import string
from src.Infrastructure.Model.product import Produto
from src.Infrastructure.Security.jwt_handler import JWTHandler
from werkzeug.security import check_password_hash, generate_password_hash
from src.Domain.user import UserDomain
from src.Infrastructure.Model.user import User
from src.config.data_base import db
from src.Infrastructure.http.whats_app import send_activation_code

class UserService:
    @staticmethod
    def create_user(name, cnpj, email, celular, password):
        
        hashed_password = generate_password_hash(password)
                
        # Gerar código de ativação de 4 dígitos
        activation_code = ''.join(random.choices(string.digits, k=4))
       
        user = User(name=name, cnpj=cnpj, email=email, celular=celular, password=hashed_password, status='Inativo', activation_code=activation_code)        
        db.session.add(user)
        db.session.commit()
        
        # Enviar código via WhatsApp (Sua parte da Main)
        send_activation_code(activation_code)
        
        return UserDomain(user.id, user.name, user.cnpj, user.email, user.celular, user.status)

    @staticmethod
    def activate_user(celular, code, email):
        # (Sua parte da Main)
        user = User.query.filter_by(celular=celular, activation_code=code, email=email).first()
        if user and user.status == 'Inativo':
            user.status = 'Ativo'
            user.activation_code = None  # Limpar código após ativação
            db.session.commit()
            return True
        return False
    
    @staticmethod
    def login(email, senha):
        user = User.query.filter_by(email=email).first()
       
        # 1. Verifica se o e-mail existe e se a senha desencriptada bate com a digitada
        if not user or not check_password_hash(user.password, senha):
            raise ValueError("E-mail ou senha incorretos.")
           
        # 2. Impede login se não ativou o zap
        if user.status == 'Inativo':
            raise PermissionError("Conta pendente de ativação via WhatsApp.")
           
        # 3. Gera e retorna o Token JWT
        token = JWTHandler.generate_token(user.id)
        return token
