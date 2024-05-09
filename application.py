from flask import Flask, jsonify, redirect
from flask_restful import Api, MethodNotAllowed, NotFound
from flask_cors import CORS
from util.common import domain, port, prefix, build_swagger_config_json
from flask_swagger_ui import get_swaggerui_blueprint
from flask_session import Session
import secrets
import ssl
from flask_jwt_extended import JWTManager
from resources.swaggerConfig import SwaggerConfig
from resources.userResource import *
from resources.eventResource import *
from resources.loginResource import  *
from resources.userEventsResource import *
from resources.connectionsResource import *

# ============================================x
# Main
# ============================================
   
app = Flask(__name__)
app.config['PROPAGATE_EXCEPTIONS'] = True
CORS(app)

secret_key = secrets.token_hex(16) 
app.config['SECRET_KEY'] = secret_key
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)
api = Api(app, prefix=prefix, catch_all_404s=True)

# ============================================
# Authentication
# ============================================

app.config['JWT_SECRET_KEY'] = secret_key
jwt = JWTManager(app)


# ============================================
# Swagger
# ============================================
build_swagger_config_json()
swaggerui_blueprint = get_swaggerui_blueprint(
    prefix,
    f'http://{domain}:{port}{prefix}/swagger-config',
    config={
        'app_name': "Flask API",
        "layout": "BaseLayout",
        "docExpansion": "none"
    },
)
app.register_blueprint(swaggerui_blueprint)

# ============================================
# Error Handler
# ============================================


@app.errorhandler(NotFound)
def handle_method_not_found(e):
    response = jsonify({"message": str(e)})
    response.status_code = 404
    return response


@app.errorhandler(MethodNotAllowed)
def handle_method_not_allowed_error(e):
    response = jsonify({"message": str(e)})
    response.status_code = 405
    return response


@app.route('/')
def redirect_to_prefix():
    if prefix != '':
        return redirect(prefix)


# ============================================
# Add Resource
# ============================================
# GET swagger config
api.add_resource(SwaggerConfig, '/swagger-config')

# GET users
api.add_resource(UsersGETResource, '/users')
api.add_resource(UserGETResource, '/users/<string:email>')
api.add_resource(UserFromEmailGetResource, '/users/email/<string:email>')
# POST users
api.add_resource(UserPOSTResource, '/users')
# PUT users
api.add_resource(UserPUTResource, '/users/<int:id>')
# DELETE users
api.add_resource(UserDELETEResource, '/users/<int:id>')

# GET events
api.add_resource(EventsGETResource, '/events')
api.add_resource(EventGETResource, '/events/<int:id>')
# POST events
api.add_resource(EventPOSTResource, '/events')
# PUT events
api.add_resource(EventPUTResource, '/events/<int:id>')
# DELETE events
api.add_resource(EventDELETEResource, '/events/<int:id>')

# GET user events
api.add_resource(UserEventsGETResource, '/users/<int:id>/events')
# POST user events
api.add_resource(UserEventsPOSTResource, '/users/<int:id>/events')
# DELETE user events
api.add_resource(UserEventsDELETEResource, '/users/<int:id>/events')

# GET connections
api.add_resource(ConnectionsGETResource, '/users/<int:id>/connections')

# POST connections
api.add_resource(ConnectionsPOSTResource, '/connections')

# PUT connections
api.add_resource(ConnectionsPUTResource, '/connections')

# DELETE connections
api.add_resource(ConnectionsDELETEResource, '/connections')

# POST login
api.add_resource(LoginPOSTResource, '/login')
api.add_resource(LogoutGETResource, '/logout')




if __name__ == '__main__':
    # context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    # context.load_cert_chain('cert.pem', 'key.pem')
    app.run(debug=True)