from flask import Flask, render_template

def create_app():
    app = Flask(__name__, 
                template_folder='../../templates',
                static_folder='../../frontend/build/static')
    
    # Import and register blueprints
    from . import routes
    app.register_blueprint(routes.main)
    
    return app
