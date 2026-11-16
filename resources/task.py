from flask_restful import Resource, reqparse
from flask_jwt_extended import get_jwt, get_jwt_identity

from con_sql_alchemy import bd
from models.task import ESTADOS_VALIDOS, TaskModel
from resources.auth import jwt_obrigatorio


def dados_tarefa(parser):
    parser.add_argument("titulo", type=str, required=True, help="O título é obrigatório")
    parser.add_argument("descricao", type=str, required=False, default="")
    parser.add_argument("estado", type=str, required=False, default="Pendente")
    return parser


class Tarefas(Resource):
    argumentos = dados_tarefa(reqparse.RequestParser())

    @jwt_obrigatorio()
    def get(self):
        if get_jwt().get("tipo") == "admin":
            tarefas = TaskModel.query.order_by(TaskModel.id).all()
        else:
            tarefas = TaskModel.query.filter_by(
                utilizador_id=int(get_jwt_identity())
            ).order_by(TaskModel.id).all()
        return {"tarefas": [tarefa.json() for tarefa in tarefas]}, 200

    @jwt_obrigatorio()
    def post(self):
        dados = self.argumentos.parse_args()
        if dados["estado"] not in ESTADOS_VALIDOS:
            return {"mensagem": "Estado inválido. Use: Pendente, Em curso ou Concluída"}, 400
        tarefa = TaskModel(
            dados["titulo"], dados["descricao"], dados["estado"], int(get_jwt_identity())
        )
        try:
            tarefa.save_task()
            return tarefa.json(), 201
        except Exception:
            bd.session.rollback()
            return {"mensagem": "Erro ao criar a tarefa"}, 400


class Tarefa(Resource):
    argumentos = dados_tarefa(reqparse.RequestParser())

    @jwt_obrigatorio()
    def get(self, task_id):
        tarefa = TaskModel.find_task(task_id)
        if tarefa is None:
            return {"mensagem": "Tarefa não encontrada"}, 404
        if not self._tem_acesso(tarefa):
            return {"mensagem": "Não tem permissões para consultar esta tarefa"}, 403
        return tarefa.json(), 200

    @jwt_obrigatorio()
    def put(self, task_id):
        tarefa = TaskModel.find_task(task_id)
        if tarefa is None:
            return {"mensagem": "Tarefa não encontrada"}, 404
        if not self._tem_acesso(tarefa):
            return {"mensagem": "Não tem permissões para alterar esta tarefa"}, 403
        dados = self.argumentos.parse_args()
        if dados["estado"] not in ESTADOS_VALIDOS:
            return {"mensagem": "Estado inválido. Use: Pendente, Em curso ou Concluída"}, 400
        tarefa.titulo = dados["titulo"]
        tarefa.descricao = dados["descricao"]
        tarefa.estado = dados["estado"]
        bd.session.commit()
        return tarefa.json(), 200

    @jwt_obrigatorio()
    def delete(self, task_id):
        tarefa = TaskModel.find_task(task_id)
        if tarefa is None:
            return {"mensagem": "Tarefa não encontrada"}, 404
        if not self._tem_acesso(tarefa):
            return {"mensagem": "Não tem permissões para eliminar esta tarefa"}, 403
        tarefa.delete_task()
        return {"mensagem": "Tarefa eliminada com sucesso"}, 200

    @staticmethod
    def _tem_acesso(tarefa):
        return get_jwt().get("tipo") == "admin" or tarefa.utilizador_id == int(get_jwt_identity())
