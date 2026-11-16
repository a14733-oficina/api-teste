import os
from datetime import timedelta

from flask import Flask
from flask_jwt_extended import JWTManager
from flask_jwt_extended.exceptions import NoAuthorizationError
from flask_restful import Api

from blocklist import BLOCKLIST
from con_sql_alchemy import bd
from resources.task import Tarefa, Tarefas
from resources.user import UserLogin, UserLogout, UserRegister, criar_admin_inicial


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tarefas.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = "chave-secreta-api-tarefas-alterar-em-producao"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=30)

bd.init_app(app)
api = Api(app)
jwt = JWTManager(app)


@jwt.token_in_blocklist_loader
def verifica_blocklist(jwt_header, jwt_payload):
    return jwt_payload["jti"] in BLOCKLIST


@jwt.revoked_token_loader
def token_invalido(jwt_header, jwt_payload):
    return {"mensagem": "Token revogado. Faça login novamente"}, 401


@jwt.unauthorized_loader
def sem_autenticacao(mensagem):
    return {"mensagem": "É necessário um token JWT válido"}, 401


@jwt.invalid_token_loader
def token_invalido_formato(mensagem):
    return {"mensagem": "Token JWT inválido"}, 401


@app.errorhandler(NoAuthorizationError)
def erro_sem_token(erro):
    return {"mensagem": "É necessário um token JWT válido"}, 401


api.add_resource(UserRegister, "/registo")
api.add_resource(UserLogin, "/login")
api.add_resource(UserLogout, "/logout")
api.add_resource(Tarefas, "/tarefas")
api.add_resource(Tarefa, "/tarefas/<int:task_id>")


with app.app_context():
    bd.create_all()
    criar_admin_inicial()


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        debug=True,
    )
