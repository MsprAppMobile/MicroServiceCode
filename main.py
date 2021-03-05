from flask import Flask
from Api.CodeApi import code_api
from Api.CodeLIstApi import codelist_api

app=Flask(__name__)

app.register_blueprint(code_api)
app.register_blueprint(codelist_api)

if __name__ =='__main__' :
    app.run()