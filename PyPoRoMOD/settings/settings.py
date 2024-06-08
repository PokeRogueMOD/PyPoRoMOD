from pathlib import Path
import sys
from loguru import logger

LOG_FILE = False
LOG_LEVEL = "DEBUG"  # "INFO", "DEBUG"

_DIR = Path(__file__).resolve().parent

if LOG_LEVEL == "INFO":
    logger.remove()
    logger.add(
        sys.stdout,
        format=(
            "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
            "<level>{level: <8}</level> ㉿ "
            "<level>{message}</level>"
        ),
        level=LOG_LEVEL,
    )

if LOG_FILE:
    _FILE_DIR = _DIR.parent.parent / "log"
    _FILE_DIR.mkdir(parents=True, exist_ok=True)

    _FILE = _FILE_DIR / "PokeRogueMODLog.log"

    logger.add(
        _FILE,
        format=(
            "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
            "<level>{level: <8}</level> ㉿ "
            "<level>{message}</level>"
        ),
        level="DEBUG",
    )
