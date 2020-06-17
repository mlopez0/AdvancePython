import enums

file = open('test.py', 'r')
code = file.read()
print(code)
print()

end = len(code)
skipper = -1

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
    ASSIGNMENT = 'assignment'


state = {
    classes.IDENTIFIER: False,
    classes.DELIMITER: False,
    classes.OPERATOR: False,
    classes.LITERAL: False,
    classes.COMMENT: False,
    classes.INDENT: False,
    classes.KEYWORD: False,
    classes.BLOCK: False,
    classes.STRING: False,
    classes.ASSIGNMENT: False
}

prestate = state.copy()

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

def clear_prestate():
    for key in state.keys():
        prestate.update({key: False})

# print(is_clean_state())

string_closure = None


def set_string_closure(value):
    global string_closure
    string_closure = value


def get_string_closure():
    return string_closure


def get_token_state(char, i):
    global skipper
    if state[classes.STRING]:
        print('INSIDE STRING')
        if sorted(enums.STRING_BORDERS, key=lambda q: rm_neg(code.find(q, i)))[0] == get_string_closure()\
            and code.find(get_string_closure(), i) == i:
            skipper = i + len(get_string_closure())
            set_string_closure(None)
            print("CLOSING TRUE", sorted(enums.STRING_BORDERS, key=lambda q: rm_neg(code.find(q, i)))[0],
            min([rm_neg(code.find(q, i)) for q in enums.STRING_BORDERS]), i)
            if not prestate[classes.LITERAL]:
                results['tokens'].append("")
                results[classes.LITERAL].append("")
            clear_state()
            clear_prestate()
            
            return
        else:
            change_state(classes.LITERAL)
        return
    elif char in enums.STRING_BORDERS:
        change_state(classes.STRING)
    elif is_letter(char):
        change_state(classes.IDENTIFIER)
        change_state(classes.KEYWORD)
    elif is_digit(char) or (char in enums.STRING_BORDERS and not state.get(classes.LITERAL)):
        change_state(classes.LITERAL)
    elif char in enums.BLOCKS and not char in enums.CLOSING_BRACKETS:
        change_state(classes.BLOCK)
    elif char in enums.CLOSING_BRACKETS:
        clear_prestate()
        clear_state()
        set_string_closure(None)
    elif min([rm_neg(code.find(operator, i)) for operator in enums.OPERATORS]) == i:
        change_state(classes.OPERATOR)


def rm_neg(number):
    """
    Returns index beyond code length to eliminate negative numbers during sorting
    """
    if number < 0:
        return end + 1
    
    return number


def jump(i, delimeters = None):
    # print('JUMP', min([code.find(delimeter, i) for delimeter in enums.DELIMETERS]))
    print('JUMP', delimeters)
    return min([rm_neg(code.find(delimeter, i)) for delimeter in delimeters])


def get_token(start, closing_marks = None):
    print('CLOS', closing_marks)
    end = jump(i, closing_marks)
    return code[start:end], end


def get_closing_marks(opening = None):
    print('CLO2', opening)
    if not opening:
        return enums.DELIMETERS
    
    if opening in enums.STRING_BORDERS:
        return opening
    if opening in enums.BRACKETS:
        return chr(ord(opening)+ (1 if opening == '(' else 2))

    return enums.DELIMETERS

# last_entry = -1
results = { key: [] for key in state.keys() }
results['tokens'] = []

def get_only_state():
    for key in state.keys():
        if state.get(key):
            return key


def add_to_results(token):
    results[get_only_state()].append(token)


def merge_states(prestate, state):
    return {key: prestate[key] or state[key] for key in state.keys()}


opening_mark = None
opening_mark_returns = -1
calls = 0

for i in range(len(code)):

    if i < skipper:
        continue

    char = code[i]

    # print(char, i)
    if char in [' ', '\n', '.']:
        clear_state()

        continue
    
    print('\n' + '=========='*10 + '\n')
    print("PRESTATE", prestate)

    get_token_state(char, i)
    if i < skipper:
        continue

    if prestate[classes.IDENTIFIER] and state[classes.OPERATOR]:
        prestate[classes.IDENTIFIER] = False
    elif prestate[classes.OPERATOR]:
        prestate[classes.OPERATOR] = False
    elif is_clean_state() and prestate[classes.IDENTIFIER]:
        prestate[classes.IDENTIFIER] = False
    elif is_clean_state() and prestate[classes.LITERAL]:
        prestate[classes.LITERAL] = False

    state = merge_states(prestate, state)

    print(char, i)
    print(state)

    


    if state[classes.STRING] and not state[classes.LITERAL]:
        mark = sorted(enums.STRING_BORDERS, key=lambda q: rm_neg(code.find(q, i)))[0]
        set_string_closure(mark)
        print('OPEN', get_string_closure(), mark)
        skipper = i + len(mark)
        prestate = state.copy()
        print("SAVED", prestate)
        continue

    if state[classes.BLOCK] and state[classes.IDENTIFIER] :
        # Probably function call
        clear_state()
        prestate = state.copy()
        continue
    elif state[classes.BLOCK] and not state[classes.LITERAL]:
        # set_string_closure(char)
        clear_state()
        prestate = state.copy()
        continue
    

    token, skipper = get_token(i, get_closing_marks(get_string_closure()))

    if char in enums.OPERATORS:
        token = sorted(enums.OPERATORS, key=lambda op: rm_neg(code.find(op, i)))[0]
        skipper = i + len(token)
        print(token)

    print(state)
    
    if sum(state.values()) > 1 and not state[classes.STRING]:
        if token in enums.RESERVED:
            clear_state()
            change_state(classes.KEYWORD)
        else:
            clear_state()
            change_state(classes.IDENTIFIER)

    print(state)

    if state[classes.BLOCK]:
        token = char

    print(i, skipper)
    prestate = state.copy()
    print("SAVED", prestate)

    if not is_clean_state():
        add_to_results(token)
        if (not state[classes.STRING]):
            clear_state()
        
        results['tokens'].append(token)

    print(token)
    print()

print('=' * 10 + ' RESULTS ' + '=' * 10)
print('\n\n'.join([key + '\n' + str(results[key]) for key in results.keys()]))
