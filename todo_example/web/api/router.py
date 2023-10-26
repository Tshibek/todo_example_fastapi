from fastapi.routing import APIRouter

from todo_example.web.api import monitoring, todo, users

api_router = APIRouter()
api_router.include_router(monitoring.router)
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(todo.router, prefix="/todo", tags=["todo"])
