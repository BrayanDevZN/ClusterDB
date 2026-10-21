"teste dos logs"
from src.logs.log import logger

def test_logs() -> None:

    loggers = [
        logger.info,
        logger.success,
        logger.warning,
        logger.debug,
        logger.error,
        logger.critical
    ]

    for log in loggers:

        log("Test")


if __name__ == "__main__":
    test_logs()