from enums import *

# file = open("bc.py", "r")
# code = file.read()

# end = len(code)

# functions = []
# number_of_calls = 0
# prev_line_closed = False

# def multisplit(s, delims):
#     pos = 0
#     for i, c in enumerate(s):
#         if c in delims:
#             yield s[pos:i]
#             pos = i + 1
#     yield s[pos:]


# def is_closed(line):
#     pass

tokens = string_borders + operators + assignment + boolean + arithmetics


def rm_neg(number, line):
    end = len(line)
    if number < 0:
        return end + 1
    
    return end


# state = {
#     inside_string: False,
#     inside_parentheses: False,
#     inside_function: False
# }


class Def:
    def __init__(self, name, args, body):
        self.name = name
        self.args = args
        self.body = body


def update_state(token):
    pass


def jump_string(mark, line):
    if mark in string_borders:
        return line[:line.find(mark)]
    
    return mark


def find_closing_parentheses(line):
    if line.find("(") < line.find(")"):
        return find_closing_parentheses(line[line.find(")")+1:])
    
    return line.find(")")


def parse_function(line):
    name = line[:line.find("(")].strip()
    args = line[line.find("("):find_closing_parentheses(line)]
    


def pipe(token, line):
    if token == "def":
        


def get_closest_token(line):
    token = sorted(tokens, key=lambda token: rm_neg(line.find(token), line))[0]
    updated_line = line[line.find(token) + len(token):]
    pipe(token, updated_line)
    return token

print(get_closest_token('def x():'))
