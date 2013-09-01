import logging
import logging.config

logging.config.fileConfig("scripts/log.conf")
logger = logging.getLogger("Tornado")
logger.debug('debug message')
logger.info('info message')
logger.warn('warn message')
logger.error('error message')
logger.critical('critical message')
