from codestatlib import *

rc(multipage=true, filename='report.pdf', papersize='a4')

@report_object(output=False)
@report_complexity(operator=False, operands=False)

def foo():
    print("hello")


if __name__ == "__main__":
    foo()