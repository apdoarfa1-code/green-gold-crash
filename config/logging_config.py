import logging
import sys
from config.settings import get_settings


def setup_logging():
    settings = get_settings()
    log_level = logging.DEBUG if settings.debug else logging.INFO

    log_format = (
        "%(asctime)s [%(levelname)s] %(name)s (%(filename)s:%(lineno)d) - %(message)s"
    )

    logging.basicConfig(
        level=log_level,
        format=log_format,
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )

    # Silence noise from external libraries
    logging.getLogger("asyncio").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("playwright").setLevel(logging.WARNING)


setup_logging()
logger = logging.getLogger("green_gold")
