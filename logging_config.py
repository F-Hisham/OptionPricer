import logging

logging_level = logging.DEBUG
main_logger = logging.getLogger()
main_logger.setLevel(logging_level)

# Create a Formatter for formatting the log messages
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging_level)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
stream_handler.setFormatter(formatter)

main_logger.addHandler(stream_handler)
