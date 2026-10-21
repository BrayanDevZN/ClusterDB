"gera o hash de senha e compara"
from src.logs.log import logger 
import bcrypt

class Hash:

    #Gera o hash
    @staticmethod
    async def encode(password:str) -> str:

        try:

            logger.info("Creating hash password...")

            new_pass = bcrypt.hashpw(password=password.encode("utf-8"),
                                     salt=bcrypt.gensalt()).decode("utf-8")

            logger.success("hashed password created with success")

            return new_pass

        except Exception as error:

            logger.error(f"Error: {error}")
            raise 

    #Compara os hashs
    @staticmethod
    async def check(password:str, hashed_password:str) -> bool:

        try:

            logger.info("Checking password...")

            check = bcrypt.checkpw(hashed_password=hashed_password.encode("utf-8"), 
                                   password=password.encode("utf-8"))

            if check:
                logger.warning("Valid password")

            else:
                logger.success("Invalid password")

            return check

        except Exception as error:
            logger.error(f"Error: {error}")
            raise

            

    
    