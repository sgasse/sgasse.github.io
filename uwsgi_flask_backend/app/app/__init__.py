from flask import Flask
# Create flask app
app = Flask(__name__)


# Import and register blueprint
from app.mod_landing.views import mod_landing as landing_module
app.register_blueprint(landing_module)
