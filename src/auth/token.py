"Gera e compara jwt"
from src.logs.log import logger
import jwt

class JWT:

    def __init__(self, secret:str)-> None:

        self.secret = secret
        self.alg = "HS256"


    #gera o token jwt
    async def generate(self, payload:dict) -> str:

        try:

            logger.info("Generating token...")

            token = jwt.encode(
                payload=payload,
                algorithm=self.alg,
                key=self.secret
            )

            logger.success("Token generated with success")

            return token 

        except Exception as error:
            logger.error(f"Error: {error}")
            raise 

    #Descriptografa o token
    async def decode(self, token:str) -> dict:

        try:

            logger.info("Decoding token...")

            payload = jwt.decode(
                jwt=token,
                algorithms=self.alg,
                key=self.secret
            )

            logger.success("token decoded with success")

            return payload
        except Exception as error:
            logger.error(f"Error: {error}")
            raise 

        