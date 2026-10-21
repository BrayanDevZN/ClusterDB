"Cria a engine do banco de dados"
from src.logs.log import logger
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine 
from sqlalchemy import text
class Connect:

    def __init__(self, url:str)-> None:
        self.url = url

    #Cria a engine
    async def _create(self) -> None:

        try:

            logger.info("Creating engine of database...")

            self.engine = create_async_engine(url=self.url)

            logger.success("Created engine with sucess")

        except Exception as error:

            logger.error(f"Error: {error}")
            raise  

    #Testa a conexão
    async def _test(self) -> None:

        countdown = 0

        while True:

            logger.info("Testing conection from database...")

            try:

                async with self.engine.begin() as session:

                    await session.execute(
                        text("Select 1;")
                    )


                logger.success("Connection ok!!")

                break 

            except Exception as error:

                if countdown != 3:

                    logger.warning(f"Error with connection, testing again...")
                    countdown +=1
                    continue

                logger.error(f"Error with connection from database: {error}")
                raise 

    #executa os metodos e retorna a engine
    async def run(self) -> AsyncEngine:

        await self._create()
        await self._test()
        

    





        
        