from con_sql_alchemy import bd


ESTADOS_VALIDOS = {"Pendente", "Em curso", "Concluída"}


class TaskModel(bd.Model):
    __tablename__ = "tarefas"

    id = bd.Column(bd.Integer, primary_key=True, autoincrement=True)
    titulo = bd.Column(bd.String(150), nullable=False)
    descricao = bd.Column(bd.Text, nullable=False, default="")
    estado = bd.Column(bd.String(20), nullable=False, default="Pendente")
    utilizador_id = bd.Column(
        bd.Integer, bd.ForeignKey("utilizadores.id"), nullable=False
    )

    utilizador = bd.relationship("UserModel", back_populates="tarefas")

    def __init__(self, titulo, descricao, estado, utilizador_id):
        self.titulo = titulo
        self.descricao = descricao
        self.estado = estado
        self.utilizador_id = utilizador_id

    def json(self):
        return {
            "id": self.id,
            "titulo": self.titulo,
            "descricao": self.descricao,
            "estado": self.estado,
            "utilizador_id": self.utilizador_id,
            "utilizador": self.utilizador.username if self.utilizador else None,
        }

    @classmethod
    def find_task(cls, task_id):
        return cls.query.get(task_id)

    def save_task(self):
        bd.session.add(self)
        bd.session.commit()

    def delete_task(self):
        bd.session.delete(self)
        bd.session.commit()
