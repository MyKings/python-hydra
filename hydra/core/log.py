# coding: utf-8

import logging
import sys

logger = logging.getLogger("hydra")
logger_handler = logging.StreamHandler(sys.stdout)
FORMATTER = logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s", "%H:%M:%S")
FORMATTER_DEV = logging.Formatter("[%(asctime)s] [%(pathname)s(%(lineno)d)%(funcName)s()] [%(levelname)s] %(message)s", "%H:%M:%S")
logger_handler.setFormatter(FORMATTER_DEV)
logger_handler.setFormatter(FORMATTER)
logger.addHandler(logger_handler)
logger.setLevel(logging.INFO)
