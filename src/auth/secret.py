from src.logs.log import logger
import secrets
import string

def generate_secret() -> str:

    logger.info("Generating secret...")

    chars = string.ascii_letters + string.digits
    value = "".join(secrets.choice(chars) for _ in range(32))

    logger.success("Generated secret with success")

    return value