import os
from flask import Flask
from extensions import db, login_manager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'test'

# Configuración de BD mínima para el test
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
login_manager.init_app(app)

# Importar blueprints
from controllers.auth_controller import auth
from controllers.book_controller import book
from controllers.purchase_controller import purchase
from controllers.payment_controller import payment
from controllers.delivery_controller import delivery
from controllers.admin_controller import admin

# Registrar blueprints
app.register_blueprint(auth)
app.register_blueprint(book, url_prefix='/book')
app.register_blueprint(purchase)
app.register_blueprint(payment)
app.register_blueprint(delivery)
app.register_blueprint(admin)

print("Blueprints registrados:")
for bp in app.blueprints:
    print(f" - {bp}")

print("\nRutas disponibles:")
for rule in app.url_map.iter_rules():
    print(f" - {rule}")

print(f"\nTotal de rutas: {len(list(app.url_map.iter_rules()))}")
