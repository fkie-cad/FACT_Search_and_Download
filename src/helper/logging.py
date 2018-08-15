import logging


def _get_log_level(debug_flag):
    if debug_flag:
        return logging.DEBUG
    else:
        return logging.INFO


def setup_logging(debug_flag):
    log_format = logging.Formatter(fmt='[%(asctime)s][%(module)s][%(levelname)s]: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    console_log = logging.StreamHandler()
    console_log.setLevel(_get_log_level(debug_flag))
    console_log.setFormatter(log_format)
