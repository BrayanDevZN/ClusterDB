"controla a tabela de keys"

from src.logs.log import logger
from src.database.models.keys import keys

from sqlalchemy import select, update
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from uuid import UUID
from typing import Any


class KeyControl:

    def __init__(self, session_maker: async_sessionmaker[AsyncSession]) -> None:
        self.session_maker = session_maker
        logger.info("KeyControl initialized")

    def _to_dict(self, key: keys) -> dict[str, Any]:
        return {column.name: getattr(key, column.name) for column in key.__table__.columns}

    async def create(self, user_id: int, permission_db: str = "all", permission_actions: str = "all", environment: str = "test") -> dict[str, Any]:
        logger.info(f"Creating key for user {user_id}...")

        try:
            async with self.session_maker() as session:
                async with session.begin():
                    key = keys(user_id=user_id, permission_db=permission_db, permission_actions=permission_actions, environment=environment)
                    session.add(key)
                    await session.flush()
                    await session.refresh(key)
                    data = self._to_dict(key)

            logger.success(f"Key {key.key} created successfully for user {user_id}")
            return data

        except IntegrityError as error:
            logger.error(f"Integrity error while creating key for user {user_id}: {error}")
            raise

        except SQLAlchemyError as error:
            logger.error(f"Database error while creating key for user {user_id}: {error}")
            raise

        except Exception as error:
            logger.critical(f"Unexpected error while creating key for user {user_id}: {error}")
            raise

    async def get_by_id(self, key_id: int) -> dict[str, Any] | None:
        logger.info(f"Getting key by id {key_id}...")

        try:
            async with self.session_maker() as session:
                async with session.begin():
                    result = await session.execute(select(keys).where(keys.id == key_id))
                    key = result.scalar_one_or_none()

                    if key is None:
                        logger.warning(f"Key with id {key_id} not found")
                        return None

                    data = self._to_dict(key)

            logger.success(f"Key with id {key_id} found successfully")
            return data

        except SQLAlchemyError as error:
            logger.error(f"Database error while getting key by id {key_id}: {error}")
            raise

        except Exception as error:
            logger.critical(f"Unexpected error while getting key by id {key_id}: {error}")
            raise

    async def get_by_key(self, key_value: UUID) -> dict[str, Any] | None:
        logger.info(f"Getting key {key_value}...")

        try:
            async with self.session_maker() as session:
                async with session.begin():
                    result = await session.execute(select(keys).where(keys.key == key_value))
                    key = result.scalar_one_or_none()

                    if key is None:
                        logger.warning(f"Key {key_value} not found")
                        return None

                    data = self._to_dict(key)

            logger.success(f"Key {key_value} found successfully")
            return data

        except SQLAlchemyError as error:
            logger.error(f"Database error while getting key {key_value}: {error}")
            raise

        except Exception as error:
            logger.critical(f"Unexpected error while getting key {key_value}: {error}")
            raise

    async def get_by_user_id(self, user_id: int) -> list[dict[str, Any]]:
        logger.info(f"Getting keys for user {user_id}...")

        try:
            async with self.session_maker() as session:
                async with session.begin():
                    result = await session.execute(select(keys).where(keys.user_id == user_id))
                    user_keys = result.scalars().all()
                    data = [self._to_dict(key) for key in user_keys]

            logger.success(f"Retrieved {len(data)} keys for user {user_id}")
            return data

        except SQLAlchemyError as error:
            logger.error(f"Database error while getting keys for user {user_id}: {error}")
            raise

        except Exception as error:
            logger.critical(f"Unexpected error while getting keys for user {user_id}: {error}")
            raise

    async def get_by_environment(self, environment: str) -> list[dict[str, Any]]:
        logger.info(f"Getting keys from environment {environment}...")

        try:
            async with self.session_maker() as session:
                async with session.begin():
                    result = await session.execute(select(keys).where(keys.environment == environment))
                    environment_keys = result.scalars().all()
                    data = [self._to_dict(key) for key in environment_keys]

            logger.success(f"Retrieved {len(data)} keys from environment {environment}")
            return data

        except SQLAlchemyError as error:
            logger.error(f"Database error while getting keys from environment {environment}: {error}")
            raise

        except Exception as error:
            logger.critical(f"Unexpected error while getting keys from environment {environment}: {error}")
            raise

    async def get_all(self) -> list[dict[str, Any]]:
        logger.info("Getting all keys...")

        try:
            async with self.session_maker() as session:
                async with session.begin():
                    result = await session.execute(select(keys))
                    all_keys = result.scalars().all()
                    data = [self._to_dict(key) for key in all_keys]

            logger.success(f"Retrieved {len(data)} keys successfully")
            return data

        except SQLAlchemyError as error:
            logger.error(f"Database error while getting all keys: {error}")
            raise

        except Exception as error:
            logger.critical(f"Unexpected error while getting all keys: {error}")
            raise

    async def update(self, key_id: int, **values) -> dict[str, Any] | None:
        logger.info(f"Updating key {key_id}...")

        try:
            async with self.session_maker() as session:
                async with session.begin():
                    result = await session.execute(update(keys).where(keys.id == key_id).values(**values).returning(keys))
                    key = result.scalar_one_or_none()

                    if key is None:
                        logger.warning(f"Key with id {key_id} not found")
                        return None

                    data = self._to_dict(key)

            logger.success(f"Key {key_id} updated successfully")
            return data

        except IntegrityError as error:
            logger.error(f"Integrity error while updating key {key_id}: {error}")
            raise

        except SQLAlchemyError as error:
            logger.error(f"Database error while updating key {key_id}: {error}")
            raise

        except Exception as error:
            logger.critical(f"Unexpected error while updating key {key_id}: {error}")
            raise

    async def delete(self, key_id: int) -> dict[str, Any] | None:
        logger.info(f"Deleting key {key_id}...")

        try:
            async with self.session_maker() as session:
                async with session.begin():
                    result = await session.execute(select(keys).where(keys.id == key_id))
                    key = result.scalar_one_or_none()

                    if key is None:
                        logger.warning(f"Key with id {key_id} not found")
                        return None

                    data = self._to_dict(key)
                    await session.delete(key)

            logger.success(f"Key {key_id} deleted successfully")
            return data

        except IntegrityError as error:
            logger.error(f"Integrity error while deleting key {key_id}: {error}")
            raise

        except SQLAlchemyError as error:
            logger.error(f"Database error while deleting key {key_id}: {error}")
            raise

        except Exception as error:
            logger.critical(f"Unexpected error while deleting key {key_id}: {error}")
            raise