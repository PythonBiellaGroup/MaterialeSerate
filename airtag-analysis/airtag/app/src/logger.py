# REMEMBER:
# log early
# log often

import logging  # using standard library
import os


from logging.handlers import RotatingFileHandler

# from logging.handlers import TimeRotatingFileHandler

# using rich library
# from rich.logging import RichHandler

# Set the logs costants (You can use env var)
# -------------------------------------------------
# VERBOSITY = info as default, #debug for local dev
VERBOSITY = os.getenv("VERBOSITY", "debug")
LOG_PATH = os.getenv("LOG_PATH", "./logs")  # logs folder
LOGGER_FILENAME = "daemon.log"
FILE_TIME_WHEN = "D"  # Days
FILE_TIME_INTERVAL = 30
FILE_BACKUP_COUNT = 12  # Number of backup
FILE_MAX_BYTES = 100 * 1024 * 1024  # 100 MB
FILE_ENCODING = "utf-8"
FILE_DELAY = False

# shell formatter syntax
SHELL_FORMATTER_SYNTAX = "%(asctime)s (%(levelname)s) \t| %(message)s"
# file formatter syntax
FILE_FORMATTER_SYNTAX = "%(asctime)s (%(levelname)s) \t| [%(filename)s:%(funcName)s:%(lineno)d] \t| %(message)s"

# handler for file (make the folder if not exist)
if not os.path.exists(LOG_PATH):
    os.makedirs(LOG_PATH)
FILE_LOG_PATH = os.path.join(LOG_PATH, LOGGER_FILENAME)
# -------------------------------------------------

# Define the logger
logger = logging.getLogger(__name__)

# For your application you can just use this: from logger import logger
log_name = VERBOSITY.upper().strip()
log_level = logging.getLevelName(log_name)

# handler for shell
shell_handler = logging.StreamHandler()


# Rotating handler for file
# (Rotating = autodelete by space and backup number to avoid oversized logs)
file_handler = RotatingFileHandler(
    FILE_LOG_PATH,
    mode="a",
    maxBytes=FILE_MAX_BYTES,
    backupCount=FILE_BACKUP_COUNT,
    encoding=FILE_ENCODING,
    delay=FILE_DELAY,
)

# TimeRotating handler for file
# (TimeRotating = autodelete by time to avoid oversized logs)
# file_handler = logging.handlers.TimeRotatingFileHandler(
#     FILE_LOG_PATH,
#     when=FILE_TIME_WHEN,
#     interval=FILE_TIME_INTERVAL,
#     backupCount=FILE_BACKUP_COUNT,
#     encoding=FILE_ENCODING,
#     delay=FILE_DELAY,
# )

# beautiful log with rich library
# shell_handler = RichHandler()
# rich_fmt = "%(message)s"

if isinstance(log_level, int):
    # set the verbosity of the logs
    logger.setLevel(log_level)
    shell_handler.setLevel(log_level)
    file_handler.setLevel(log_level)
else:
    raise NotImplementedError(f"Logging level error: {log_name}")

# register the formatter with the formatter sintax
shell_formatter = logging.Formatter(SHELL_FORMATTER_SYNTAX)
file_formatter = logging.Formatter(FILE_FORMATTER_SYNTAX)

# set the formatter
shell_handler.setFormatter(shell_formatter)
file_handler.setFormatter(file_formatter)

# add the handler (to catch the logs)
logger.addHandler(shell_handler)
logger.addHandler(file_handler)


# Logger usage (by level)
# logger.debug("debug statement")
# logger.info("info statement")
# logger.warning("warning statement")
# logger.critical("critical statement")
# logger.error("error statement")
# logger.exception("exception statement")