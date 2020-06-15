from enums import *
import math

file = open("bc.py", "r")
code = file.read()

end = len(code)

functions = []
number_of_calls = 0


def add_calls():
    global number_of_calls
    number_of_calls += 1

def save_function(line):
    name = line.replace("def", "")[:line.find("(") - 3].strip()
    if not (name.startswith("__") and name.endswith("__")):
        functions.append(name)


def is_letter(char):
    return (ord(char) <= 122 and ord(char) >= 97) or (ord(char) <= 90 and ord(char) >= 65)


def is_digit(char):
    return ord(char) >= 48 and ord(char) <= 56

def find_closing_bracket(line):
    print("CLOS", line)
    if line.find("(") < line.find(")"):
        return find_closing_bracket(line[line.find(")")+1:])
    
    return line.find(")")


# def find_prev_char(line, position):
#     while i != 0:
#         char = line[i]
#         if allowed_caller(char):
#             add_calls()
#             return parse_call(arguments)
#         elif char == " ":
#             i -= 1
#         elif not allowed_caller(char):
#             return parse_call(arguments)

def allowed_caller(char):
    return char ==")" or is_letter(char) or is_digit(char)


def parse_call(line):
    print("LINE", line)
    if line.strip() == "":
        return ""

    open_brackets = line.find("(")
    if (open_brackets) == -1:
        return

    i = len(line[:open_brackets-1])
    arguments = line[open_brackets + 1:find_closing_bracket(line[open_brackets + 1:])]
    print("ARGS", arguments)

    while i != 0:
        char = line[i]
        print(line, char, ord(char))
        if allowed_caller(char):
            print(char, ord(char))
            add_calls()
            return parse_call(arguments)
        elif char == " ":
            i -= 1
        elif not allowed_caller(char):
            return parse_call(arguments)
        
    return parse_call(arguments)


# def parse_calls(line):
#     closest_bracket = line.find("(")


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

    if closest_operator == 'def':
        # print(line[op_id:line.find('\n', op_id)])
        save_function(line[op_id:line.find('\n', op_id)])


    current_result = {get_alias(closest_operator): 1}
    recursive_result = get_closest_operator2(line[op_id + len(closest_operator):])
    return {k: current_result.get(k, 0) + recursive_result.get(k, 0) for k in set(current_result) | set(recursive_result)}


code = remove_inline_comments(code)
pointer = 0


result = get_closest_operator2(code)

print ("[OPERATORS]")
N1= 0
for x,z in result.items():
    print (x, ": ",z)
    N1 = N1 + z

#print("FUNCTIONS:", functions)

#parse_call("heyhoi(args(args2))")
#print(number_of_calls)
#number_of_calls = 0
#parse_call("x = (1, 2)")
#print(number_of_calls)
# number_of_calls = 0
# parse_call("reflect(reflect)(reflect)(reflect)")
# print(number_of_calls)
# number_of_calls = 0

# parse_call("reflect(reflect)(reflect)")


def programF(n1,n2,N1,N2):
    n = n1+n2
    print ("Program vocabulary:", n)
    N = N1 + N2
    print ("Program lenght:", N)
    L = n1*math.log(N1,2)+n2*math.log(N2,2)
    print ("Calculated program length:", L)
    V = N * math.log(n,2)
    print ("Volume:", V)
    D = (n1/2)*(N2/n2)
    print ("Difficulty:", D)
    E = D*V
    print ("Effort:", E)

print ("\n[program]")
n1 = len(operators)
n2 = 5 #len(operands) ## Must pass the value of n2 instead of 5

programF(n1,n2,N1,20) ## Must pass the value of N2 instead of 20