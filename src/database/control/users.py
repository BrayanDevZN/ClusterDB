"controla a tabela de users"

from src.logs.log import logger
from src.database.models.users import Users

from sqlalchemy import select, update
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from uuid import UUID
from typing import Any


class UserControl:

    def __init__(self, session_maker: async_sessionmaker[AsyncSession]) -> None:
        self.session_maker = session_maker
        logger.info("UserControl initialized")

    def _to_dict(self, user: Users) -> dict[str, Any]:
        return {column.name: getattr(user, column.name) for column in user.__table__.columns}

    async def create(self, user_name: str, email: str, password: str, role: str = "user") -> dict[str, Any]:
        logger.info(f"Creating user {user_name}...")

        try:
            async with self.session_maker() as session:
                async with session.begin():
                    user = Users(user_name=user_name, email=email, password=password, role=role)
                    session.add(user)
                    await session.flush()
                    await session.refresh(user)
                    data = self._to_dict(user)

            logger.success(f"User {user_name} created successfully")
            return data

        except IntegrityError as error:
            logger.error(f"Integrity error while creating user {user_name}: {error}")
            raise

        except SQLAlchemyError as error:
            logger.error(f"Database error while creating user {user_name}: {error}")
            raise

        except Exception as error:
            logger.critical(f"Unexpected error while creating user {user_name}: {error}")
            raise

    async def get_by_id(self, user_id: int) -> dict[str, Any] | None:
        logger.info(f"Getting user by id {user_id}...")

        try:
            async with self.session_maker() as session:
                async with session.begin():
                    result = await session.execute(select(Users).where(Users.id == user_id))
                    user = result.scalar_one_or_none()

                    if user is None:
                        logger.warning(f"User with id {user_id} not found")
                        return None

                    data = self._to_dict(user)

            logger.success(f"User with id {user_id} found successfully")
            return data

        except SQLAlchemyError as error:
            logger.error(f"Database error while getting user by id {user_id}: {error}")
            raise

        except Exception as error:
            logger.critical(f"Unexpected error while getting user by id {user_id}: {error}")
            raise

    async def get_by_public_id(self, public_id: UUID) -> dict[str, Any] | None:
        logger.info(f"Getting user by public id {public_id}...")

        try:
            async with self.session_maker() as session:
                async with session.begin():
                    result = await session.execute(select(Users).where(Users.public_id == public_id))
                    user = result.scalar_one_or_none()

                    if user is None:
                        logger.warning(f"User with public id {public_id} not found")
                        return None

                    data = self._to_dict(user)

            logger.success(f"User with public id {public_id} found successfully")
            return data

        except SQLAlchemyError as error:
            logger.error(f"Database error while getting user by public id {public_id}: {error}")
            raise

        except Exception as error:
            logger.critical(f"Unexpected error while getting user by public id {public_id}: {error}")
            raise

    async def get_by_username(self, user_name: str) -> dict[str, Any] | None:
        logger.info(f"Getting user by username {user_name}...")

        try:
            async with self.session_maker() as session:
                async with session.begin():
                    result = await session.execute(select(Users).where(Users.user_name == user_name))
                    user = result.scalar_one_or_none()

                    if user is None:
                        logger.warning(f"User {user_name} not found")
                        return None

                    data = self._to_dict(user)

            logger.success(f"User {user_name} found successfully")
            return data

        except SQLAlchemyError as error:
            logger.error(f"Database error while getting user {user_name}: {error}")
            raise

        except Exception as error:
            logger.critical(f"Unexpected error while getting user {user_name}: {error}")
            raise

    async def get_by_email(self, email: str) -> dict[str, Any] | None:
        logger.info(f"Getting user by email {email}...")

        try:
            async with self.session_maker() as session:
                async with session.begin():
                    result = await session.execute(select(Users).where(Users.email == email))
                    user = result.scalar_one_or_none()

                    if user is None:
                        logger.warning(f"User with email {email} not found")
                        return None

                    data = self._to_dict(user)

            logger.success(f"User with email {email} found successfully")
            return data

        except SQLAlchemyError as error:
            logger.error(f"Database error while getting user by email {email}: {error}")
            raise

        except Exception as error:
            logger.critical(f"Unexpected error while getting user by email {email}: {error}")
            raise

    async def get_all(self) -> list[dict[str, Any]]:
        logger.info("Getting all users...")

        try:
            async with self.session_maker() as session:
                async with session.begin():
                    result = await session.execute(select(Users))
                    users = result.scalars().all()
                    data = [self._to_dict(user) for user in users]

            logger.success(f"Retrieved {len(data)} users successfully")
            return data

        except SQLAlchemyError as error:
            logger.error(f"Database error while getting all users: {error}")
            raise

        except Exception as error:
            logger.critical(f"Unexpected error while getting all users: {error}")
            raise

    async def update(self, user_id: int, **values) -> dict[str, Any] | None:
        logger.info(f"Updating user {user_id}...")

        try:
            async with self.session_maker() as session:
                async with session.begin():
                    result = await session.execute(update(Users).where(Users.id == user_id).values(**values).returning(Users))
                    user = result.scalar_one_or_none()

                    if user is None:
                        logger.warning(f"User with id {user_id} not found")
                        return None

                    data = self._to_dict(user)

            logger.success(f"User {user_id} updated successfully")
            return data

        except IntegrityError as error:
            logger.error(f"Integrity error while updating user {user_id}: {error}")
            raise

        except SQLAlchemyError as error:
            logger.error(f"Database error while updating user {user_id}: {error}")
            raise

        except Exception as error:
            logger.critical(f"Unexpected error while updating user {user_id}: {error}")
            raise

    async def delete(self, user_id: int) -> dict[str, Any] | None:
        logger.info(f"Deleting user {user_id}...")

        try:
            async with self.session_maker() as session:
                async with session.begin():
                    result = await session.execute(select(Users).where(Users.id == user_id))
                    user = result.scalar_one_or_none()

                    if user is None:
                        logger.warning(f"User with id {user_id} not found")
                        return None

                    data = self._to_dict(user)
                    await session.delete(user)

            logger.success(f"User {user_id} deleted successfully")
            return data

        except IntegrityError as error:
            logger.error(f"Integrity error while deleting user {user_id}: {error}")
            raise

        except SQLAlchemyError as error:
            logger.error(f"Database error while deleting user {user_id}: {error}")
            raise

        except Exception as error:
            logger.critical(f"Unexpected error while deleting user {user_id}: {error}")
            raise