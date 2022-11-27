from nanoid import generate


def nano_id():
    return generate(
        '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz',
        size=12)
