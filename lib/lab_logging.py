import logging


def setup(stream_level=logging.WARNING, file_level=logging.DEBUG, file_postfix=''):
    # create logger with 'vs2lab'
    logger = logging.getLogger('vs2lab')
    logger.setLevel(logging.DEBUG)

    # create file handler which logs even debug messages
    fh = logging.FileHandler('vs2lab' + file_postfix + '.log')
    fh.setLevel(file_level)

    # create console handler which logs even debug messages
    ch = logging.StreamHandler()
    ch.setLevel(stream_level)

    # create formatter and add it to the handlers
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    # add the handlers to the logger
    logger.addHandler(fh)
    logger.addHandler(ch)
