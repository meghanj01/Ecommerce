import logging

# create the logger instance
logger = logging.getLogger("Ecommerce")

# set the log level for logger
logger.setLevel(logging.DEBUG)

# create a formatter to define log message format
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

# create a handler for debug messages (eg.debug.py)
debug_handler = logging.FileHandler(
    f"C:\\Users\\megha\\Git_projects\\logging\\debug.log"
)
debug_handler.setLevel(logging.DEBUG)
debug_handler.setFormatter(formatter)

# create a handler for error messages (eg. error.py)
error_handler = logging.FileHandler(
    f"C:\\Users\\megha\\Git_projects\\logging\\error.log"
)
error_handler.setLevel(logging.ERROR)
error_handler.setFormatter(formatter)

# add both the handlers
logger.addHandler(debug_handler)
logger.addHandler(error_handler)
