import uuid
from typing import List

from fastapi import APIRouter, Depends

from todo_example.db.dao.todo_dao import TodoDAO
from todo_example.db.models.user_model import UserModel
from todo_example.services.authentication.deps import get_current_user
from todo_example.web.api.todo.schema import TodoCreateSchema, TodoSchema

router = APIRouter()


@router.post(
    "/create",
)
async def create_todo(
    todo: TodoCreateSchema = Depends(),
    current_user: UserModel = Depends(get_current_user),
    todo_dao: TodoDAO = Depends(),
):
    return await todo_dao.create_todo(todo, current_user["id"])


@router.get("/list", response_model=List[TodoSchema])
async def get_list_todos(todo_dao: TodoDAO = Depends()) -> List[TodoSchema]:
    return await todo_dao.get_all_todos()


@router.get("/{todo_id}", response_model=TodoSchema)
async def get_todo(todo_id: uuid.UUID, todo_dao: TodoDAO = Depends()) -> TodoSchema:
    return await todo_dao.get_one_by_id(todo_id)
