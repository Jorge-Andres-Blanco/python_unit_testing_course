def sum(a,b):
    return a+b

def substract(a,b):
    return a-b


def divide(a,b):
    if b == 0:
        raise ValueError("Division por 0")
    return a/b