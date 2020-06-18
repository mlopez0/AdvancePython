import enums

file = open('test.py', 'r')
code = file.read()
print(code)
print()

end = len(code)
skipper = -1


def rm_neg(number):
    """
    Returns index beyond code length to eliminate negative numbers during sorting
    """
    if number < 0:
        return end + 1
    
    return number


def parse_line_comment(line, inside_string=False, string_mark=""):
    """
    Find inline comment in a line and return inline comment as a string
    """
    if inside_string:
        line = line[line.find(string_mark) + len(string_mark):]
        
    comment_char = line.find("#")

    if comment_char == -1:
        return ""

    string_border = min(rm_neg(line.find(quote)) for quote in enums.STRING_BORDERS)
    
    if string_border < comment_char:
        closest_quote = sorted(enums.STRING_BORDERS, key=lambda op: rm_neg(line.find(op)))[0]
        return parse_line_comment(line[string_border + len(closest_quote):], True, closest_quote)
    
    return line[comment_char:]


def remove_inline_comments(code):
    """
    Clean code from inline comments. Returns code without inline comments.
    """
    lines = code.split('\n')
    for i in range(len(lines)):
        
        lines[i] = lines[i].replace(parse_line_comment(lines[i]), "")

    return '\n'.join(lines)

code = remove_inline_comments(code)
print(code)


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


class c:
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
    INDICE = 'indice'
    CALLABLE = 'callable'


state = {
    c.IDENTIFIER: False,
    c.DELIMITER: False,
    c.OPERATOR: False,
    c.LITERAL: False,
    c.COMMENT: False,
    c.INDENT: False,
    c.KEYWORD: False,
    c.BLOCK: False,
    c.STRING: False,
    c.ASSIGNMENT: False,
    c.INDICE: False,
    c.CALLABLE: False
}

prestate = state.copy()

