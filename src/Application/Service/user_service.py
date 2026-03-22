import random
import string
from src.Domain.user import UserDomain
from src.Infrastructure.Model.user import User
from src.config.data_base import db
from src.Infrastructure.http.whats_app import send_activation_code

class UserService:
    @staticmethod
    def create_user(name, cnpj, email, celular, password):        
        # Gerar código de ativação de 4 dígitos
        activation_code = ''.join(random.choices(string.digits, k=4))
       
        user = User(name=name, cnpj=cnpj, email=email, celular=celular, password=password, status='Inativo', activation_code=activation_code)        
        db.session.add(user)
        db.session.commit()
       
        # Enviar código via WhatsApp
        send_activation_code(activation_code)
       
        return UserDomain(user.id, user.name, user.cnpj, user.email, user.celular, user.status)
   
    @staticmethod
    def activate_user(celular, code, email):
        user = User.query.filter_by(celular=celular, activation_code=code, email=email).first()
        if user and user.status == 'Inativo':
            user.status = 'Ativo'
            user.activation_code = None  # Limpar código após ativação
            db.session.commit()
            return True
        return False
