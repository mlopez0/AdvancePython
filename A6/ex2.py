storage = []

def throw_error():
    print('err: invalid expression')
    get_input()


def is_digit(symbol):
    """
    Returns true if char is digit
    """
    for char in symbol:
        if not (ord(char) >= 48 and ord(char) <= 56):
            return False
    return True


def solve_symbols(symbols):
    result = 0
    operator = 1

    # print(symbols)
    for symbol in symbols:
        if is_digit(symbol) or (symbol.startswith('-') and is_digit(symbol[1:]) and not symbol=='-'):
            # print("DIGIT", symbol)
            if symbol.startswith('-'):
                operator *= -1
                symbol = symbol[1:]
            result += operator * int(symbol)
            operator = 1
        elif symbol[0] == '[' and symbol[-1] == ']':
            symbol = symbol[1:-1]
            if is_digit(symbol) and int(symbol) < len(storage):
                result += operator * storage[int(symbol)]

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
        brackets_start = string.find('(', brackets_start+1)

        if brackets_start == -1:
            break

        brackets_end = string.find(')', brackets_start+1) 
        string = string[:brackets_start] + str(parse_string(string[brackets_start + 1:brackets_end])) + string[brackets_end+1:]

    result = parse_string(string)
    storage.append(result)
    
    print(str(len(storage)-1) + ':', storage[-1])
    # print(storage)
    get_input()


def get_input():
    expression = input()
    parse_brackets(expression)

get_input()