# Construindo uma REST API de TODO com Python e FastAPI

> Projeto de estudo. O objetivo não é só fazer funcionar — é entender **por que** cada peça existe.

---

## O que vamos construir

Uma API REST completa com CRUD de tarefas (TODOs):

| Método HTTP | Rota          | O que faz                  |
|-------------|---------------|----------------------------|
| `GET`       | `/todos`      | Lista todas as tarefas     |
| `GET`       | `/todos/{id}` | Busca uma tarefa pelo id   |
| `POST`      | `/todos`      | Cria uma nova tarefa       |
| `PUT`       | `/todos/{id}` | Atualiza uma tarefa        |
| `DELETE`    | `/todos/{id}` | Remove uma tarefa          |

---

## Conceitos fundamentais antes de começar

### O que é uma API REST?

**API** (Application Programming Interface) é um contrato: você define como outros sistemas podem interagir com o seu. No caso de uma **REST API**, esse contrato usa o protocolo **HTTP** — o mesmo que o browser usa para acessar sites.

A diferença é que em vez de retornar HTML (páginas visuais), a API retorna **dados estruturados**, geralmente em formato **JSON**.

**Por que REST?** Porque HTTP é universal. Qualquer linguagem, qualquer plataforma consegue fazer uma requisição HTTP. Sua API em Python pode ser consumida por um app em React, um mobile em Swift, outro servidor em Go — sem nenhuma configuração especial.

### O que é CRUD?

CRUD é um acrônimo para as 4 operações fundamentais que qualquer sistema de dados precisa ter:

| Letra | Operação | HTTP Equivalente |
|-------|----------|-----------------|
| **C** | Create (criar) | `POST` |
| **R** | Read (ler) | `GET` |
| **U** | Update (atualizar) | `PUT` |
| **D** | Delete (deletar) | `DELETE` |

### O que é um status HTTP?

Toda resposta HTTP vem com um **código de status** que indica o resultado:

| Código | Significado                     |
|--------|---------------------------------|
| `200`  | OK — sucesso                    |
| `201`  | Created — recurso criado        |
| `404`  | Not Found — não encontrado      |
| `422`  | Unprocessable Entity — dados inválidos |
| `500`  | Internal Server Error — erro no servidor |

**Por que isso importa?** Porque o cliente da API (browser, app, outro servidor) usa o código de status para saber o que fazer. Se receber `404`, sabe que o item não existe. Se receber `201`, sabe que a criação foi bem-sucedida.

---

## Estrutura do projeto

```
python-api/
├── pyproject.toml              # dependências e configurações do projeto
└── src/
    └── python_api/
        ├── __init__.py         # marca o diretório como um pacote Python
        ├── main.py             # ponto de entrada — cria o app FastAPI
        ├── models.py           # define a estrutura dos dados (o que é um TODO)
        └── routers/
            └── todos.py        # agrupa todas as rotas relacionadas a TODO
```

**Por que essa estrutura?**

- `src/` separa o código-fonte dos arquivos de configuração. Evita importar módulos acidentalmente antes de instalar o pacote.
- `routers/` agrupa endpoints por recurso. Quando o projeto crescer (usuários, projetos, etc.), cada recurso terá seu próprio arquivo, mantendo o `main.py` limpo.
- `models.py` centraliza a definição dos dados. Se o formato do TODO mudar, você edita em um só lugar.

---

## Passo 1 — O ambiente Python

### Por que precisamos de um ambiente virtual?

Quando você instala um pacote com `pip install fastapi`, ele vai para o Python **global** da sua máquina. Se dois projetos usam versões diferentes de uma mesma biblioteca, há conflito.

O **virtual environment** (`.venv`) cria uma instalação Python isolada por projeto. Cada projeto tem suas próprias dependências, sem interferir nos outros.

Este projeto já usa `pyproject.toml` com `uv` como gerenciador. Para instalar as dependências:

```bash
# Instalar uv (se não tiver)
pip install uv

# Instalar as dependências do projeto
uv sync
```

Para rodar o servidor de desenvolvimento:

```bash
uv run fastapi dev src/python_api/main.py
```

**Por que `fastapi dev` em vez de só `python`?**

O `fastapi dev` usa o **uvicorn** (servidor ASGI) com **hot reload** — ele detecta mudanças nos arquivos e reinicia automaticamente. Sem isso, você precisaria parar e reiniciar o servidor manualmente a cada mudança.

