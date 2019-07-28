import logging
import config as config
import os

# LOGGING
logging.getLogger('discord').setLevel(logging.INFO)
logging.getLogger('discord.http').setLevel(logging.WARNING)

log_path = config.LOG_PATH

if not os.path.exists(log_path):
    os.makedirs(log_path)

logFormatter = logging.Formatter("[%(asctime)s] [%(module)s] [%(levelname)-5.5s]  %(message)s")
LOGGER = logging.getLogger('adbkraken')

fileHandler = logging.FileHandler("{0}/adbkraken.log".format(log_path))
fileHandler.setFormatter(logFormatter)
LOGGER.addHandler(fileHandler)

consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
LOGGER.addHandler(consoleHandler)
LOGGER.setLevel(level=logging.INFO)
