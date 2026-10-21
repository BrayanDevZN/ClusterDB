"Cria o session manage"
from src.logs.log import logger 
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession, AsyncEngine

def get_session(engine:AsyncEngine) -> AsyncSession:

    try:
        logger.info("Creating session make...")

        session =  async_sessionmaker(
            engine,
            expire_on_commit=False
        )

        logger.success("Created with sucess")

        return session

    except Exception as error:

        logger.error(f"Error: {error}")
        raise
    

    