---

## Passo 2 — O modelo de dados com Pydantic

Crie o arquivo `src/python_api/models.py`:

```python
from pydantic import BaseModel, Field
from datetime import datetime, timezone


class TodoCreate(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    description: str | None = None


class Todo(BaseModel):
    id: int
    title: str
    description: str | None = None
    completed: bool = False
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
```

**Por que Pydantic?**

Pydantic faz **validação automática de dados**. Quando alguém envia um JSON para sua API, o Pydantic:

1. Verifica se os campos obrigatórios estão presentes
2. Verifica se os tipos estão corretos (string, int, bool, etc.)
3. Aplica regras de validação (`min_length`, `max_length`, etc.)
4. Retorna erros claros se algo estiver errado

Sem Pydantic, você precisaria escrever todo esse código de validação manualmente — e provavelmente esqueceria algum caso.

**Por que dois modelos (`TodoCreate` e `Todo`)?**

Porque os dados que chegam (entrada) são diferentes dos dados que saem (resposta):

- **`TodoCreate`** — o que o cliente envia ao criar um TODO. Não tem `id`, `completed` ou `created_at` porque esses campos são gerados pelo servidor.
- **`Todo`** — a representação completa, com todos os campos incluindo os gerados.

Misturar os dois modelos seria um erro de design: você não quer que o cliente passe um `id` ao criar um recurso.

**Por que `str | None = None`?**

O `|` é o operador de union type do Python 3.10+. `str | None` significa "pode ser uma string ou None". O `= None` define o valor padrão quando não for informado. Isso torna o campo **opcional**.

---

## Passo 3 — O roteador de TODOs

Crie o diretório `src/python_api/routers/` e dentro dele o arquivo `todos.py`:

```python
from fastapi import APIRouter, HTTPException
from python_api.models import Todo, TodoCreate

router = APIRouter(prefix="/todos", tags=["todos"])

# Banco de dados em memória (por enquanto)
_db: list[Todo] = []
_next_id: int = 1


@router.get("/", response_model=list[Todo])
def list_todos():
    return _db


@router.get("/{todo_id}", response_model=Todo)
def get_todo(todo_id: int):
    todo = next((t for t in _db if t.id == todo_id), None)
    if todo is None:
        raise HTTPException(status_code=404, detail="TODO not found")
    return todo


@router.post("/", response_model=Todo, status_code=201)
def create_todo(data: TodoCreate):
    global _next_id
    todo = Todo(id=_next_id, **data.model_dump())
    _next_id += 1
    _db.append(todo)
    return todo


@router.put("/{todo_id}", response_model=Todo)
def update_todo(todo_id: int, data: TodoCreate):
    todo = next((t for t in _db if t.id == todo_id), None)
    if todo is None:
        raise HTTPException(status_code=404, detail="TODO not found")
    todo.title = data.title
    todo.description = data.description
    return todo


@router.delete("/{todo_id}", status_code=204)
def delete_todo(todo_id: int):
    global _db
    todo = next((t for t in _db if t.id == todo_id), None)
    if todo is None:
        raise HTTPException(status_code=404, detail="TODO not found")
    _db = [t for t in _db if t.id != todo_id]
```

**Explicando cada parte:**

### `APIRouter`

```python
router = APIRouter(prefix="/todos", tags=["todos"])
```

`APIRouter` é um mini-app que agrupa rotas relacionadas. O `prefix="/todos"` significa que todas as rotas definidas aqui começam com `/todos`. O `tags=["todos"]` é para organização na documentação Swagger.

**Por que não colocar tudo em `main.py`?** Porque conforme o projeto cresce, um único arquivo com todas as rotas fica impossível de manter. Cada roteador é responsável por um recurso.

### `@router.get("/", response_model=list[Todo])`

O `response_model` faz duas coisas:
1. **Documenta** — o Swagger sabe o formato da resposta
2. **Filtra** — garante que apenas os campos do modelo são retornados, mesmo que internamente você tenha campos extras

### `HTTPException`

```python
raise HTTPException(status_code=404, detail="TODO not found")
```

Quando um recurso não é encontrado, não retornamos `None` nem um dict vazio — levantamos uma exceção com o código HTTP correto. O FastAPI converte isso automaticamente em uma resposta JSON com o status code adequado.

