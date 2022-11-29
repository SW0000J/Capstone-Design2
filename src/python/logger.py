import logging


class Logger:
    def __init__(self, logName):
        # Set logger
        self.mLogger = logging.getLogger()
        # Set log's level
        self.mLogger.setLevel(logging.INFO)
        # Set log's format
        self.mFormatter = logging.Formatter("[%(asctime)s-%(name)s-%(levelname)s] %(message)s")
        # Set log name
        self.mLogName = logName
        self.SetHandler()

    def SetHandler(self):
        file_handler = logging.FileHandler(self.mLogName)
        file_handler.setFormatter(self.mFormatter)
        self.mLogger.addHandler(file_handler)

    def PrintLog(self, string):
        self.mLogger.info(string)