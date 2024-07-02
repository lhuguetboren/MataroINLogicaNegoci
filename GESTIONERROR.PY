
class InvalidAgeException(Exception):
    "Raised when the input value is less than 18"
    print(Exception)
    pass


def exceptionABC(e):
    if e=="problema division por cero":
        print("lo de siempre")
    else:
        print("lo no de siempre")


try: 
    raise InvalidAgeException
    try:
        A = 1/0
    except ZeroDivisionError as e:
        raise TypeError("problema division por cero") from e       
except TypeError as e:
    exceptionABC('e')