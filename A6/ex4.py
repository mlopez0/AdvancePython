import sys

_nparam = len(sys.argv)

def check_arguments():
    if _nparam==2:
        if sys.argv[1] == "-h":
            print("This program support the following operations:")
            print("\t - Addition \n \t - Subtraction")
            exit()

check_arguments()

storage = []

def throw_error():
    print('err: invalid expression')
    get_input()

def empty_input(expression): # Empty string validator
    if expression.strip():
        return True

def is_digit(symbol):
    """
    Returns true if char is digit
    """
    for char in symbol:
        if not (ord(char) >= 48 and ord(char) <= 56):
            return False
    return True

def is_variable(symbol):
    char = symbol[0]
    return (ord(char) <= 122 and ord(char) >= 97) or (ord(char) <= 90 and ord(char) >= 65)


def get_result(result,candidate):
    if is_digit(candidate):
        return candidate
    
    return str(result) + ('+ ' + candidate) if candidate[0] != '-' else ('- ' + candidate)


def add(symbol, operator):
    return symbol if operator == 1 else -symbol


def solve_symbols(symbols):
    result = 0
    str_result = ''
    operator = 1
    variables = []

    for symbol in symbols:
        try:
            symbol = int(symbol)
            result += add(symbol, operator)
            continue
        except ValueError:
            pass

        if symbol[0] == '[' and symbol[-1] == ']':
            symbol = symbol[1:-1]

            if is_digit(symbol) and int(symbol) < len(storage):
                result += add(storage[int(symbol)], operator)

        elif symbol in ['+', '-']:
            operator = 1 if symbol == '+' else -1

        else:
            throw_error()
    
    return result


def parse_string(string):
    symbols = string.split(' ')
    return solve_symbols(symbols)


def parse_brackets(string): 

    brackets_start = 0

    while True:
        brackets_start = string.find('(', brackets_start)
        if brackets_start == -1:
            break

        brackets_end = string.find(')', brackets_start) 
        # print(string[brackets_start + 1:brackets_end])
        string = string[:brackets_start] + str(parse_string(string[brackets_start + 1:brackets_end])) + string[brackets_end+1:]

    result = parse_string(string)
    storage.append(result)
    
    print(str(len(storage)-1) + ': ', storage[-1])
    # print(storage)
    get_input()

def multiplication(a, b):
    if a == 0 or b == 0:
        return 0
    else:
        if a < 0 and b > 0:
            return a + multiplication(a, b - 1)
        elif a < 0 and b < 0:
            return -b + multiplication(-a - 1, -b)
        else:
            return b + multiplication(a - 1, b)

def get_input():
    print('>>> ', end='')
    expression = input()

    if not empty_input(expression):
        get_input()

    parse_brackets(expression)

get_input()