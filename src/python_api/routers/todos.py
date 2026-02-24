from fastapi import APIRouter, HTTPException

from python_api.models import Todo, TodoCreate

router = APIRouter(prefix="/todos", tags=["todos"])

_db: list[Todo] = []
_next_id: int = 1

@router.get("/", response_model=list[Todo])
def list_todos() -> list[Todo]:
    return _db

@router.get("/{todo_id}", response_model=Todo)
def get_todo(todo_id: int) -> Todo:
    todo = next((t for t in _db if t.id == todo_id), None)
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo

@router.post("/", response_model=Todo, status_code=201)
def create_todo(todo: TodoCreate) -> Todo:
    global _next_id
    new_todo = Todo(id=_next_id, **todo.model_dump())
    _next_id += 1
    _db.append(new_todo)
    return new_todo

@router.put("/{todo_id}", response_model=Todo)
def update_todo(todo_id: int, updated_todo: TodoCreate) -> Todo:
    todo = next((t for t in _db if t.id == todo_id), None)
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    todo.title = updated_todo.title
    todo.description = updated_todo.description
    return todo

@router.delete("/{todo_id}", status_code=204)
def delete_todo(todo_id: int) -> None:
    global _db
    todo = next((t for t in _db if t.id == todo_id), None)
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    _db = [t for t in _db if t.id != todo_id]