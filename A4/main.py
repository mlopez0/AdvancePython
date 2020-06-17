import enums

file = open('test.py', 'r')
code = file.read()
print(code)
print()

end = len(code)


def is_letter(char):
    """
    Returns false if char is letter
    """
    return (ord(char) <= 122 and ord(char) >= 97) or (ord(char) <= 90 and ord(char) >= 65)


def is_digit(char):
    """
    Returns true if char is digit
    """
    return ord(char) >= 48 and ord(char) <= 56


class classes:
    IDENTIFIER = 'indentifier'
    DELIMITER = 'delimiter'
    OPERATOR = 'operator'
    LITERAL = 'literal'
    COMMENT = 'comment'
    INDENT = 'indent'
    DEDENT = 'dedent'
    NEWLINE = 'newline'
    KEYWORD = 'keyword'
    BLOCK = 'block'
    STRING = 'string'


state = {
    classes.IDENTIFIER: False,
    classes.DELIMITER: False,
    classes.OPERATOR: False,
    classes.LITERAL: False,
    classes.COMMENT: False,
    classes.INDENT: False,
    classes.KEYWORD: False,
    classes.BLOCK: False,
    classes.STRING: False
}

tokens = {
    classes.IDENTIFIER: False,
    classes.DELIMITER: False,
    classes.OPERATOR: False,
    classes.LITERAL: False,
    classes.COMMENT: False,
}


def change_state(key):
    # global state
    state.update({key: (not state.get(key))})


def rbmult(iterator):
    """Boolean reverse multiplicator? Returns True if all values are False"""
    for element in iterator:
        if element: return False
    
    return True


def is_clean_state():
    return rbmult(state.values())


def clear_state():
    for key in state.keys():
        state.update({key: False})

# print(is_clean_state())

string_closure = None


def set_string_closure(value):
    global string_closure
    string_closure = value


def get_string_closure():
    return string_closure


def get_token_start(char, i):
    if state[classes.STRING]:
        if char == get_string_closure():
            change_state(classes.STRING)
        return
    elif is_letter(char):
        change_state(classes.IDENTIFIER)
        change_state(classes.KEYWORD)
    elif is_digit(char) or (char in enums.STRING_BORDERS and not state.get(classes.LITERAL)):
        change_state(classes.LITERAL)
    elif char in enums.BLOCKS and not state.get(classes.BLOCK):
        change_state(classes.BLOCK)
    elif min([rm_neg(code.find(operator, i)) for operator in enums.OPERATORS]) == i:
        change_state(classes.OPERATOR)



def rm_neg(number):
    """
    Returns index beyond code length to eliminate negative numbers during sorting
    """
    if number < 0:
        return end + 1
    
    return number


def jump(i, strict_delimeters = None):
    # print('JUMP', min([code.find(delimeter, i) for delimeter in enums.DELIMETERS]))
    return min([rm_neg(code.find(delimeter, i)) for delimeter in (enums.DELIMETERS if not strict_delimeters else strict_delimeters)])


def get_token(start, closing_marks = None):
    end = jump(i, closing_marks)
    return code[start:end], end


def get_closing_marks(opening = None):
    if not opening:
        return None
    
    if opening in enums.STRING_BORDERS:
        return opening
    if opening in enums.BRACKETS:
        return chr(ord(opening)+ (1 if opening == '(' else 2))

    return None

# last_entry = -1
results = { key: [] for key in state.keys() }
results['tokens'] = []

def get_only_state():
    for key in state.keys():
        if state.get(key):
            return key


def add_to_results(token):
    results[get_only_state()].append(token)
# tokens = []
# keywords = []
# indentifiers = []
# literals = []
opening_mark = None
opening_mark_returns = -1
calls = 0
for i in range(len(code)):
    char = code[i]

    # print(char, i)
    if char in [' ', '\n', '.']:
        clear_state()

        continue

    
    get_token_start(char, i)
    print(char, i)
    
    # if char == '"':
    #     print(char in enums.STRING_BORDERS, state.get(classes.LITERAL))
    # if char in enums.STRING_BORDERS and state.get(classes.LITERAL):
    #     opening_mark = char
    #     print(code[i] + 10)

    
    token, i = get_token(i, get_closing_marks(opening_mark))

    if char in enums.OPERATORS:
        token = sorted(enums.OPERATORS, key=lambda op: rm_neg(code.find(op, i)))[0]
        print(token)

    if sum(state.values()) > 1:
        if token in enums.RESERVED:
            clear_state()
            change_state(classes.KEYWORD)
        else:
            clear_state()
            change_state(classes.IDENTIFIER)

    print(state)

    add_to_results(token)
    results['tokens'].append(token)

    print(token)
    print()

    # print(token)


def print_list(name, iterator):
    print('[' + name + ']')
    print(iterator)
    print()

print('\n'.join([key + '\n' + str(results[key]) for key in results.keys()]))
# print_list('tokens', tokens)
# print_list('keywords', keywords)
# print_list('literals', literals)
# print_list('identifiers', indentifiers)