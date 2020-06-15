from enums import *

file = open("bc.py", "r")
code = file.read()

end = len(code)


def rm_neg(number):
    if number < 0:
        return end + 1
    
    return number


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


def get_alias(operator_name):
    if operator_name in arithmetics:
        return 'arithmetics'
    elif operator_name in boolean:
        return 'logic'
    elif operator_name in assignment:
        return 'assignment'

    return operator_name


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

    
    current_result = {get_alias(closest_operator): 1}
    recursive_result = get_closest_operator2(line[op_id + len(closest_operator):])
    return {k: current_result.get(k, 0) + recursive_result.get(k, 0) for k in set(current_result) | set(recursive_result)}


code = remove_inline_comments(code)
pointer = 0


result = get_closest_operator2(code)

print(result)