from fastapi import APIRouter, Depends, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from todo_example.db.dependencies import get_db_session
from todo_example.db.models.user_model import UserModel
from todo_example.services.authentication.deps import get_current_user
from todo_example.web.api.users.schema import UserRegister

router = APIRouter()


@router.post("/register")
async def register_user(
    register_schema: UserRegister = Depends(),
    db: AsyncSession = Depends(get_db_session),
):
    from todo_example.db.dao.user_dao import UserDAO

    user_dao = UserDAO(db)
    return await user_dao.register_user(register_schema)


@router.post("/login")
async def login_user(
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db_session),
):
    from todo_example.db.dao.user_dao import UserDAO

    user_data = UserDAO(db)
    return await user_data.login(response, form_data)


@router.get("/me")
async def get_current_me(
    current_user: UserModel = Depends(get_current_user),
):
    return current_user
