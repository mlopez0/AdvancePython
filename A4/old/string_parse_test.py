string_borders = ['"""', "'''", '"', "'"]
inline_comment_borders = ["#", "\n"]
operators = [
    'if', 
    'elif', 
    'else', 
    'try', 
    'for', 
    'with', 
    'return', 
    'def', 
    'import', 
    'except'
]


file = open("bc.py", "r")
code = file.read()

end = len(code)
quote = None


def get_closest_comment(pointer):
    position = code.find("#", pointer) + len(closest_quote)

    return position, closest_quote


def parse_line_comment(line, inside_string=False, string_mark=""):
    if inside_string:
        line = line[line.find(string_mark) + len(string_mark):]
        
    comment_char = line.find("#")

    if comment_char == -1:
        return ""

    string_border = min(rm_neg(line.find(quote)) for quote in string_borders)
    
    if string_border < comment_char:
        closest_quote = sorted(string_borders, key=lambda op: rm_neg(line.find(op)))[0]
        return parse_line_comment(line[string_border + len(closest_quote):], True, closest_quote)

    return line
    


def remove_inline_comments(code):
    lines = code.split('\n')
    for i in range(len(lines)):
        
        lines[i] = lines[i].replace(parse_line_comment(lines[i]), "")
        # if parse_line_comment(lines[i]):
        #     print("LINE", lines[i])

    return '\n'.join(lines)


def get_closest_string(pointer):
    closest_quote = sorted(string_borders, key = lambda quote: rm_neg(code.find(quote, pointer)))[0]
    position = code.find(closest_quote, pointer)
    if position == -1:
        return end + 1, ""

    return position + len(closest_quote), closest_quote


def get_closest(symbol, pointer):
    return code.find(symbol, pointer) + len(symbol)


def jump_string(quote, pointer):
    return get_closest(quote, pointer)


def rm_neg(number):
    if number < 0:
        return end + 1
    
    return number


def get_closest_operator(pointer):
    quote_pointer, closest_quote = get_closest_string(pointer)

    closest_operator = sorted(operators, key=lambda op: rm_neg(code.find(op, pointer)))[0]
    op_pointer = code.find(closest_operator, pointer)

    if op_pointer == -1:
        return -1, ""

    print(quote_pointer, op_pointer)

    if quote_pointer < op_pointer:
        pointer = jump_string(closest_quote, quote_pointer)
        op_pointer, _ = get_closest_operator(pointer)

    closest_quote = None
    pointer += len(closest_operator)
    return op_pointer + len(closest_operator), closest_operator


def get_closest_operator2(line, inside_string=False, string_mark=""):
    if inside_string:
        line = line[line.find(string_mark) + len(string_mark):]
        
    closest_operator = sorted(operators, key=lambda op: rm_neg(line.find(op)))[0]
    op_id = line.find(closest_operator)

    if op_id == -1:
        return {}

    string_border = min(rm_neg(line.find(quote)) for quote in string_borders)
    
    if string_border < op_id:
        closest_quote = sorted(string_borders, key=lambda op: rm_neg(line.find(op)))[0]
        return get_closest_operator2(line[string_border + len(closest_quote):], True, closest_quote)

    current_result = {closest_operator: 1}
    recursive_result = get_closest_operator2(line[op_id + len(closest_operator):])
    return {k: current_result.get(k, 0) + recursive_result.get(k, 0) for k in set(current_result) | set(recursive_result)}


code = remove_inline_comments(code)
pointer = 0
# while pointer != -1:
#     pointer, operator = get_closest_operator(pointer)
#     print(operator)

print(get_closest_operator2(code))
