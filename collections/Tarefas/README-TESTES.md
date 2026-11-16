# Testes da API no Bruno

## Preparação

No Codespaces:

```bash
source .venv/bin/activate
python app.py
```

No Bruno, seleciona o ambiente `Codespaces` e configura:

```text
baseUrl = https://ENDERECO-REAL-DA-PORTA-5000.github.dev
```

Não uses `https://api.example.com`.

## Sequência completa

### Teste 1 — Registo

Executa `Registo`.

```json
{
  "username": "Joana",
  "email": "joana@empresa.pt",
  "password": "pass123"
}
```

Esperado: **201 Created**.

### Teste 2 — Login

Executa `Login` com:

```json
{
  "email": "joana@empresa.pt",
  "password": "pass123"
}
```

Esperado: **200 OK** e um `access_token`.

Copia o token e coloca-o em `Auth > Bearer Token` nos pedidos protegidos.

### Teste 3 — Criar tarefa

Executa `Criar tarefa`.

Esperado: **201 Created**. Guarda o `id` da tarefa. Os pedidos seguintes usam o ID `1`; se o ID for diferente, altera o URL.

### Teste 4 — Listar tarefas

Executa `Listar tarefas`.

Esperado: **200 OK** e apenas as tarefas da Joana.

### Teste 5 — Consultar uma tarefa

Executa `Consultar tarefa`.

Esperado: **200 OK**.

### Teste 6 — Alterar uma tarefa

Executa `Alterar tarefa`.

Esperado: **200 OK** e o estado `Em curso`.

### Teste 7 — Eliminar uma tarefa

Executa `Eliminar tarefa`.

Esperado: **200 OK**.

### Teste 8 — Sem autenticação

Executa `Teste sem token - deve dar 401`.

Esperado: **401 Unauthorized**.

### Teste 9 — Permissões

1. Regista outro utilizador, por exemplo `carlos@empresa.pt`.
2. Faz login com esse utilizador.
3. Tenta consultar a tarefa criada pela Joana.
4. Usa o token do Carlos no pedido `Teste permissões - deve dar 403`.

Esperado: **403 Forbidden**.

### Teste 10 — Administrador

Faz login com:

```json
{
  "email": "admin@empresa.pt",
  "password": "admin123"
}
```

Usa o token do administrador nos pedidos protegidos.

Esperado: o administrador consegue consultar, alterar e eliminar tarefas de todos os utilizadores.

### Teste 11 — Logout

Executa `Logout` com o token atual.

Esperado: **200 OK**. Se tentares usar novamente esse token, deverá deixar de ser aceite.
