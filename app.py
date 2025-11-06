import os
from dotenv import load_dotenv
from flask import Flask, render_template
from extensions import db, login_manager
from models.user import User

load_dotenv()
app = Flask(__name__)

# Configuración desde variables de entorno
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'secretkey-prod-2025')

# Configuración de RDS
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_USER = os.getenv('DB_USER', 'admin')
DB_PASS = os.getenv('DB_PASS', 'password')
DB_NAME = os.getenv('DB_NAME', 'bookstore')
DB_PORT = os.getenv('DB_PORT', '3306')

app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Configurar uploads en EFS
app.config['UPLOAD_FOLDER'] = '/mnt/efs/uploads'

db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Importar y registrar blueprints
from controllers.auth_controller import auth
from controllers.book_controller import book
from controllers.purchase_controller import purchase
from controllers.payment_controller import payment
from controllers.delivery_controller import delivery
from controllers.admin_controller import admin

app.register_blueprint(auth)
app.register_blueprint(book, url_prefix='/book')
app.register_blueprint(purchase)
app.register_blueprint(payment)
app.register_blueprint(delivery)
app.register_blueprint(admin)

from models.delivery import DeliveryProvider

def initialize_delivery_providers():
    with app.app_context():
        if DeliveryProvider.query.count() == 0:
            providers = [
                DeliveryProvider(name="DHL", coverage_area="Internacional", cost=50.0),
                DeliveryProvider(name="FedEx", coverage_area="Internacional", cost=45.0),
                DeliveryProvider(name="Envia", coverage_area="Nacional", cost=20.0),
                DeliveryProvider(name="Servientrega", coverage_area="Nacional", cost=15.0),
            ]
            db.session.bulk_save_objects(providers)
            db.session.commit()

@app.route('/')
def home():
    return """
    <html>
    <head><title>BookStore</title></head>
    <body>
        <h1>BookStore Application - FUNCIONANDO! 🎉</h1>
        <p>El ALB está conectado correctamente.</p>
        <ul>
            <li><a href="/book/catalog">Ver Catálogo</a></li>
            <li><a href="/login">Iniciar Sesión</a></li>
            <li><a href="/register">Registrarse</a></li>
        </ul>
        <p><a href="/health">Health Check</a></p>
    </body>
    </html>
    """, 200

# Health check para ALB
@app.route('/health')
def health():
    return {'status': 'healthy'}, 200

if __name__ == '__main__':
    with app.app_context():
        # Crear directorio de uploads en EFS
        import os
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        
        db.create_all()
        initialize_delivery_providers()
    
    app.run(host="0.0.0.0", port=5000, debug=False)
