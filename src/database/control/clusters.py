"controla a tabela de clusters"

from src.logs.log import logger
from src.database.models.clusters import Clusters

from sqlalchemy import select, update
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from uuid import UUID
from typing import Any


class ClusterControl:

    def __init__(self, session_maker: async_sessionmaker[AsyncSession]) -> None:
        self.session_maker = session_maker
        logger.info("ClusterControl initialized")

    def _to_dict(self, cluster: Clusters) -> dict[str, Any]:
        return {column.name: getattr(cluster, column.name) for column in cluster.__table__.columns}

    async def create(self, cluster_name: str, instance_limit: int, created_key: int) -> dict[str, Any]:
        logger.info(f"Creating cluster {cluster_name}...")

        try:
            async with self.session_maker() as session:
                async with session.begin():
                    cluster = Clusters(cluster_name=cluster_name, instance_limit=instance_limit, created_key=created_key)
                    session.add(cluster)
                    await session.flush()
                    await session.refresh(cluster)
                    data = self._to_dict(cluster)

            logger.success(f"Cluster {cluster_name} created successfully")
            return data

        except IntegrityError as error:
            logger.error(f"Integrity error while creating cluster {cluster_name}: {error}")
            raise

        except SQLAlchemyError as error:
            logger.error(f"Database error while creating cluster {cluster_name}: {error}")
            raise

        except Exception as error:
            logger.critical(f"Unexpected error while creating cluster {cluster_name}: {error}")
            raise

    async def get_by_id(self, cluster_id: int) -> dict[str, Any] | None:
        logger.info(f"Getting cluster by id {cluster_id}...")

        try:
            async with self.session_maker() as session:
                async with session.begin():
                    result = await session.execute(select(Clusters).where(Clusters.id == cluster_id))
                    cluster = result.scalar_one_or_none()

                    if cluster is None:
                        logger.warning(f"Cluster with id {cluster_id} not found")
                        return None

                    data = self._to_dict(cluster)

            logger.success(f"Cluster with id {cluster_id} found successfully")
            return data

        except SQLAlchemyError as error:
            logger.error(f"Database error while getting cluster by id {cluster_id}: {error}")
            raise

        except Exception as error:
            logger.critical(f"Unexpected error while getting cluster by id {cluster_id}: {error}")
            raise

    async def get_by_public_id(self, public_id: UUID) -> dict[str, Any] | None:
        logger.info(f"Getting cluster by public id {public_id}...")

        try:
            async with self.session_maker() as session:
                async with session.begin():
                    result = await session.execute(select(Clusters).where(Clusters.public_id == public_id))
                    cluster = result.scalar_one_or_none()

                    if cluster is None:
                        logger.warning(f"Cluster with public id {public_id} not found")
                        return None

                    data = self._to_dict(cluster)

            logger.success(f"Cluster with public id {public_id} found successfully")
            return data

        except SQLAlchemyError as error:
            logger.error(f"Database error while getting cluster by public id {public_id}: {error}")
            raise

        except Exception as error:
            logger.critical(f"Unexpected error while getting cluster by public id {public_id}: {error}")
            raise

    async def get_by_name(self, cluster_name: str) -> dict[str, Any] | None:
        logger.info(f"Getting cluster by name {cluster_name}...")

        try:
            async with self.session_maker() as session:
                async with session.begin():
                    result = await session.execute(select(Clusters).where(Clusters.cluster_name == cluster_name))
                    cluster = result.scalar_one_or_none()

                    if cluster is None:
                        logger.warning(f"Cluster {cluster_name} not found")
                        return None

                    data = self._to_dict(cluster)

            logger.success(f"Cluster {cluster_name} found successfully")
            return data

        except SQLAlchemyError as error:
            logger.error(f"Database error while getting cluster {cluster_name}: {error}")
            raise

        except Exception as error:
            logger.critical(f"Unexpected error while getting cluster {cluster_name}: {error}")
            raise

    async def get_by_created_key(self, key_id: int) -> list[dict[str, Any]]:
        logger.info(f"Getting clusters created by key {key_id}...")

        try:
            async with self.session_maker() as session:
                async with session.begin():
                    result = await session.execute(select(Clusters).where(Clusters.created_key == key_id))
                    clusters = result.scalars().all()
                    data = [self._to_dict(cluster) for cluster in clusters]

            logger.success(f"Retrieved {len(data)} clusters created by key {key_id}")
            return data

        except SQLAlchemyError as error:
            logger.error(f"Database error while getting clusters created by key {key_id}: {error}")
            raise

        except Exception as error:
            logger.critical(f"Unexpected error while getting clusters created by key {key_id}: {error}")
            raise

    async def get_all(self) -> list[dict[str, Any]]:
        logger.info("Getting all clusters...")

        try:
            async with self.session_maker() as session:
                async with session.begin():
                    result = await session.execute(select(Clusters))
                    clusters = result.scalars().all()
                    data = [self._to_dict(cluster) for cluster in clusters]

            logger.success(f"Retrieved {len(data)} clusters successfully")
            return data

        except SQLAlchemyError as error:
            logger.error(f"Database error while getting all clusters: {error}")
            raise

        except Exception as error:
            logger.critical(f"Unexpected error while getting all clusters: {error}")
            raise

    async def update(self, cluster_id: int, **values) -> dict[str, Any] | None:
        logger.info(f"Updating cluster {cluster_id}...")

        try:
            async with self.session_maker() as session:
                async with session.begin():
                    result = await session.execute(update(Clusters).where(Clusters.id == cluster_id).values(**values).returning(Clusters))
                    cluster = result.scalar_one_or_none()

                    if cluster is None:
                        logger.warning(f"Cluster with id {cluster_id} not found")
                        return None

                    data = self._to_dict(cluster)

            logger.success(f"Cluster {cluster_id} updated successfully")
            return data

        except IntegrityError as error:
            logger.error(f"Integrity error while updating cluster {cluster_id}: {error}")
            raise

        except SQLAlchemyError as error:
            logger.error(f"Database error while updating cluster {cluster_id}: {error}")
            raise

        except Exception as error:
            logger.critical(f"Unexpected error while updating cluster {cluster_id}: {error}")
            raise

    async def delete(self, cluster_id: int) -> dict[str, Any] | None:
        logger.info(f"Deleting cluster {cluster_id}...")

        try:
            async with self.session_maker() as session:
                async with session.begin():
                    result = await session.execute(select(Clusters).where(Clusters.id == cluster_id))
                    cluster = result.scalar_one_or_none()

                    if cluster is None:
                        logger.warning(f"Cluster with id {cluster_id} not found")
                        return None

                    data = self._to_dict(cluster)
                    await session.delete(cluster)

            logger.success(f"Cluster {cluster_id} deleted successfully")
            return data

        except IntegrityError as error:
            logger.error(f"Integrity error while deleting cluster {cluster_id}: {error}")
            raise

        except SQLAlchemyError as error:
            logger.error(f"Database error while deleting cluster {cluster_id}: {error}")
            raise

        except Exception as error:
            logger.critical(f"Unexpected error while deleting cluster {cluster_id}: {error}")
            raise