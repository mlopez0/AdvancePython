'''
Marvin Lopez
Vladimir Semenov

Assignment 3
"Reflecting upon itself"

Python 3.8.0
'''

import inspect
from io import StringIO 
import sys

class Capturing(list):
    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = self._stringio = StringIO()
        return self
    def __exit__(self, *args):
        self.extend(self._stringio.getvalue().splitlines())
        del self._stringio    # free up some memory
        sys.stdout = self._stdout

def reflect(function):

    def wrapper(*args, **kwrd):
        positional_args = []
        keyworded_args = []

        print("Name:\t", function.__name__)
        print("Type:\t", type(function))
        print("Sign:\t", inspect.signature(function))
        print()
        print("Args:", end="")
        if locals()['args']:
            print("\tpositional", locals()['args'])
        if locals()['kwrd']:
            print("\tkey=worded", locals()['kwrd'])
        print()
        print("Doc:", end="")
        for line in function.__doc__.split('\n')[1:]:
            print("\t", line.strip())

        print("Complx:", end="")
        counter = 0
        sub = "print"
        for line in inspect.getsourcelines(function)[0]:
            counter = counter + line.count(sub)
        print ( "\t"+'{\''+sub+'\'}: '+ str(counter))

        print("Source:", end="")
        for line in inspect.getsourcelines(function)[0]:
            print("\t", line)

        print("Output:", end="")
        with Capturing() as output:
            function(*args, **kwrd)

        for line in output:
            print("\t", line)

    return wrapper

@reflect
def foo(bar1, bar2=""):
    """
    This function does nothing useful
    :param bar1: description
    :param bar2: description
    """
    print("some\nmultiline\noutput")

if __name__ == "__main__":
    foo(None, bar2="")
    
