from src.Domain.user import UserDomain
from src.Infrastructure.Model.user import User
from src.config.data_base import db 
from src.Infrastructure.http.whats_app import send_activation_code
import random
import string


class UserService:
    @staticmethod
    def create_user(name, cnpj, email, celular, password):        
        # gera código de ativação numérico de 4 dígitos
        activation_code = ''.join(random.choices(string.digits, k=4))
        user = User(
            name=name,
            cnpj=cnpj,
            email=email,
            celular=celular,
            password=password,
            status='Inativo',
            activation_code=activation_code,
        )        
        db.session.add(user)
        db.session.commit()
        # envia mensagem via WhatsApp
        try:
            send_activation_code(celular, activation_code)
        except Exception:
            # não voglamos falhar a criação caso o envio falhe; apenas log
            print(f"Erro ao enviar código WhatsApp para {celular}")
        return UserDomain(user.id, user.name, user.cnpj, user.email, user.celular, user.status)

    @staticmethod
    def activate_user(celular, code):
        user = User.query.filter_by(celular=celular, activation_code=code).first()
        if user and user.status == 'Inativo':
            user.status = 'Ativo'
            user.activation_code = None
            db.session.commit()
            return True
        return False
