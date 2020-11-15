import logging


_log_format = "%(asctime)s - [%(levelname)s] - %(name)s - " \
              "(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"


def _get_stream_handler():
    """Ensure base handler for logger"""
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(logging.Formatter(_log_format))
    return stream_handler


def getLogger(name: str) -> str:
    """Ensure logger for logging purposes"""
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.addHandler(_get_stream_handler())
    return logger
