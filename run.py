import sys
import os
from dotenv import load_dotenv  # ← adiciona
load_dotenv()                   # ← adiciona


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "src")))

from flask import Flask, send_from_directory
from flask_cors import CORS
from config.data_base import init_db
from routes import init_routes

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    init_db(app)
    init_routes(app)

    @app.route('/uploads/<filename>')
    def uploaded_file(filename):
        return send_from_directory(UPLOAD_FOLDER, filename)

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)