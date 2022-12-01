import logging


class Logger:
    def __init__(self, logName, loggerName):
        # Set logger
        self.mLogger = logging.getLogger(logName)
        # Set log's level
        self.mLogger.setLevel(logging.INFO)
        # Set log's format
        self.mFormatter = logging.Formatter("[%(asctime)s-%(name)s-%(levelname)-08s] %(message)s")
        # Set log name
        self.mLoggerName = loggerName
        self.SetHandler()

    def SetHandler(self):
        file_handler = logging.FileHandler(self.mLoggerName)
        file_handler.setFormatter(self.mFormatter)
        self.mLogger.addHandler(file_handler)

    def PrintLog(self, string):
        self.mLogger.info(string)