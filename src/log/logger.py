# pylint: disable=line-too-long
"""
Logging Module
"""
import logging
import sys
import inspect
import traceback
from logging import DEBUG
from enum import Enum, unique


@unique
class Color(Enum):
    """A class for terminal color codes."""

    BOLD = "\033[1m"
    BLUE = "\033[94m"
    WHITE = "\033[97m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    LIGHT_PURPLE = "\033[5;202m"
    PURPLE = "\033[95m"
    LIME = "\033[96m"
    ORANGE = "\033[38;5;215m"
    ORANGE_BOLD = "\033[38;5;214m"
    DARKGREY = "\033[90m"
    MAROON = "\033[38;5;52m"
    LIGHTBLUE = "\033[38;5;51m"
    DARK_YELLOW = "\033[38;5;11m"
    JADE = "\033[38;5;35m"
    LIGHT_RED = "\033[38;5;9m"
    BOLD_WHITE = BOLD + WHITE
    BOLD_BLUE = BOLD + BLUE
    BOLD_GREEN = BOLD + GREEN
    BOLD_YELLOW = BOLD + YELLOW
    BOLD_RED = BOLD + RED
    BOLD_LIME = BOLD + LIME
    END = "\033[0m"

    def format(self, text):
        return f"{self.value}{text}{Color.END.value}"


class Logs:
    format = "%(asctime)s | %(levelname)-8s | %(function)-40s | %(message)s"
    format_date = "%Y-%m-%d %H:%M:%S"
    console_formatter = logging.Formatter(format, datefmt=format_date)
    console_logger = logging.StreamHandler(sys.stdout)
    console_logger.setFormatter(console_formatter)
    logger = logging.getLogger("pixitrend")
    logger.setLevel(level=DEBUG)
    logger.addHandler(console_logger)
    log_file = logging.FileHandler("logs.log")
    log_file.setFormatter(console_formatter)
    logger.addHandler(log_file)

    def __init__(self, level=DEBUG):
        self.extra = {
            "function": None,
        }
        self.level = level

    def info(self, msg):
        self.set_function_name()
        self.logger.info(msg, extra=self.extra)

    def error(self, msg):
        self.set_function_name()
        _, _, tb = sys.exc_info()
        try:
            _, _, funname, line = traceback.extract_tb(tb)[-1]
            debug = f"function = {funname} -- codeline = {line}"
            self.logger.error(f"{debug} -- msg = {msg}", extra=self.extra)
        except Exception:
            self.logger.error(msg, extra=self.extra)

    def debug(self, msg):
        self.set_function_name()
        self.logger.debug(msg, extra=self.extra)

    def warn(self, msg):
        self.set_function_name()
        self.logger.warn(msg, extra=self.extra)

    def set_function_name(self):
        # Get call function's name
        func = inspect.currentframe().f_back.f_back.f_code
        self.extra["function"] = Color.JADE.format(func.co_name)
