# Roteiro: REST API de TODO em Python

## Etapa 1 — Entender o ambiente Python

Antes de qualquer coisa, você precisa entender como o Python gerencia projetos e dependências:

- **O que é um `virtualenv`**: ambiente isolado para instalar pacotes sem afetar o sistema
- **O que é o `pip`**: gerenciador de pacotes do Python
- **O que é o `pyproject.toml` ou `requirements.txt`**: arquivo que lista as dependências do projeto

**Pesquise sobre**: "Python virtual environment tutorial" e "pip install packages"

---

## Etapa 2 — Escolher o framework web

Para criar APIs REST em Python, os frameworks mais usados são:

| Framework | Característica |
| --------- | -------------- |
| **FastAPI** | Moderno, rápido, tipado, gera documentação automática |
| **Flask** | Simples e minimalista, ótimo para aprender |
| **Django REST** | Completo e robusto, mais complexo |

**Recomendação para aprender**: comece com **FastAPI** — ele força boas práticas de tipagem e gera uma UI de documentação automática (Swagger) que facilita testar sua API.

---

## Etapa 3 — Estrutura do projeto

Uma API de TODO simples terá esta estrutura de arquivos:

```text
python-api/
├── main.py           # ponto de entrada da aplicação
├── models.py         # estrutura dos dados (o que é um TODO)
├── database.py       # conexão e configuração do banco de dados
├── routes/
│   └── todos.py      # as rotas/endpoints da API
└── requirements.txt  # dependências do projeto
```

---

## Etapa 4 — Modelar os dados

Um TODO tem campos simples. Pense em:

- `id` — identificador único
- `title` — título da tarefa
- `description` — descrição (opcional)
- `completed` — booleano: feita ou não
- `created_at` — data de criação

No FastAPI você vai usar **Pydantic** para definir esses modelos com tipagem.

**Pesquise sobre**: "Pydantic models Python" e "Python type hints"

---

## Etapa 5 — Criar os endpoints REST

Uma API de TODO precisa dos seguintes endpoints:

| Método | Rota | O que faz |
| ------ | ---- | --------- |
| `GET` | `/todos` | Lista todos os TODOs |
| `GET` | `/todos/{id}` | Busca um TODO específico |
| `POST` | `/todos` | Cria um novo TODO |
| `PUT` | `/todos/{id}` | Atualiza um TODO |
| `DELETE` | `/todos/{id}` | Remove um TODO |

**Pesquise sobre**: "FastAPI path operations tutorial" e "HTTP methods REST"

---

## Etapa 6 — Armazenar os dados

Você tem algumas opções, da mais simples para a mais completa:

1. **Lista em memória** (começo) — dados somem quando reinicia o servidor
2. **SQLite com SQLAlchemy** — banco de dados local em arquivo, sem instalar nada
3. **PostgreSQL** — banco de dados real para produção

**Recomendação**: comece com **lista em memória**, depois evolua para **SQLite**.

**Pesquise sobre**: "SQLAlchemy tutorial" e "SQLite Python"

---

## Etapa 7 — Testar a API

O FastAPI já gera automaticamente uma interface visual em:

- `http://localhost:8000/docs` — Swagger UI
- `http://localhost:8000/redoc` — ReDoc

Você também pode usar ferramentas como:

- **curl** no terminal
- **Postman** ou **Insomnia** (apps gráficos)
- **Thunder Client** (extensão do VSCode)

---

## Ordem sugerida para implementar

1. Crie o `virtualenv` e instale o FastAPI
2. Crie um `main.py` com um endpoint `GET /` que retorna `{"message": "Hello World"}`
3. Rode o servidor e acesse no browser
4. Adicione o modelo `Todo` com Pydantic
5. Implemente o `POST /todos` com lista em memória
6. Implemente o `GET /todos`
7. Implemente `GET /todos/{id}`, `PUT` e `DELETE`
8. Substitua a lista em memória por SQLite

---

## Recursos para estudar

- [Documentação oficial do FastAPI](https://fastapi.tiangolo.com/tutorial/) — excelente, em português em algumas partes
- [Python.org Tutorial](https://docs.python.org/3/tutorial/) — base da linguagem
- [Real Python](https://realpython.com) — tutoriais práticos
