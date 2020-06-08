'''
Marvin Lopez
Vladimir Semenov

Assignment 3
"Reflecting upon itself"

Python 3.8.0
'''


print (open(__file__).read()) # smallest python program that can print its own source code but it is not a quine because a quine should not use open() function to print out its source code.


def foo():
    print("bar")
    
if __name__ == "__main__":
    foo()
    
