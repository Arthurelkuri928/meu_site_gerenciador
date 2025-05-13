import os
import sys
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, redirect, url_for, render_template, request, flash
from flask_login import LoginManager, current_user, login_required
from src.models.user import db, User
from src.models.config import SiteConfiguration # Ensure SiteConfiguration is created in db
from src.routes.auth import auth_bp
from src.routes.admin import admin_bp # Import admin blueprint

app = Flask(__name__,
            static_folder='static',
            template_folder='templates')
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev_secret_key_for_prod_change_this_e9a8b7c6d5f4e3d2c1b0a9')

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth_bp.login'
login_manager.login_message = "Por favor, faça login para acessar esta página."
login_manager.login_message_category = "info"

@login_manager.user_loader
def load_user(user_id):
    if user_id is not None and user_id != 'None':
        try:
            return User.query.get(int(user_id))
        except ValueError:
            return None
    return None

# Register Blueprints
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(admin_bp, url_prefix='/admin') # Register admin blueprint

# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{os.getenv('DB_USERNAME', 'root')}:{os.getenv('DB_PASSWORD', 'password')}@{os.getenv('DB_HOST', 'localhost')}:{os.getenv('DB_PORT', '3306')}/{os.getenv('DB_NAME', 'mydb')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Create database tables if they don't exist
with app.app_context():
    db.create_all() # This will create User and SiteConfiguration tables

@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return redirect(url_for('auth_bp.login'))

@app.route('/dashboard')
@login_required
def dashboard():
    # Pass site_title to dashboard as well, if needed for layout
    site_title = admin_bp.get_config_value('site_title', default='Meu Site Padrão')
    return render_template('dashboard_placeholder.html', site_title=site_title)

# The /admin route is now handled by admin_bp.admin_panel, so the one below is removed.
# @app.route('/admin')
# @login_required
# def admin_panel():
#     if not current_user.is_admin:
#         flash("Acesso negado. Você não tem permissão para acessar esta página.", "danger")
#         return redirect(url_for('dashboard'))
#     # Logic for admin panel will go here
#     return render_template('admin_panel_placeholder.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