tokens = {
    c.IDENTIFIER: False,
    c.DELIMITER: False,
    c.OPERATOR: False,
    c.LITERAL: False,
    c.COMMENT: False,
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

string_closure = None


def set_string_closure(value):
    global string_closure
    string_closure = value


def get_string_closure():
    return string_closure


def get_token_state(char, i):
    global skipper
    if prestate[c.STRING]:
        print('INSIDE STRING')
        if sorted(enums.STRING_BORDERS, key=lambda q: rm_neg(code.find(q, i)))[0] == get_string_closure()\
            and code.find(get_string_closure(), i) == i:
            skipper = i + len(get_string_closure())
            set_string_closure(None)
            print("CLOSING TRUE", sorted(enums.STRING_BORDERS, key=lambda q: rm_neg(code.find(q, i)))[0],
            min([rm_neg(code.find(q, i)) for q in enums.STRING_BORDERS]), i)
            if not prestate[c.LITERAL]:
                results['tokens'].append("")
                results[c.LITERAL].append("")
            clear_state()
            clear_prestate()
            
            return
        else:
            change_state(c.LITERAL)
    # elif prestate[c.STRING]:
    #     change_state(c.LITERAL)
    elif char in enums.STRING_BORDERS:
        change_state(c.STRING)
    elif is_letter(char):
        change_state(c.IDENTIFIER)
        change_state(c.KEYWORD)
    elif char == '_':
        change_state(c.IDENTIFIER)
    elif is_digit(char) or (char in enums.STRING_BORDERS and not state.get(c.LITERAL)):
        change_state(c.LITERAL)
    elif char in enums.BLOCKS and not char in enums.CLOSING_BRACKETS:
        change_state(c.BLOCK)
    elif char in enums.CLOSING_BRACKETS and not prestate[c.IDENTIFIER]:
        clear_prestate()
        clear_state()
        set_string_closure(None)
    elif char in enums.CLOSING_BRACKETS and prestate[c.IDENTIFIER]:
        clear_prestate()
        clear_state()
        set_string_closure(None)
        prestate[c.CALLABLE] = True
    elif min([rm_neg(code.find(operator, i)) for operator in enums.OPERATORS]) == i:
        change_state(c.OPERATOR)


def jump(i, delimeters = None):
    print('JUMP', min([code.find(delimeter, i) for delimeter in enums.DELIMETERS]))
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
    # if state[c.INDICE] and state[c.IDENTIFIER] and opening in enums.BRACKETS:
    #     return opening
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


def get_only_prestate():
    for key in prestate.keys():
        if prestate.get(key):
            return key


def add_to_results(token):
    print('RESULT', get_only_state(), token)
    results[get_only_state()].append(token)


def merge_states(prestate, state):
    return {key: prestate[key] or state[key] for key in state.keys()}


passable_state = [
    c.IDENTIFIER,
    c.INDICE,
    c.STRING,
    c.BLOCK,
    c.OPERATOR,
    c.LITERAL,
    c.CALLABLE
]

callable_breakers = [
]

opening_mark = None
opening_mark_returns = -1
calls = 0

for i in range(len(code)):

    if i < skipper:
        continue

    char = code[i]

    print(char, i)
    if char in [' ', '\n', '.'] and not prestate[c.STRING]:
        clear_prestate()
        clear_state()

        continue
    
    print('\n' + '=========='*10 + '\n')
    print("PRESTATE", prestate, char)

    get_token_state(char, i)
    if i < skipper:
        continue
    
    if sum(prestate.values()) == 1 and get_only_prestate() not in passable_state:
        print("CLEARING PRESTATE")
        clear_prestate()
    elif prestate[c.INDICE]:
        print('2')
        set_string_closure('[')
    elif prestate[c.IDENTIFIER] and state[c.OPERATOR]:
        print('3')
        prestate[c.IDENTIFIER] = False
        prestate[c.CALLABLE] = False
    elif prestate[c.OPERATOR]:
        print('4')
        clear_prestate() # ?
        prestate[c.OPERATOR] = False
    elif is_clean_state() and prestate[c.IDENTIFIER] and not char == '(':
        print('5')
        prestate[c.IDENTIFIER] = False
    elif is_clean_state() and prestate[c.LITERAL]:
        print('6')
        prestate[c.LITERAL] = False
    elif (prestate[c.IDENTIFIER] and char not in ['[', '{']) or char == '(':
        print('7')
        prestate[c.CALLABLE] = True

    print("PRESTATE", prestate)

    state = merge_states(prestate, state)

    if state[c.CALLABLE] and not prestate[c.BLOCK] and not char in enums.CLOSING_BRACKETS and char not in ['[', '{', ':']:
        print('CALL')
        calls += 1
        indentifier = results[c.IDENTIFIER][-1]
        results[c.CALLABLE].append(indentifier)
        change_state(c.CALLABLE)


    print(char, i)
    print(state)


    if state[c.STRING] and not state[c.LITERAL]:
        mark = sorted(enums.STRING_BORDERS, key=lambda q: rm_neg(code.find(q, i)))[0]
        set_string_closure(mark)
        print('OPEN', get_string_closure(), mark)
        skipper = i + len(mark)
        prestate = state.copy()
        print("SAVED", prestate)
        continue

    if state[c.BLOCK] and state[c.IDENTIFIER] :
        if char == '[':
            clear_state()
            change_state(c.INDICE)
            
        # Probably function call
        elif not state[c.CALLABLE]:
            clear_state()
        
        results['tokens'].append(char)
        prestate = state.copy()
        continue
    elif state[c.BLOCK] and not state[c.LITERAL]:
        # set_string_closure(char)
        clear_state()
        results['tokens'].append(char)
        prestate = state.copy()
        continue
    elif get_only_state() == c.CALLABLE:
        results['tokens'].append(char)
        continue
    

    token, skipper = get_token(i, get_closing_marks(get_string_closure()))

    if state[c.OPERATOR]:
        token = sorted(enums.OPERATORS, key=lambda op: rm_neg(code.find(op, i)))[0]
        skipper = i + len(token)
        print(token)

    print(state)
    

    if state[c.INDICE] and (state[c.LITERAL] or state[c.IDENTIFIER] or state[c.KEYWORD]):
        appendice = '[' + token + ']'
        print('ADDED', results['tokens'][-1], end =' ')
        results['tokens'][-1] += appendice
        results[c.IDENTIFIER][-1] += appendice

        print(appendice)
        
        i -= 1
        skipper = -1

        set_string_closure(None)

        # change_state(c.INDICE)
        # if state[c.LITERAL]:
        #     add_to_results(token)
        #     results['tokens'].append(token)
            
        # clear_state()
        # prestate = state.copy()
        # continue
        if not state[c.LITERAL]:
            token = token[:token.find('[')]
        
        

    if sum(state.values()) > 1 and not (state[c.STRING]):
        if token in enums.RESERVED:
            clear_state()
            change_state(c.KEYWORD)
        elif state[c.LITERAL]:
            if state[c.DOC]:
                results[c.DOC].append

            clear_state()
            change_state(c.LITERAL)
        else:
            clear_state()
            change_state(c.IDENTIFIER)
            state[c.CALLABLE] = True


    print(state)

    if state[c.BLOCK]:
        token = char

    print(i, skipper)
    prestate = state.copy()
    print("SAVED", prestate)

    if not is_clean_state():
        add_to_results(token)
        if (not state[c.STRING]):
            clear_state()
        
        results['tokens'].append(token)

    print(token)
    print()

print('=' * 10 + ' RESULTS ' + '=' * 10)
print('\n\n'.join([key + '\n' + str(results[key]) for key in results.keys()]))

print('[operators]')
checked = []
N1 = 0
for operator in results['tokens']:
    if operator not in enums.ASSIGNMENT_OPERATORS\
        or operator in checked: continue
    
    print(operator + ":", results['tokens'].count(operator))
    checked.append(operator)


calls = calls - results[c.KEYWORD].count('def')
assign = results[c.OPERATOR].count('=')
logic = sum(map(results[c.OPERATOR].count, ['==', '!='])) + sum(map(results[c.KEYWORD].count, ['and', 'not']))
arithmetic = sum(map(results[c.OPERATOR].count, ['+', '-', '/', '*']))

N1 += calls + assign + logic + arithmetic

if N1 == 0:
    print('-\n')

if calls > 0: print('calls:', calls)
if assign > 0: print('assign:', assign)
if logic > 0: print('logic:', logic)
if arithmetic > 0: print('arithmetic:', arithmetic)
    
print('[operands]')
print('literals:', len(results[c.LITERAL]))
print('entities:', len(set(results[c.IDENTIFIER])))



