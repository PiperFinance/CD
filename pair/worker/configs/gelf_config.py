import os
import logging
from pygelf import GelfUdpHandler


def config(
        logger,
        app_name,
        GELF_STATUS=None,
        GRAYLOG_HOST=None,
        GRAYLOG_PORT=None,
        level=logging.INFO):
    logging.basicConfig(
        format='%(asctime)s:%(levelname)s:%(message)s',
        datefmt='%m/%d/%Y %I:%M:%S %p',

        level=level)

    if GELF_STATUS or os.getenv("GRAYLOGGER_ENABLE"):
        gray_log_host = GRAYLOG_HOST or os.getenv("GRAYLOG_HOST")
        logger = logging.getLogger()
        handler_to_remove = []
        for handler in logger.handlers:
            if isinstance(handler, GelfUdpHandler):
                handler_to_remove.append(handler)
        for handler in handler_to_remove:
            logger.removeHandler(handler)
        logger.addHandler(
            GelfUdpHandler(
                host=gray_log_host,
                port=GRAYLOG_PORT or 12201,
                _app_name=app_name)
        )
        logger.setLevel(level)

    return logger
