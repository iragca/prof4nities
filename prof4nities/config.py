import os
import pathlib
from enum import Enum

from dotenv import load_dotenv
from loguru import logger

from .utils import check_env_variable


class DirectoryPaths(Enum):
    PROJECT_ROOT = pathlib.Path(__file__).resolve().parent.parent
    ENV_FILE = PROJECT_ROOT / ".env"
    DATA = PROJECT_ROOT / "data"
    EXTERNAL_DATA = DATA / "external"


_PROJECT_ROOT = DirectoryPaths.PROJECT_ROOT.value
_DATA_DIR = DirectoryPaths.DATA.value
_ENV_FILE = DirectoryPaths.ENV_FILE.value

if _ENV_FILE.exists():
    load_dotenv(dotenv_path=_ENV_FILE)
    logger.info(f"Loaded environment variables from {_ENV_FILE}")


class Environment(Enum):
    """Settings class to hold environment variables."""

    # Example:
    DATABASE_URL = os.getenv("DATABASE_URL")


required_env_vars = []
non_essential_env_vars = []

for var in required_env_vars:
    value = os.getenv(var)
    check_env_variable(value, var, important=True)

for var in non_essential_env_vars:
    value = os.getenv(var)
    check_env_variable(value, var)


# Log key paths
logger.info(f"PROJECT_ROOT: {_PROJECT_ROOT}")
logger.info(f"DATA_DIR: {_DATA_DIR}")
