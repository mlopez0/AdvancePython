from custom_tokenizer import enums
from custom_tokenizer.custom_token_classes import classes as c


code = ""
end = 0
skipper = -1

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
    c.CALLABLE: False,
    c.DOC: False
}

prestate = state.copy()

tokens = {
    c.IDENTIFIER: False,
    c.DELIMITER: False,
    c.OPERATOR: False,
    c.LITERAL: False,
    c.COMMENT: False,
}

results = { key: [] for key in state.keys() }
results['tokens'] = []


def rm_neg(number):
    global end
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


def remove_inline_comments(_code):
    """
    Clean code from inline comments. Returns code without inline comments.
    """
    lines = _code.split('\n')
    counter = 0
    for i in range(len(lines)):
        inline_comment = parse_line_comment(lines[i])
        if inline_comment != "": counter += 1
        lines[i] = lines[i].replace(inline_comment, "")

    return '\n'.join(lines), counter



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


def change_state(key):
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
        if sorted(enums.STRING_BORDERS, key=lambda q: rm_neg(code.find(q, i)))[0] == get_string_closure()\
            and code.find(get_string_closure(), i) == i:
            skipper = i + len(get_string_closure())
            set_string_closure(None)
            if not prestate[c.LITERAL]:
                results['tokens'].append("")
                results[c.LITERAL].append("")
            
            clear_state()
            clear_prestate()
            
            return

        else:
            change_state(c.LITERAL)
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
    return min([rm_neg(code.find(delimeter, i)) for delimeter in delimeters])


def get_token(start, closing_marks = None):
    end = jump(start, closing_marks)
    return code[start:end], end


def get_closing_marks(opening = None):
    if not opening:
        return enums.DELIMETERS
    
    if opening in enums.STRING_BORDERS:
        return opening

    if opening in enums.BRACKETS:
        return chr(ord(opening)+ (1 if opening == '(' else 2))

    return enums.DELIMETERS


def get_only_state():
    for key in state.keys():
        if state.get(key):
            return key


def get_only_prestate():
    for key in prestate.keys():
        if prestate.get(key):
            return key


def add_to_results(token):
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
        c.CALLABLE,
        c.DOC
    ]


def reduce_states(current_char):
    if sum(prestate.values()) == 1 and get_only_prestate() not in passable_state:
        clear_prestate()

    elif prestate[c.INDICE]:
        set_string_closure('[')
        state[c.STRING] = False

    elif prestate[c.IDENTIFIER] and state[c.OPERATOR]:
        prestate[c.IDENTIFIER] = False
        prestate[c.CALLABLE] = False

    elif prestate[c.OPERATOR]:
        clear_prestate()
        prestate[c.OPERATOR] = False

    elif is_clean_state() and prestate[c.IDENTIFIER] and not current_char == '(':
        prestate[c.IDENTIFIER] = False

    elif is_clean_state() and prestate[c.LITERAL]:
        prestate[c.LITERAL] = False

    elif (prestate[c.IDENTIFIER] and current_char not in ['[', '{']) or current_char == '(':
        prestate[c.CALLABLE] = True


def reduce_merged_state(current_char, pointer):
    global prestate
    global skipper

    if state[c.STRING] and not state[c.LITERAL]:
        mark = sorted(enums.STRING_BORDERS, key=lambda q: rm_neg(code.find(q, pointer)))[0]
        if len(mark) > 1:
            state[c.DOC] = True
        set_string_closure(mark)
        skipper = pointer + len(mark)
        prestate = state.copy()
        return True

    if state[c.BLOCK] and state[c.IDENTIFIER] :
        if current_char == '[':
            clear_state()
            change_state(c.INDICE)
            
        elif not state[c.CALLABLE]:
            clear_state()
            
        prestate = state.copy()
        results['tokens'].append(current_char)
        return True
    elif state[c.BLOCK] and not state[c.LITERAL]:
        clear_state()
        prestate = state.copy()
        results['tokens'].append(current_char)
        return True

    elif get_only_state() == c.CALLABLE:
        results['tokens'].append(current_char)
        return True


def tokenize(code_):
    global end
    global code
    global skipper
    global state
    global prestate

    end = len(code_)
    code, results['inlinedocs'] = remove_inline_comments(code_)

    calls = 0

    for i in range(len(code)):

        if i < skipper:
            continue

        char = code[i]

        if char in [' ', '\n', '.'] and not prestate[c.STRING]:
            clear_prestate()
            clear_state()

            continue

        if char == ',' and not prestate[c.STRING]:
            results['tokens'].append('|')

        get_token_state(char, i)

        if i < skipper:
            continue
        
        reduce_states(char)

        state = merge_states(prestate, state)

        if state[c.CALLABLE] and not prestate[c.BLOCK] and not char in enums.CLOSING_BRACKETS and char not in ['[', '{', ':']:
            calls += 1
            indentifier = results[c.IDENTIFIER][-1]
            results[c.CALLABLE].append(indentifier)
            change_state(c.CALLABLE)

        should_skip = reduce_merged_state(char, i)
        if should_skip:
            continue


        token, skipper = get_token(i, get_closing_marks(get_string_closure()))
        if state[c.OPERATOR]:
            token = sorted(enums.OPERATORS, key=lambda op: rm_neg(code.find(op, i)))[0]
            skipper = i + len(token)

        if state[c.INDICE] and (state[c.LITERAL] or state[c.IDENTIFIER] or state[c.KEYWORD]):
            appendice = '[' + token + ']'
            results['tokens'][-1] += appendice
            results[c.IDENTIFIER][-1] += appendice
            
            i -= 1
            skipper = -1

            set_string_closure(None)

            if not state[c.LITERAL]:
                token = token[:token.find('[')]
            
        if sum(state.values()) > 1 and not (state[c.STRING]):
            if token in enums.RESERVED:
                clear_state()
                change_state(c.KEYWORD)
            elif state[c.LITERAL]:
                clear_state()
                change_state(c.LITERAL)
            else:
                clear_state()
                change_state(c.IDENTIFIER)
                state[c.CALLABLE] = True

        if state[c.BLOCK]:
            token = char

        prestate = state.copy()

        if not is_clean_state():
            add_to_results(token)
            if (not state[c.STRING]):
                clear_state()
            if state[c.DOC]:
                results[c.DOC].append(token)


            results['tokens'].append(token)

        if char == ')' and not state[c.STRING]:
            results['tokens'].append(char)

    results['calls'] = calls
    return results


# TODO: ['string']