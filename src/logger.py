import logging
from pathlib import Path


LOG_FILE = Path("logs/pipeline.log")


def setup_logger():
    """
    Configure the application logger.
    """

    LOG_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    logging.basicConfig(
        filename=LOG_FILE,
        level=logging.INFO,
        format=(
            "%(asctime)s | "
            "%(levelname)s | "
            "%(message)s"
        )
    )

    return logging.getLogger("trade_pipeline")