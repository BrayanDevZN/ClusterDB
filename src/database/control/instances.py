"controla a tabela de instances"

from src.logs.log import logger
from src.database.models.instances import Instances
from src.database.models.central import Central

from sqlalchemy import select, update
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from uuid import UUID
from typing import Any


class InstanceControl:

    def __init__(self, session_maker: async_sessionmaker[AsyncSession]) -> None:
        self.session_maker = session_maker
        logger.info("InstanceControl initialized")


    def _to_dict(self, instance: Instances, mean: list[float] | None = None) -> dict[str, Any]:
        data = {column.name: getattr(instance, column.name) for column in instance.__table__.columns}
        data["mean"] = mean
        return data


    async def create(self, cluster_id: int) -> dict[str, Any]:
        logger.info(f"Creating instance for cluster {cluster_id}...")

        try:
            async with self.session_maker() as session:
                async with session.begin():

                    instance = Instances(cluster_id=cluster_id)
                    session.add(instance)

                    await session.flush()
                    await session.refresh(instance)

                    data = self._to_dict(instance)

            logger.success(f"Instance {instance.id} created successfully for cluster {cluster_id}")
            return data

        except IntegrityError as error:
            logger.error(f"Integrity error while creating instance for cluster {cluster_id}: {error}")
            raise

        except SQLAlchemyError as error:
            logger.error(f"Database error while creating instance for cluster {cluster_id}: {error}")
            raise

        except Exception as error:
            logger.critical(f"Unexpected error while creating instance for cluster {cluster_id}: {error}")
            raise


    async def create_central(self, instance_id: UUID, mean: list[float]) -> dict[str, Any]:
        logger.info(f"Creating central for instance {instance_id}...")

        try:
            async with self.session_maker() as session:
                async with session.begin():

                    central = Central(
                        instance_id=instance_id,
                        mean=mean
                    )

                    session.add(central)

                    await session.flush()
                    await session.refresh(central)

                    data = {
                        column.name: getattr(central, column.name)
                        for column in central.__table__.columns
                    }

            logger.success(f"Central created successfully for instance {instance_id}")
            return data

        except IntegrityError as error:
            logger.error(f"Integrity error while creating central for instance {instance_id}: {error}")
            raise

        except SQLAlchemyError as error:
            logger.error(f"Database error while creating central for instance {instance_id}: {error}")
            raise

        except Exception as error:
            logger.critical(f"Unexpected error while creating central for instance {instance_id}: {error}")
            raise


    async def get_by_id(self, instance_id: UUID) -> dict[str, Any] | None:
        logger.info(f"Getting instance by id {instance_id}...")

        try:
            async with self.session_maker() as session:
                async with session.begin():

                    result = await session.execute(
                        select(Instances, Central.mean)
                        .outerjoin(Central, Central.instance_id == Instances.id)
                        .where(Instances.id == instance_id)
                    )

                    row = result.one_or_none()

                    if row is None:
                        logger.warning(f"Instance with id {instance_id} not found")
                        return None

                    instance, mean = row
                    data = self._to_dict(instance, mean)

            logger.success(f"Instance with id {instance_id} found successfully")
            return data

        except SQLAlchemyError as error:
            logger.error(f"Database error while getting instance by id {instance_id}: {error}")
            raise

        except Exception as error:
            logger.critical(f"Unexpected error while getting instance by id {instance_id}: {error}")
            raise


    async def get_by_cluster_id(self, cluster_id: int) -> list[dict[str, Any]]:
        logger.info(f"Getting instances from cluster {cluster_id}...")

        try:
            async with self.session_maker() as session:
                async with session.begin():

                    result = await session.execute(
                        select(Instances, Central.mean)
                        .outerjoin(Central, Central.instance_id == Instances.id)
                        .where(Instances.cluster_id == cluster_id)
                    )

                    rows = result.all()

                    data = [
                        self._to_dict(instance, mean)
                        for instance, mean in rows
                    ]

            logger.success(f"Retrieved {len(data)} instances from cluster {cluster_id}")
            return data

        except SQLAlchemyError as error:
            logger.error(f"Database error while getting instances from cluster {cluster_id}: {error}")
            raise

        except Exception as error:
            logger.critical(f"Unexpected error while getting instances from cluster {cluster_id}: {error}")
            raise


    async def get_all(self) -> list[dict[str, Any]]:
        logger.info("Getting all instances...")

        try:
            async with self.session_maker() as session:
                async with session.begin():

                    result = await session.execute(
                        select(Instances, Central.mean)
                        .outerjoin(Central, Central.instance_id == Instances.id)
                    )

                    rows = result.all()

                    data = [
                        self._to_dict(instance, mean)
                        for instance, mean in rows
                    ]

            logger.success(f"Retrieved {len(data)} instances successfully")
            return data

        except SQLAlchemyError as error:
            logger.error(f"Database error while getting all instances: {error}")
            raise

        except Exception as error:
            logger.critical(f"Unexpected error while getting all instances: {error}")
            raise


    async def update(self, instance_id: UUID, mean: list[float] | None = None, **values) -> dict[str, Any] | None:
        logger.info(f"Updating instance {instance_id}...")

        try:
            async with self.session_maker() as session:
                async with session.begin():

                    result = await session.execute(
                        select(Instances)
                        .where(Instances.id == instance_id)
                    )

                    instance = result.scalar_one_or_none()

                    if instance is None:
                        logger.warning(f"Instance with id {instance_id} not found")
                        return None

                    if values:
                        await session.execute(
                            update(Instances)
                            .where(Instances.id == instance_id)
                            .values(**values)
                        )

                    if mean is not None:
                        await session.execute(
                            update(Central)
                            .where(Central.instance_id == instance_id)
                            .values(mean=mean)
                        )

                    await session.flush()

                    result = await session.execute(
                        select(Instances, Central.mean)
                        .outerjoin(Central, Central.instance_id == Instances.id)
                        .where(Instances.id == instance_id)
                    )

                    instance, current_mean = result.one()
                    data = self._to_dict(instance, current_mean)

            logger.success(f"Instance {instance_id} updated successfully")
            return data

        except IntegrityError as error:
            logger.error(f"Integrity error while updating instance {instance_id}: {error}")
            raise

        except SQLAlchemyError as error:
            logger.error(f"Database error while updating instance {instance_id}: {error}")
            raise

        except Exception as error:
            logger.critical(f"Unexpected error while updating instance {instance_id}: {error}")
            raise


    async def delete(self, instance_id: UUID) -> dict[str, Any] | None:
        logger.info(f"Deleting instance {instance_id}...")

        try:
            async with self.session_maker() as session:
                async with session.begin():

                    result = await session.execute(
                        select(Instances, Central.mean)
                        .outerjoin(Central, Central.instance_id == Instances.id)
                        .where(Instances.id == instance_id)
                    )

                    row = result.one_or_none()

                    if row is None:
                        logger.warning(f"Instance with id {instance_id} not found")
                        return None

                    instance, mean = row
                    data = self._to_dict(instance, mean)

                    await session.delete(instance)

            logger.success(f"Instance {instance_id} deleted successfully")
            return data

        except IntegrityError as error:
            logger.error(f"Integrity error while deleting instance {instance_id}: {error}")
            raise

        except SQLAlchemyError as error:
            logger.error(f"Database error while deleting instance {instance_id}: {error}")
            raise

        except Exception as error:
            logger.critical(f"Unexpected error while deleting instance {instance_id}: {error}")
            raise