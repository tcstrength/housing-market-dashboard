import os
import sys
import dotenv
from loguru import logger
from pathlib import Path

def __get_project_root() -> Path:
    return Path(__file__).parent.parent.parent.parent

PROJECT_ROOT = __get_project_root()

print("Project Root:", PROJECT_ROOT)

if not dotenv.load_dotenv(
    dotenv_path=str(PROJECT_ROOT.joinpath(".env")),
    override=True
):
    logger.warning("Failed to load `.env`")

logger.remove()
logger.add(sys.stdout, level=os.getenv("LOG_LEVEL", "INFO"))

SELENIUM_REMOTE_URL = os.getenv("SELENIUM_REMOTE_URL")
POSTGRES_CONN = os.getenv("POSTGRES_CONN")
DATA_PATH = PROJECT_ROOT.joinpath(os.getenv("DATA_PATH"))