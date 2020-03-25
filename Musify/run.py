from flask import Flask

def create_app(config_filename):
    app = Flask(__name__)
    app.config.from_object(config_filename)
    
    from app import api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    from Model import database
    database.init_app(app)

    return app


if __name__ == "__main__":
    app = create_app("config")
    app.run(host='0.0.0.0', debug=True)
