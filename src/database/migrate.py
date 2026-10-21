"Executa migração"
from src.logs.log import logger
from .base import Base 
from .models.users import Users
from .models.keys import keys
from .models.clusters import Clusters
from .models.instances import Instances
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy import text
class MakeMigrate:

    def __init__(self, engine:AsyncEngine)-> None:

        self.engine = engine 

    #Cria as tabelas
    async def create_tables(self) -> None:

        try:

            logger.info("Creating tables if not exists...")

            async with self.engine.begin() as session:
                await session.run_sync(Base.metadata.create_all)

            logger.success("Tables created with success")

        except Exception as error:

            logger.error(f"Error: {error}")
            raise 

    #Reseta os dados das tabelas
    async def reset_tables(self) -> None:

        try:

            logger.info("Reseting tables...")

            async with self.engine.begin() as session:

                await session.run_sync(Base.metadata.drop_all)
                await session.run_sync(Base.metadata.create_all)

            logger.success("Tables reseted")

        except Exception as error:
            logger.error(f"Error: {error}")
            raise

    #Deleta as tabelas
    async def delete_tables(self) -> None:

        try:

            logger.info("Droping tables...")

            async with self.engine.begin() as session:

                await session.run_sync(Base.metadata.drop_all)

            logger.success("Droped tables")

        except Exception as error:
            logger.error(f"Error: {error}")
            raise

        

    