from flask import Flask
# Added import of flask_login module and loginmanager
from flask_login import LoginManager
from config import Config
from .site.routes import site
#from .authentication.routes import auth
from flask_migrate import Migrate
from twitter_inventory.models import db as root_db, login_manager, ma
from flask_sqlalchemy import SQLAlchemy

# Added CORS (cross origin resource sharing)
from flask_cors import CORS

app = Flask(__name__)



app.config.from_object(Config)

# Added secret_key from config.Config
app.secret_key = Config.SECRET_KEY

app.register_blueprint(api)
app.register_blueprint(site)
app.register_blueprint(auth)

root_db.init_app(app)
migrate = Migrate(app, root_db)

login_manager.init_app(app)

# Added redirect to signin for logged out users accessing routes
login_manager.login_view = 'auth.signin'

# Added initialization of marshaller and CORS
ma.init_app(app)
CORS(app)

# Added import of User instead of just models
from twitter_inventory.models import User

# Relocated loginmanager from models to ensure access to current_user
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
