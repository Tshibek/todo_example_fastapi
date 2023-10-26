import uuid
from typing import List, Type, TypeVar

from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from starlette import status

from todo_example.db.dependencies import get_db_session

ModelType = TypeVar("ModelType")
SchemaType = TypeVar("SchemaType")


class BaseDAO:
    def __init__(self, session: AsyncSession = Depends(get_db_session)):
        self.session = session

    async def _execute_in_transaction(self, func):
        async with self.session as session:
            async with session.begin():
                return await func(session)

    async def execute_query(self, session, query):
        result = await session.execute(query)
        return result.scalars().all()

    async def get_object_by_id(
        self,
        model: Type[ModelType],
        schema: Type[SchemaType],
        object_id: uuid.UUID,
    ) -> SchemaType:
        if not object_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid object_id",
            )

        query = select(model).where(model.id == object_id)
        row = await self._execute_in_transaction(
            lambda session: self.execute_query(session, query),
        )

        if not row:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Object not found",
            )
        return schema.from_orm(row[0])

    async def get_all_objects(
        self,
        model: Type[ModelType],
        schema: Type[SchemaType],
    ) -> List[SchemaType]:
        query = select(model)
        rows = await self._execute_in_transaction(
            lambda session: self.execute_query(session, query),
        )
        return [schema.from_orm(row) for row in rows]

    async def create_object(
        self,
        model,
        input_schema: SchemaType,
        foreign_field: str = None,
        foreign_value: uuid.UUID = None,
    ) -> SchemaType:
        new_object = model(**input_schema.dict())
        if foreign_field is not None and foreign_value is not None:
            setattr(new_object, foreign_field, foreign_value)
        self.session.add(new_object)
        await self.session.commit()
        await self.session.refresh(new_object)
        return input_schema.from_orm(new_object)

    async def get_object_by_name(
        self,
        model: Type[ModelType],
        field_name: str,
        object_name: str,
        schema: Type[SchemaType],
    ) -> SchemaType:
        if not object_name:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid object_name",
            )

        query = select(model).where(getattr(model, field_name) == object_name)
        row = await self._execute_in_transaction(
            lambda session: self.execute_query(session, query),
        )

        if not row:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Object not found",
            )
        return schema.from_orm(row[0])
