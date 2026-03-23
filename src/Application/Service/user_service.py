from werkzeug.security import generate_password_hash, check_password_hash
from src.Infrastructure.Security.jwt_handler import JWTHandler # Ajuste o caminho se necessário
from src.Infrastructure.Model.user import User
from src.config.data_base import db
import random
import string

class UserService:
    @staticmethod
    def create_user(name, cnpj, email, celular, senha): # Recebendo 'senha'
        # 1. Criptografa a senha antes de salvar no banco
        hashed_password = generate_password_hash(senha)
       
        activation_code = ''.join(random.choices(string.digits, k=4))
       
        # 2. Salva a senha criptografada (hashed_password)
        user = User(
            name=name, cnpj=cnpj, email=email, celular=celular,
            password=hashed_password, status='Inativo', activation_code=activation_code
        )        
        db.session.add(user)
        db.session.commit()
       
        # (Aqui continua a lógica de enviar o WhatsApp que já está pronta)
        return user

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