import sys


def validate_post_size(value: str) -> str:
    if sys.getsizeof(value) > 1024**2:
        raise ValueError('Value is too big!')

    return value
