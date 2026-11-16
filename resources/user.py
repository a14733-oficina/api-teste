from hmac import compare_digest

from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token, get_jwt

from blocklist import BLOCKLIST
from con_sql_alchemy import bd
from models.user import UserModel
from resources.auth import jwt_obrigatorio


class UserRegister(Resource):
    argumentos = reqparse.RequestParser()
    argumentos.add_argument("username", type=str, required=True, help="O username é obrigatório")
    argumentos.add_argument("email", type=str, required=True, help="O email é obrigatório")
    argumentos.add_argument("password", type=str, required=True, help="A password é obrigatória")

    def post(self):
        dados = self.argumentos.parse_args()
        email = dados["email"].strip().lower()
        if UserModel.find_by_email(email):
            return {"mensagem": "Já existe um utilizador com este email"}, 400
        if len(dados["password"]) < 4:
            return {"mensagem": "A password deve ter pelo menos 4 caracteres"}, 400
        novo_utilizador = UserModel(dados["username"], email, dados["password"])
        try:
            novo_utilizador.save_user()
            return {"mensagem": "Utilizador criado com sucesso", "utilizador": novo_utilizador.json()}, 201
        except Exception:
            bd.session.rollback()
            return {"mensagem": "Erro ao criar o utilizador"}, 400


class UserLogin(Resource):
    argumentos = reqparse.RequestParser()
    argumentos.add_argument("email", type=str, required=True, help="O email é obrigatório")
    argumentos.add_argument("password", type=str, required=True, help="A password é obrigatória")

    def post(self):
        dados = self.argumentos.parse_args()
        user = UserModel.find_by_email(dados["email"])
        if user and user.verificar_password(dados["password"]):
            token = create_access_token(
                identity=str(user.id),
                additional_claims={"tipo": user.tipo, "email": user.email},
            )
            return {"access_token": token, "utilizador": user.json()}, 200
        return {"mensagem": "Email ou password incorretos"}, 401


class UserLogout(Resource):
    @jwt_obrigatorio()
    def post(self):
        BLOCKLIST.add(get_jwt()["jti"])
        return {"mensagem": "Logout efetuado com sucesso"}, 200


def criar_admin_inicial():
    """Cria um administrador apenas se ainda não existir nenhum."""
    if not UserModel.query.filter_by(tipo="admin").first():
        admin = UserModel("Administrador", "admin@empresa.pt", "admin123", "admin")
        bd.session.add(admin)
        bd.session.commit()
