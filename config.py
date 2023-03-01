import os
import sys

from loguru import logger

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(ROOT_DIR, 'data.csv')
LOG_PATH = os.path.join(ROOT_DIR, 'logs')

TOP_OF_THE_BOOK_PRICE_COUNT = 4
ORDER_ID_FOR_QUEUE_POSITION_QUERY: int = 7427602921427632413
SHOW_FINAL_ORDER_BOOK: bool = False

FLOAT_SIGNIFICANT_DIGIT_FORMAT = "{0:.2f}"


def create_log_path():
    if os.path.exists(LOG_PATH):
        print(f"Logging path already exists. {LOG_PATH}")
    else:
        os.mkdir(LOG_PATH)
        print(f"Created logging path at {LOG_PATH}.")


def configure_logger():
    create_log_path()
    debug_file_path = os.path.join(LOG_PATH, "debug")
    logger.add(sys.stdout, format="{time} {level} {message}", filter="my_module", level="DEBUG")
    logger.add(debug_file_path, format="{time} {level} {message}", filter="my_module", level="DEBUG")
