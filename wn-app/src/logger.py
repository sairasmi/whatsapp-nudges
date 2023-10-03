import logging
from logging.handlers import TimedRotatingFileHandler
from whatsappnudge.utils import create_folder
from config import settings

# initiate logger only one time
def initiate_logger_old(path):
    logger = logging.getLogger("WN-APP ")
    logger.setLevel(logging.DEBUG)

    handler = TimedRotatingFileHandler(path, when="m", interval=1, backupCount=0)
    logger.addHandler(handler)

    return logger


# initiate logger only one time
def initiate_logger(path):
    # create logger folder
    create_folder(path)

    # file path for log
    file_path = f'{path}/nudges.log'


    fmt = '%(asctime)s %(filename)s [line:%(lineno)d] %(levelname)s %(message)s'
    formatter = logging.Formatter(fmt=fmt, datefmt='%d/%m/%Y %H:%M:%S')

    handler = TimedRotatingFileHandler(file_path, when=settings.LOGGER_INTERVAL_UNIT, interval=settings.LOGGER_INTERVAL_VALUE, backupCount=settings.LOGGER_BACKUP_COUNT)
    handler.setFormatter(formatter)

    logger = logging.getLogger("WN-APP ") # or pass string to give it a name
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)

    logger.debug("Timeline Logger::Initiated")

    return logger



log = initiate_logger("../logs/")