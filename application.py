from flask import Flask, jsonify, redirect
from flask_restful import Api, MethodNotAllowed, NotFound
from flask_cors import CORS
from util.common import domain, port, prefix, build_swagger_config_json
from resources.swaggerConfig import SwaggerConfig
from resources.userResource import UsersGETResource, UserGETResource, UserPOSTResource, UserPUTResource, UserDELETEResource
from resources.eventResource import EventsGETResource, EventGETResource, EventPOSTResource, EventPUTResource, EventDELETEResource
from resources.loginResource import  LoginPOSTResource
from flask_swagger_ui import get_swaggerui_blueprint

# ============================================x
# Main
# ============================================
application = Flask(__name__)
app = application
app.config['PROPAGATE_EXCEPTIONS'] = True
CORS(app)
api = Api(app, prefix=prefix, catch_all_404s=True)

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
api.add_resource(UserGETResource, '/users/<int:id>')
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

# POST login
api.add_resource(LoginPOSTResource, '/login')

if __name__ == '__main__':
    app.run(debug=True)
