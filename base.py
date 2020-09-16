import logging


class Base:
    """
    There should be LogMixIn for Base class
    As there is no common functionality in Base - logging is implemented here
    """
    def __init__(self):
        # TODO: add params for logging
        self.logger = logging
        self.set_level()

    def set_level(self):
        # TODO: add all levels
        self.logger.basicConfig(level=logging.DEBUG)

    def debug_info(self, message, data=None):
        if data:
            message = message + ': {}'.format(data)
        self.logger.debug(message)
