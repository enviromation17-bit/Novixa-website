import logging

# Create logger
logger = logging.getLogger("novixa")
logger.setLevel(logging.INFO)

# Prevent duplicate logs
if not logger.handlers:

    # Console output
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # File output
    file_handler = logging.FileHandler("logs/novixa.log")
    file_handler.setLevel(logging.INFO)

    # Log format
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s"
    )

    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)