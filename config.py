import logging
import os

logger = logging.getLogger(__name__)


def get_current_environment() -> str:
    env = os.environ.get("ENV", "DEV")
    logger.info(f"Current environment is {env}")
    print(f"env is :{env}")
    return env


ENV = get_current_environment()
