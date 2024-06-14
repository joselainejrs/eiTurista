from flask import Flask
from flask_migrate import Migrate
from flask_cors import CORS
from controllers.localidade import localidade_route
from controllers.depoimento import depoimento_route
from models import db

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///eiTurista.db'
db.init_app(app)
migrate = Migrate(app, db)

app.register_blueprint(localidade_route)
app.register_blueprint(depoimento_route, url_prefix='/depoimento')

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host='localhost', debug=True)
