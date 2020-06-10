'''
Marvin Lopez
Vladimir Semenov

Assignment 3
"Reflecting upon itself"

Python 3.8.0
'''

import inspect

def reflect(function):
    """ 
    It is considered a quine since this program takes no input, but it produces an output.
    Displaying its own source code
    """
    def wrapper(*args, **kwrd):
        print(inspect.getsource(function).replace("@reflect\n", ""))
    return wrapper


@reflect
def foo():
    print("bar")


if __name__ == "__main__":
    foo()
    
