from flask import Flask
from src.config.data_base import init_db
from src.routes import init_routes
from src.config.data_base import db


def create_app():
    """
    Função que cria e configura a aplicação Flask.
    """
    app = Flask(__name__)

    init_db(app)

    with app.app_context():
        db.create_all()

    init_routes(app)

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
