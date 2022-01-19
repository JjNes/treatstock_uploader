import logging

def setup_custom_logger(name):
    formatter = logging.Formatter(fmt='%(asctime)s - %(levelname)s - %(module)s - %(message)s')

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)


    file = logging.FileHandler("error.log")
    fileformat = logging.Formatter('%(asctime)s - %(levelname)s - %(module)s - %(message)s')
    file.setLevel(logging.ERROR)
    file.setFormatter(fileformat)

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)
    logger.addHandler(file)
    return logger