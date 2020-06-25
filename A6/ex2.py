storage = []

def throw_error():
    return 'err: invalid expression'
    # get_input()


def is_digit(symbol):
    """
    Returns true if char is digit
    """
    for char in symbol:
        if not (ord(char) >= 48 and ord(char) <= 56):
            return False
    return True


def get_result(result,candidate):
    if is_digit(candidate):
        return candidate
    
    return str(result) + ('+ ' + candidate) if candidate[0] != '-' else ('- ' + candidate)


def fill_zeros(a, b):
    start = max(len(a), len(b)) - 1
    end = min(len(a), len(b)) - 2
    diff = start - end - 1
    zeros = '0' * diff if diff > 0 else ''

    if len(a) < len(b):
        a = zeros + a
    elif len(b) < len(a):
        b = zeros + b
    
    return a, b


def remove_zeros(symbol):
    for i, char in enumerate(symbol):
        if char != '0':
            return symbol[i:]

    return '0'


def remove_neg(a,b):
    # print(a, b)
    a = a if a[0] != '-' else a[1:]
    b = b if b[0] != '-' else b[1:]

    return a, b


def subtract(a, b):
    # print(a, '-', b, '=', end=' ')
    result = []
    decimal = 0
    
    a, b = remove_neg(a, b)    
    a, b = fill_zeros(a, b)

    negative = int(a) < int(b)

    for i in range(max(len(a), len(b)) - 1, -1, -1):
        x, y = (int(a[i]), int(b[i])) if not negative else (int(b[i]), int(a[i]))
        
        interim = x - decimal - y if x >= y else 10 + x - decimal - y
        if x < y: decimal = 1
        if interim < 0: interim = 0

        result.append(str(interim))

    return ('-' if negative else '')  + remove_zeros(''.join(reversed(result))) 


def add(a, b):
    result = []
    decimal = '0'

    a,b = remove_neg(a, b)
    a, b = fill_zeros(a, b)

    for i in range(max(len(a), len(b)) - 1, -1, -1):
        interim = str(int(a[i]) + int(b[i]) + int(decimal))
        result.append(interim[-1])
        decimal = str(interim)[:-1] if len(str(interim)) > 1 else '0'
    
    if decimal != '0':
        result.append(decimal)

    return ''.join(reversed(result))


def operate(a, b, operator):
    neg = int(a) < 0 or int(b) < 0
    both_neg = int(a) < 0 and int(b) < 0

    only_b_neg = int(b) < 0 and not int(a) < 0
    only_a_neg = not int(b) < 0 and int(a) < 0

    # print(a, b, operator)
    
    if (operator == '+' and not neg) or (only_b_neg and operator == '-'):
        return add(a, b)
    elif (operator == '+' and both_neg) or (only_a_neg and operator == '-'):
        return '-' + add(a, b)
    elif (operator == '-' and both_neg) or (only_a_neg and operator == '+'):
        return subtract(b, a)
    elif (operator == '-' and not neg) or (only_b_neg and operator == '+'):
        return subtract(a, b)

    return throw_error()


# def add(symbol, operator):
#     return symbol if operator == 1 else -symbol


def solve_symbols(symbols):
    result = 0
    str_result = ''
    operator = 1
    variables = []

    for symbol in symbols:
        try:
            symbol = symbol
            # result += add(symbol, operator)
            result = int(operate(str(result), symbol, '+' if operator == 1 else '-'))
            continue
        except ValueError:
            pass

        if symbol[0] == '[' and symbol[-1] == ']':
            symbol = symbol[1:-1]

            if is_digit(symbol) and int(symbol) < len(storage):
                result = int(operate(str(result), str(storage[int(symbol)]), '+' if operator == 1 else '-'))

        elif symbol in ['+', '-']:
            operator = 1 if symbol == '+' else -1

        else:
            return throw_error()
    
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
    if str(result).startswith('err:'):
        return result
    storage.append(result)
    
    # print(str(len(storage)-1) + ': ', storage[-1])
    # print(storage)
    return str(len(storage)-1) + ': ' + str(storage[-1])
    
    # get_input()


def get_input():
    print('>>> ', end='')
    expression = input()
    parse_brackets(expression)

# get_input()

# print(operate('-1', '2', '+'))
# print(subtract('2', '1'))


# TODO: Remove test
expressions2 = {
    "2 + 2": "0: 4",
    "6 + [0]": "1: 10",
    "-1 - (2 + 4)": "2: -7",
    "-1 - 2 + 4": "3: 1",
    "1 + -1": "4: 0",
    "2+2": "err: invalid expression"
}

for expression, result in expressions2.items():
    real = parse_brackets(expression)
    # print(real == result, '\t', expression, '=\t', result[:6], '\t< ', real[:6])
    print(real == result)
