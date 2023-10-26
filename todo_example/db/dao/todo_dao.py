import uuid
from typing import List

from fastapi import HTTPException

from todo_example.db.dao.base_dao import BaseDAO
from todo_example.db.models.todo_model import TodoModel
from todo_example.web.api.todo.schema import TodoCreateSchema, TodoSchema


class TodoDAO(BaseDAO):
    async def get_one_by_id(self, todo_id: uuid.UUID) -> TodoSchema:
        return await self.get_object_by_id(TodoModel, TodoSchema, todo_id)

    async def get_all_todos(self) -> List[TodoSchema]:
        return await self.get_all_objects(TodoModel, TodoSchema)

    async def create_todo(
        self,
        todo: TodoCreateSchema,
        current_user_id: uuid.UUID,
    ):
        try:
            todo_dict = todo.model_dump()
            todo = TodoModel(
                user_id=current_user_id,
                title=todo_dict["title"],
                description=todo_dict["description"],
            )
            self.session.add(todo)
            await self.session.commit()
            return {"message": "Todo created successfully"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        # return await self.create_object(TodoModel, TodoCreateSchema(**todo_dict),
        #                                 "user_id", current_user_id)
