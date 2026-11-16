from werkzeug.security import check_password_hash, generate_password_hash
from con_sql_alchemy import bd


class UserModel(bd.Model):
    __tablename__ = "utilizadores"

    id = bd.Column(bd.Integer, primary_key=True, autoincrement=True)
    username = bd.Column(bd.String(80), nullable=False)
    email = bd.Column(bd.String(120), unique=True, nullable=False, index=True)
    password = bd.Column(bd.String(255), nullable=False)
    tipo = bd.Column(bd.String(20), nullable=False, default="utilizador")

    tarefas = bd.relationship(
        "TaskModel", back_populates="utilizador", cascade="all, delete-orphan"
    )

    def __init__(self, username, email, password, tipo="utilizador"):
        self.username = username
        self.email = email.lower().strip()
        self.password = generate_password_hash(password)
        self.tipo = tipo

    def verificar_password(self, password):
        return check_password_hash(self.password, password)

    def json(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "tipo": self.tipo,
        }

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email.lower().strip()).first()

    def save_user(self):
        bd.session.add(self)
        bd.session.commit()