**Por que exceção e não `return`?** Porque uma resposta de erro não é um "retorno normal" da função. Usar exceção é semanticamente correto e interrompe a execução imediatamente.

### `status_code=201` no POST

```python
@router.post("/", response_model=Todo, status_code=201)
```

O padrão REST diz que ao **criar** um recurso, a resposta deve ser `201 Created`, não `200 OK`. O `200` indica que a operação foi bem-sucedida, mas o `201` especifica que algo novo foi criado. É uma convenção importante para qualquer cliente que consuma sua API.

### `status_code=204` no DELETE

`204 No Content` significa: operação bem-sucedida, sem corpo na resposta. Faz sentido para DELETE — não há nada a retornar após deletar.

### `**data.model_dump()`

```python
todo = Todo(id=_next_id, **data.model_dump())
```

`model_dump()` converte o modelo Pydantic em um dicionário Python. O `**` (unpacking) passa cada chave do dicionário como argumento nomeado para o construtor de `Todo`. É equivalente a:

```python
todo = Todo(id=_next_id, title=data.title, description=data.description)
```

Mas usando `**data.model_dump()`, não precisamos listar cada campo manualmente — o código continua funcionando se adicionarmos campos ao modelo.

---

## Passo 4 — O ponto de entrada

Atualize `src/python_api/main.py`:

```python
from fastapi import FastAPI
from python_api.routers import todos

app = FastAPI(title="TODO API", version="0.1.0")

app.include_router(todos.router)


@app.get("/")
def root():
    return {"message": "Hello from python-api!"}
```

**Por que `include_router`?**

`include_router` registra todas as rotas do roteador no app principal. É o ponto de integração. O `main.py` não precisa saber como cada rota funciona — só precisa saber quais roteadores incluir.

---

## Passo 5 — O arquivo `__init__.py` do roteador

Crie `src/python_api/routers/__init__.py` (pode ser vazio):

```python
```

**Por que esse arquivo existe?**

O Python precisa de um `__init__.py` para reconhecer um diretório como **pacote** (módulo importável). Sem ele, `from python_api.routers import todos` falha. Em Python 3.3+ existem "namespace packages" sem `__init__.py`, mas a convenção com `__init__.py` ainda é mais clara e previsível.

---

## Passo 6 — Testar a API

Com o servidor rodando (`uv run fastapi dev src/python_api/main.py`), acesse:

- **http://localhost:8000/docs** — Swagger UI (interface visual para testar)
- **http://localhost:8000/redoc** — ReDoc (documentação mais legível)

Ou use `curl` no terminal:

```bash
# Listar todos os TODOs (lista vazia no início)
curl http://localhost:8000/todos/

# Criar um TODO
curl -X POST http://localhost:8000/todos/ \
  -H "Content-Type: application/json" \
  -d '{"title": "Estudar FastAPI", "description": "Completar o tutorial"}'

# Buscar o TODO de id 1
curl http://localhost:8000/todos/1

# Atualizar o TODO de id 1
curl -X PUT http://localhost:8000/todos/1 \
  -H "Content-Type: application/json" \
  -d '{"title": "Estudar FastAPI - atualizado"}'

# Deletar o TODO de id 1
curl -X DELETE http://localhost:8000/todos/1
```

---

## Estrutura final dos arquivos

```
src/python_api/
├── __init__.py
├── main.py
├── models.py
└── routers/
    ├── __init__.py
    └── todos.py
```

---

## Próximos passos sugeridos

Depois de ter o CRUD funcionando em memória, o próximo passo natural é persistir os dados:

1. **SQLite com SQLAlchemy** — adiciona um banco de dados real sem precisar instalar nada além das bibliotecas Python. Os dados sobrevivem a reinicializações do servidor.
2. **Campo `completed`** — adicione um endpoint `PATCH /todos/{id}/complete` para marcar um TODO como concluído sem precisar enviar todos os campos.
3. **Testes automatizados** — o projeto já tem `pytest` e `httpx` instalados. Escreva testes para cada endpoint.

---

## Recursos para aprofundar

- [Documentação oficial do FastAPI](https://fastapi.tiangolo.com/tutorial/) — excelente e parcialmente em português
- [Documentação do Pydantic](https://docs.pydantic.dev/) — validação de dados
- [HTTP Status Codes](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status) — referência completa
