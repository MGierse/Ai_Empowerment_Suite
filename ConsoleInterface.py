import logging

class MyFormatter(logging.Formatter):
    #format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    format = "%(message)s"

    FORMATS = {
        logging.DEBUG: "\033[0;37m" + format + "\033[0m",
        logging.INFO: "\033[0;36m" + format + "\033[0m",
        logging.WARNING: "\033[1;33m" + format + "\033[0m",
        logging.ERROR: "\033[1;31m" + format + "\033[0m",
        logging.CRITICAL: "\033[1;41m" + format + "\033[0m"
    }

    def format(self, record):
        log_format = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_format)
        return formatter.format(record)

# Logger konfigurieren
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Handler erstellen
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(MyFormatter())

# Handler zum Logger hinzufügen
logger.addHandler(ch)


