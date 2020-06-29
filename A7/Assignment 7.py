### Python Programming for Software Engineers
### Assignment 7
### 'Lambda De Parser'

# Marvin Lopez
# Vladimir Semenov

# Task 1
# ----------------------------------------------
# Given the following:
f = lambda x, y: x * y

# 1. Rewrite to its logical equivalence using ordinary funcion definition(s)
def f(x, y):
    return x * y


# Task 2
# ----------------------------------------------
# Given the following:
f = lambda x: (lambda y: (lambda z: x + y + z))

# 1. How would you call it to get the result of `x + y + z`?
x = 1
y = 2
z = 3
f(x)(y)(z)

# 2. Rewrite it using only one lambda expression and show how to call it
f = lambda x, y, z: x + y + z
f(x, y, z)


# Task 3
# ----------------------------------------------
# Given the following:
(lambda b = (lambda *c: print(c)): b("a", "b"))()

# 1. What happens here? Rewrite it so that the code can be 
# understood by a normal or your mate who has no idea what the lambda is! 
# Provide comments, neat formatting and a bit more meaningful var names.

def printer(function):
    def wrapper(*args):
        print(args)
    
    return wrapper

@printer
def b(*args):
    pass

b("a", "b")


# Task 4 (soft)
# ----------------------------------------------
# What are the main restrictions on the lambda?
# - The main limitation of lambda expression is they can contain only a single expression 
#   and this expression has to be written on a single line
#
# Provide "If yes, why? If not, why not?" for each of the following:
#
# 1. Does lambda restrict side effects?
#   Yes, lambdas is that they cannot contain anything besides an expression. 
#   It's nearly impossible for a lambda expression to produce anything besides trivial side effects, 
#   since it cannot have anywhere near as rich a body as a "def" function.
#
# 2. Does lambda restrict number of allowed statements?
# - Yes, It is not possible to have multiples statements in lambda
#
# 3. Does lambda restrict assignments? 
# - Yes, Assignment statements cannot be used in lambda. In Python, 
#   assignment statements don’t return anything, not even None (null).
# 
# 4. Does lambda restrict number of return values?
# - Yes, lambda can't return complex statements, only expressions
#   >>> lambda: if True: 0
#     File "<stdin>", line 1
#       lambda: if True: 0
#                ^
#   SyntaxError: invalid syntax
#
# 5. Does lambda restrict the use of default arguments values? 
# - Yes, One or more variables appearing in the expression may be declared previously. 
#   But if it’s there in the arguments, either it should have a default value or must be passed as an argument to the call.
#    >>> a,b=1,2
#    >>> y=lambda a,b:a+b
#    >>> y()
#Traceback (most recent call last):
#    File “<pyshell#167>”, line 1, in <module>
#    y()
#    TypeError: <lambda>() missing 2 required positional arguments: ‘a’ and ‘b’
#
# 6. Does lambda restrict possible function signatures?
# - No, Lambda's take the same signature as regular functions

# Task 5
# ----------------------------------------------
# Given the following:
(lambda f = (lambda a: (lambda b: print(list(map(lambda x: x+x, a+b))))): 
f((1,2,3))((4,5,6)))()

# 1. What happens here? Do the same as in Task 3 and
# enumerate order of execution using (1,2,3...) in comments

def func_a(a):
    def func_b(b):                          # 3
        def lmab_f(x):                      # 5
            return x + x                    # 7
        print(list(map(lmab_f, a + b)))     # 6

    return func_b                           # 4

def full_func(f=func_a):
    return f((1, 2, 3))((4, 5, 6))          # 2

full_func()                                 # 1

# 2. Why does map() requires list() call?
#   Because it returns an iterator, it omit storing the full size list in the memory. 
#   So that you can easily iterate over it in the future not making any pain to memory. 
#   Possibly a full list is not even needed, but the part of it, until the condition is reached.
