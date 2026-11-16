# API de Gestão de Tarefas

Projeto desenvolvido a partir da estrutura do exemplo `apihotel`, adaptado ao enunciado **API / Gestão de Tarefas**.

## Tecnologias

- Python 3
- Flask e Flask-RESTful
- Flask-SQLAlchemy com SQLite
- Flask-JWT-Extended
- Ambiente virtual Python (`venv`)

## Executar no GitHub Codespaces

Abra o terminal do Codespace e execute os comandos seguintes a partir da pasta do projeto:

```bash
# 1. Criar o ambiente virtual (apenas na primeira utilização)
python3 -m venv .venv

# 2. Ativar o ambiente virtual
source .venv/bin/activate

# 3. Confirmar que o terminal está a usar o venv
which python
python --version

# 4. Atualizar o instalador e instalar as dependências dentro do venv
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

# 5. Iniciar a API
python app.py
```

Quando o servidor arrancar, o Codespaces deverá detetar a porta `5000`. No separador **PORTS**, seleciona a porta 5000 e escolhe **Open in Browser** ou copia o URL encaminhado pelo Codespace.

A aplicação está configurada para escutar em `0.0.0.0:5000`, condição necessária para aceder à API através do Codespaces. Também é possível definir outra porta através da variável `PORT`:

```bash
PORT=5001 python app.py
```

### Utilizações seguintes

Sempre que reabrir o Codespace, ativa primeiro o ambiente virtual:

```bash
source .venv/bin/activate
python app.py
```

Se o `.venv` ainda não existir, executa novamente:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

> Não é necessário adicionar a pasta `.venv` ao Git. Ela já está incluída no `.gitignore`. Cada Codespace pode recriar o ambiente virtual a partir do `requirements.txt`.

A base de dados `instance/tarefas.db` e as tabelas são criadas automaticamente na primeira execução. A base de dados local também está excluída do Git através do `.gitignore`.

## Administrador inicial

- Email: `admin@empresa.pt`
- Password: `admin123`

Altera estas credenciais antes de utilizar a aplicação num ambiente real.

## Endpoints

| Método | Endpoint | Autenticação | Descrição |
|---|---|---|---|
| POST | `/registo` | Não | Regista um utilizador comum |
| POST | `/login` | Não | Devolve o token JWT |
| POST | `/logout` | JWT | Revoga o token atual |
| GET | `/tarefas` | JWT | Admin vê todas; utilizador vê as suas |
| POST | `/tarefas` | JWT | Cria uma tarefa associada ao utilizador autenticado |
| GET | `/tarefas/<id>` | JWT | Consulta uma tarefa com controlo de acesso |
| PUT | `/tarefas/<id>` | JWT | Altera uma tarefa com controlo de acesso |
| DELETE | `/tarefas/<id>` | JWT | Elimina uma tarefa com controlo de acesso |

Para endpoints protegidos, enviar o cabeçalho:

```text
Authorization: Bearer <TOKEN>
```

Os estados permitidos são exatamente: `Pendente`, `Em curso` e `Concluída`.

## Exemplos JSON

Registo:

```json
{
  "username": "Joana",
  "email": "joana@empresa.pt",
  "password": "pass123"
}
```

Login:

```json
{
  "email": "joana@empresa.pt",
  "password": "pass123"
}
```

Criar tarefa:

```json
{
  "titulo": "Preparar relatório",
  "descricao": "Concluir o relatório mensal.",
  "estado": "Pendente"
}
```

## Comandos úteis no Codespaces

Ver dependências instaladas no ambiente virtual:

```bash
python -m pip list
```

Parar a API:

```text
Ctrl + C
```
