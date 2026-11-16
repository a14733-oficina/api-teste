# Testar a API com Bruno

## 1. Iniciar a API no Codespaces

No terminal do Codespace:

```bash
source .venv/bin/activate
python app.py
```

A aplicação deve estar a correr na porta `5000`.

## 2. Obter o endereço

No GitHub Codespaces, abre **PORTS**, localiza a porta `5000` e copia o endereço HTTPS. Será parecido com:

```text
https://5000-abc123.github.dev
```

Não uses `https://api.example.com`, porque esse é apenas um endereço de exemplo.

## 3. Configurar a variável no Bruno

Na coleção, cria um ambiente chamado `Codespaces`. Adiciona uma variável:

```text
Nome: baseUrl
Valor: https://O-TEU-ENDERECO-DA-PORTA-5000.github.dev
```

Substitui o valor pelo endereço real copiado no passo anterior. Seleciona o ambiente `Codespaces` no Bruno.

Todos os pedidos usam automaticamente `{{baseUrl}}`, por exemplo:

```text
{{baseUrl}}/login
```

## 4. Ordem dos testes

1. Abre `Registo` e envia o pedido.
2. Abre `Login` e envia o pedido.
3. Copia o valor de `access_token` da resposta.
4. Nos pedidos protegidos, abre **Auth** e escolhe **Bearer Token**.
5. Cola o token no campo correspondente.
6. Testa `Criar tarefa` e `Listar tarefas`.

## Dados para testar

### Registo

```json
{
  "username": "Joana",
  "email": "joana@empresa.pt",
  "password": "pass123"
}
```

### Login do administrador

```json
{
  "email": "admin@empresa.pt",
  "password": "admin123"
}
```

### Criar tarefa

```json
{
  "titulo": "Preparar relatório",
  "descricao": "Concluir o relatório mensal.",
  "estado": "Pendente"
}
```

Os estados permitidos são `Pendente`, `Em curso` e `Concluída`.
