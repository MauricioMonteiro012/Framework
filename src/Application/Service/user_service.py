import random
from werkzeug.security import generate_password_hash
from Infrastructure.Model.user import User
from config.data_base import db
from Infrastructure.http.whats_app import WhatsApp


class UserService:

    @staticmethod
    def create_user(name, cnpj, email, phone, password):

        code = str(random.randint(1000, 9999))

        hashed_password = generate_password_hash(password)

        user = User(
            name=name,
            cnpj=cnpj,
            email=email,
            phone=phone,
            password=hashed_password,
            status=False,
            verification_code=code
        )

        db.session.add(user)
        db.session.commit()

        WhatsApp.whats_app(code)

        return user

    @staticmethod
    def update_user(user_id, data):
        user = User.query.get(user_id)

        if not user:
            raise Exception("Usuário não encontrado")

        user.name = data.get("name", user.name)
        user.cnpj = data.get("cnpj", user.cnpj)
        user.email = data.get("email", user.email)
        user.phone = data.get("phone", user.phone)

        if data.get("password"):
            user.password = generate_password_hash(data.get("password"))

        db.session.commit()

        return user