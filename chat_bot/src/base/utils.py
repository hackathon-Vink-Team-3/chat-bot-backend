from functools import wraps


def log_exceptions(logger):
    """Логировать все ошибки как критические."""

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logger.critical(e)

        return wrapper

    return decorator
