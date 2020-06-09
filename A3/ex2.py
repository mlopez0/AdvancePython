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


def print_multiline_cell(lines, strip_line = False):
    for line in lines:
        line = line if not strip_line else line.strip()
        print("\t", line.replace("\n",""))
    print()


def print_multiline_row(label, lines, strip_line=False):
    print(label + ":", end="")
    print_multiline_cell(lines, strip_line)


def reflect(function):

    def wrapper(*args, **kwrd):
        with Capturing() as output:
            function(*args, **kwrd)

        print("Name:\t", function.__name__)
        print("Type:\t", type(function))
        print("Sign:\t", inspect.signature(function), end="\n\n")
        
        print("Args:", end="")

        if locals()['args']:
            print("\tpositional", locals()['args'])
        if locals()['kwrd']:
            print("\tkey=worded", locals()['kwrd'])

        print()

        print_multiline_row("Doc", function.__doc__.split('\n')[1:-1], True)
        print_multiline_row("Source", inspect.getsourcelines(function)[0])
        print_multiline_row("Output", output)

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
