from flask import Flask, redirect, url_for,Blueprint
from app.extensions import csrf

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    
    @app.route("/")
    def index():
        return redirect(url_for('main_bp.home'))

    csrf.init_app(app)
    
    from app.routes.main import main_bp
    
    app.register_blueprint(main_bp)
    
    return app