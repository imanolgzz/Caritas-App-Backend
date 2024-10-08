import logging
import logging.handlers

# Logging (remember the 5Ws: “What”, “When”, “Who”, “Where”, “Why”)
LOG_PATH = './../logs'
LOGFILE = LOG_PATH  + '/Caritas_api.log'
logformat = '%(asctime)s.%(msecs)03d %(levelname)s: %(message)s'
formatter = logging.Formatter(logformat, datefmt='%d-%b-%y %H:%M:%S')
loggingRotativo = False
DEV = True

if loggingRotativo:
    # Logging rotativo
    LOG_HISTORY_DAYS = 3
    handler = logging.handlers.TimedRotatingFileHandler(
            LOGFILE,
            when='midnight',
            backupCount=LOG_HISTORY_DAYS)
else:
    handler = logging.FileHandler(filename=LOGFILE)

handler.setFormatter(formatter)
my_logger = logging.getLogger("Caritas_api")
my_logger.addHandler(handler)

if DEV:
    my_logger.setLevel(logging.DEBUG)
else:
    my_logger.setLevel(logging.INFO)

LOGGER = my_logger