"le e salva arquivos com pyspark em parquet"

from src.logs.log import logger 
from pyspark.sql import SparkSession, DataFrame
from pathlib import Path
import os
import shutil


class SparkFile:

    def __init__(self, session:SparkSession, path:str) -> None:

        self.session = session
        path = path if ".parquet" in path else path + ".parquet"
        self.BASE_DIR = Path(__file__).resolve().parent.parent.parent / path


    #Le o arquivo
    async def read(self) -> DataFrame|None:

        try:
            logger.info(f"Reading {self.BASE_DIR}...")

            if not os.path.exists(self.BASE_DIR):
                logger.warning(f"Not Found {self.BASE_DIR}")
                return None 

            df = self.session.read.parquet(str(self.BASE_DIR))

            logger.info(f"{self.BASE_DIR} read with success")

            return df 

        except Exception as error:
            logger.error(error)
            raise


    #Salva o arquivo
    async def write(self, data:DataFrame) -> None:

        try:
            logger.info(f"Saving data in {self.BASE_DIR}...")

            data.write.parquet(str(self.BASE_DIR))

            logger.success(f"{self.BASE_DIR} saved")

        except Exception as error:
            logger.error(f"Error: {error}")
            raise


    #Confere se a instancia existe
    async def exists(self) -> bool:

        exists = os.path.exists(self.BASE_DIR)

        logger.info(f"Path {self.BASE_DIR} {'not' if not exists else ''} exists")

        return exists 


    #Deleta instancia(s)
    async def drop_instances(self, rm_all:bool=False) -> None:

        if rm_all:
            path = self.BASE_DIR.parent

            for parquet in path.glob("*.parquet"):
                if parquet.is_dir():
                    shutil.rmtree(parquet)
                else:
                    parquet.unlink()

            logger.info(f"Deleted all parquets from {path}")
            return

        if self.BASE_DIR.exists():
            if self.BASE_DIR.is_dir():
                shutil.rmtree(self.BASE_DIR)
            else:
                self.BASE_DIR.unlink()

            logger.info(f"Deleted {self.BASE_DIR}")


    #Deleta o cluster
    async def drop_cluster(self) -> None:

        path = self.BASE_DIR.parent

        if not path.exists():
            logger.warning(f"Cluster not found {path}")
            return

        shutil.rmtree(path)

        logger.info(f"Deleted cluster {path}")


        