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
    """
    Increments number of functions defined in code
    """
    name = line.replace("def", "")[:line.find("(") - 3].strip()
    if not (name.startswith("__") and name.endswith("__")):
        functions.append(name)


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

def find_closing_bracket(line):
    """
    Finds closing bracket (parentheses) for a line (skips internal parentheses)
    """
    if line.find("(") < line.find(")"):
        return find_closing_bracket(line[line.find(")")+1:])
    
    return line.find(")")


def allowed_caller(char):
    """
    Returns true if char is an allowed ending of the function name
    """
    return char ==")" or char=="_" or is_letter(char) or is_digit(char)


def parse_call(line):
    """
    Parses calls in a line of code. Doesn't work with nested (f()()) calls
    """
    if line.strip() == "":
        return ""

    # Find open brackets in line
    open_brackets = line.find("(")
    if (open_brackets) == -1:
        return

    # Trim line to closing brackets
    current_line = line[:find_closing_bracket(line[open_brackets + 1:])]
    # i pointer to the end of string
    i = len(line[:open_brackets-1])
    # Get what inside the brackets
    arguments = line[open_brackets + 1:find_closing_bracket(line[open_brackets + 1:])].split(",")
    # Search for function name
    while i != 0:
        char = line[i]

        # Check if function name found
        if allowed_caller(char):
            # Increment calls number
            add_calls()
            # Search calls in arguments
            return search_calls_in_args(arguments)
            
        # Skip whitespaces
        elif char == " ":
            i -= 1
        
        # If it wasn't a call, search arguments for calls
        # Also break loop early
        elif not allowed_caller(char):
            return search_calls_in_args(arguments)
    
    # Anyway we need it
    return search_calls_in_args(arguments)


def search_calls_in_args(args):
    for arg in args:
        parse_call(arg)


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

    string_border = min(rm_neg(line.find(quote)) for quote in string_borders)
    
    if string_border < comment_char:
        closest_quote = sorted(string_borders, key=lambda op: rm_neg(line.find(op)))[0]
        return parse_line_comment(line[string_border + len(closest_quote):], True, closest_quote)

    return line
    


def remove_inline_comments(code):
    """
    Clean code from inline comments. Returns code without inline comments.
    """
    lines = code.split('\n')
    for i in range(len(lines)):
        
        lines[i] = lines[i].replace(parse_line_comment(lines[i]), "")

    return '\n'.join(lines)


def get_alias(operator_name):
    """
    For operators no named as they are (+, ==, etc.) find corresponding name
    """
    if operator_name in arithmetics:
        return 'arithmetics'
    elif operator_name in boolean:
        return 'logic'
    elif operator_name in assignment:
        return 'assignment'

    return operator_name


def get_operators(code, inside_string=False, string_mark=""):
    """
    Recursive function
    Searches for operators (except calls) and stacks them into dictionary of format {name: num_of_occurences}

    params:
    code - string of code read from .py file
    inside_string - marks for future recursive calls if code was passed with 0 pointer inside the string
    string_mark - character or string that opens/closes current string. Empty if pointer not inside a string

    returns dictionary of format {name: num_of_occurences}
    """
    # jump to the end of the string if we are inside one
    if inside_string:
        code = code[code.find(string_mark) + len(string_mark):]
        
    # closest operator as a string and op_id as it's position in the string
    closest_operator = sorted(operators, key=lambda op: rm_neg(code.find(op)))[0]
    op_id = code.find(closest_operator)

    # if there are no operators, stop and return nothing
    if op_id == -1:
        return {}

    # get closest mark of start/end of the string (multiline included)
    string_border = min(rm_neg(code.find(quote)) for quote in string_borders)
    
    # see if we are inside a string
    if string_border < op_id:
        closest_quote = sorted(string_borders, key=lambda op: rm_neg(code.find(op)))[0]
        return get_operators(code[string_border + len(closest_quote):], True, closest_quote)

    # add function name to functions list
    if closest_operator == 'def':
        save_function(code[op_id:code.find('\n', op_id)])

    # concat current and recursive results to get full operators counter
    current_result = {get_alias(closest_operator): 1}
    recursive_result = get_operators(code[op_id + len(closest_operator):])
    return {k: current_result.get(k, 0) + recursive_result.get(k, 0) for k in set(current_result) | set(recursive_result)}



# remove inline comments
code = remove_inline_comments(code)

# count operators
result = get_operators(code)

print ("[operators]")
for x,z in result.items():
    print (x + ":",z)

# count calls
for line in code.split("\n"):
    parse_call(line)

print ("calls:", number_of_calls)

N1 = sum(result.values()) + number_of_calls
print ("N1:", N1)

# module = __import__("bc")

# # ks = [k for k in dir(module) if (k[:2] != "__" and not callable(k))]
# # def get_locals(ks):
# #     for k in ks:
# #         print("FUNCTION", k)
# #         [print(k1) for k1 in getattr(module, k).__dict__ if (k1[:2] != "__" and not callable(k1))]


# print(getattr(__import__("bc"), 'reflect'))

# # get_locals(ks)
# # print(ks)

# #print("FUNCTIONS:", functions)

# #parse_call("heyhoi(args(args2))")
# #print(number_of_calls)
# #number_of_calls = 0
# #parse_call("x = (1, 2)")
# #print(number_of_calls)
# # number_of_calls = 0
# # parse_call("reflect(reflect)(reflect)(reflect)")
# # print(number_of_calls)
# # number_of_calls = 0

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
