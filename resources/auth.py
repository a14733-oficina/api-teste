from functools import wraps

from flask_jwt_extended import verify_jwt_in_request
from flask_jwt_extended.exceptions import NoAuthorizationError


def jwt_obrigatorio():
    def decorator(funcao):
        @wraps(funcao)
        def wrapper(*args, **kwargs):
            try:
                verify_jwt_in_request()
            except NoAuthorizationError:
                return {"mensagem": "É necessário um token JWT válido"}, 401
            return funcao(*args, **kwargs)

        return wrapper

    return decorator
