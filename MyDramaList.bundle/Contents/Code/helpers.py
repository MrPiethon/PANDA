# This builtin function doesn't seem to exist in RestrictedPython
# implementation from https://docs.python.org/2.7/library/functions.html#any
def any(iterable):
    for element in iterable:
        if element:
            return True
    return False
