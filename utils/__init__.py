from functools import wraps


def return_self(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        func(self, *args, **kwargs)
        return self

    return wrapper
