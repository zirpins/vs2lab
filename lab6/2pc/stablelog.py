import logging
import os


def create_log(name):
    """
    Create a persistent log (file) of protocol state
    :param name: some arbitrary name to identify the log output
    :return: logger object
    """
    logger = logging.getLogger(str(name))

    path = os.path.join(
        os.path.join(
            os.path.dirname(__file__),
            "stablelogs"),
        str(name) + ".log")

    logger.addHandler(logging.FileHandler(path))

    logger.setLevel(logging.INFO)

    return logger
