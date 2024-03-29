import imp
from flask import Flask
from flask_restx import Api
from .orders.views import order_namespace
from .customers.views import customer_namespace
from .config.config import config_dict
from .utils import db
from .models.orders import Order
from .models.customers import Customer
from flask_migrate import Migrate
from werkzeug.exceptions import NotFound, MethodNotAllowed, InternalServerError

def create_app(config=config_dict['dev']):
    app=Flask(__name__)

    app.config.from_object(config)

    db.init_app(app)

    migrate = Migrate(app, db)

    api=Api(app=app, version='1.0', prefix='/api/v1', title="Kinexcs Technical Assessment", description="APIs for Kinexcs Technical Assessment - Tran Que An")
    
    api.add_namespace(order_namespace, path='/orders')
    api.add_namespace(customer_namespace, path='/customers')

    @api.errorhandler(NotFound)
    def not_found(error):
        return {"error": "Not found"}, 404

    @api.errorhandler(MethodNotAllowed)
    def method_not_allowed(error):
        return {"error": "Method not allowed"}, 405

    @api.errorhandler(InternalServerError)
    def internal_server_error(error):
        return {"error": "Internal Server Error"}, 500

    @app.shell_context_processor
    def make_shell_context():
        return {
            'db': db,
            'Customer': Customer,
            'Order': Order
        }

    return app