from flask import Flask,send_from_directory
from Router.CodeApi import code_api
from Router.CodeLIstApi import codelist_api
from flask_swagger_ui import get_swaggerui_blueprint

app=Flask(__name__)

app.register_blueprint(code_api)
app.register_blueprint(codelist_api)


@app.route('/Router/<path:path>')
def send_api(path) :
    return send_from_directory('Router',path)

SWAGGER_URL = '/spec'
API_URL = '/Router/swagger.json'
swaggerui_api = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name' : "CodeApi"
    }
)
app.register_blueprint(swaggerui_api,url_prefix=SWAGGER_URL)

if __name__ =='__main__' :
    app.run()