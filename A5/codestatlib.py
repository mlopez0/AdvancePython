import inspect
from io import StringIO 
import sys
import dis
import math
import os
from custom_tokenizer.custom_tokenizer import tokenize
from custom_tokenizer.custom_token_classes import classes as c
from custom_tokenizer import enums
from functools import wraps

class Capturing(list):
    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = self._stringio = StringIO()
        return self
    def __exit__(self, *args):
        self.extend(self._stringio.getvalue().splitlines())
        del self._stringio    # free up some memory
        sys.stdout = self._stdout


def print_multiline_cell(lines, strip_line = False):
    if not lines:
        # print("\tNone")
        return

    for line in lines:
        line = line if not strip_line else line.strip()
        # print("\t", line.replace("\n",""))
    # print()


def print_multiline_row(label, lines, strip_line=False):
    # print(label + ":", end="")
    print_multiline_cell(lines, strip_line)


def search_word(function, word):
    for counter, line in enumerate(inspect.getsourcelines(function)[0]):
            counter = counter + line.count(word)

    return counter
    # print ("\t" + str({word: counter}))


class StaticAnalysis:
    def __init__(self, object):
        code = inspect.getsource(object)
        self.results = tokenize(code)
        self.arguments = []
        self.n1 = 20
        self.n2 = 5
        self.calls = self.calc_calls()
        self.assign = self.calc_assign()
        self.arithmetic = self.calc_arithmetic()
        self.logic = self.calc_logic()
        self.N1 = self.calc_N1() 
        self.N2 = self.calc_N2()

        

    def calc_N1(self):
        return self.calls + self.assign + self.arithmetic  + self.logic

    def calc_operators(self):
        operators_count = 0
        checked = []
        for operator in self.results['tokens']:
            if operator not in enums.ASSIGNMENT_OPERATORS\
                or operator in checked: continue
            
            num = results['tokens'].count(operator)
            # print(operator + ":", results['tokens'].count(operator))
            operators_count += num
            checked.append(operator)
        
        return operators_count

    def calc_calls(self):
        return self.results['calls'] - self.results[c.KEYWORD].count('def')

    def calc_assign(self):
        return self.results[c.OPERATOR].count('=')

    def calc_logic(self):
        operators = sum(map(self.results[c.OPERATOR].count, ['==', '!=']))
        keywords = sum(map(self.results[c.KEYWORD].count, ['and', 'not']))
        return  operators + keywords   

    def calc_arithmetic(self):
        return sum(map(self.results[c.OPERATOR].count, ['+', '-', '/', '*']))

    @staticmethod
    def count_entities(tokens):
        return sum(map(tokens.count, ['def', 'class', '=']))

    @staticmethod
    def find_closing_bracket(tokens, brackets = ['(', ')']):
        inside_brackets = False
        for i, token in enumerate(tokens):
            if token == brackets[0]:
                inside_brackets = True
            if token == brackets[1] and not inside_brackets:
                return i
    
    def get_args(self, tokens, closing_bracket = ')'):
        closing_bracket = min([tokens.index(closing_bracket)])
        args = [[]]
        i = 0
        for token in tokens[:self.find_closing_bracket(tokens)]:
            
            if token == "|":
                i += 1
                continue
            if i >= len(args):
                args.append([token])
                self.arguments.append(token)
            else:
                args[i].append(token)
                self.arguments.append(token)
        
        return args

    def count_args(self):
        counter = 0
        tokens = self.results['tokens']
        for i in range(len(tokens)):
            try:
                if tokens[i] in self.results[c.CALLABLE] and tokens[i-1] not in ['def','class'] and tokens[i+1] == '(':
                    if tokens[i+2] != ')':
                        counter += len(self.get_args(tokens[i+2:]))

                elif tokens[i] in self.results[c.IDENTIFIER] and tokens[i+1].startswith('['):
                        counter += 1
            except IndexError:
                continue

        return counter
    
    def count_docs(self):
        docs = []
        counter = 0
        tokens = self.results['tokens']
        for i in range(len(tokens)):
            if tokens[i] in self.results[c.DOC]:
                if tokens[i-1] != '=' and (self.arguments.count(tokens[i]) - docs.count(tokens[i]) > 0):
                    counter+= 1
                    docs.append(tokens[i])

        return counter


    def calc_inlinedocs(self):
        return self.results['inlinedocs']

    def calc_literals(self):
        return len(self.results[c.LITERAL]) + len(self.results[c.INDICE])

    def calc_entities(self):
        return self.count_entities(self.results['tokens'])

    def calc_args(self):
        return self.count_args()

    def calc_docs(self):
        return self.count_docs()
    
    def calc_N2(self):
        return self.calc_inlinedocs() + self.calc_literals() + self.calc_entities() + self.calc_args() + self.calc_docs()

    def calc_vocabulary(self):
        return self.n1 + self.n2

    def calc_length(self):
        return self.N1 + self.N2

    def calc_calc_length(self):
        if not self.N1 <=0 or self.N2 <= 0:
            # print(self.N1, self.N2)
            return self.n1 * math.log(self.N1,2) + self.n2 * math.log(self.N2,2)

        return 0

    def calc_volume(self):
        return self.calc_length() * math.log(self.calc_vocabulary(),2)

    def calc_difficulty(self):
        return (self.n1/2)*(self.N2/self.n2)

    def calc_effort(self):
        return self.calc_difficulty() * self.calc_volume()


def stat_object(function):
    # sys.stdout = open(os.devnull, "w")
    # sys.stdout = sys.__stdout__
    # if type(function) is tuple:
    #     function = function[0]
    #     print(function[1])
        
    @wraps(function)
    def wrapper(*args, **kwrd):
        # output = []
        result = {}

        result['name'] = function.__name__
        result['type'] = type(function)
        result['sign'] = inspect.signature(function)
        result['args'] = locals()['args']
        result['kwrd'] = locals()['kwrd']
        result['doc'] = function.__doc__
        result['source'] = inspect.getsource(function)

        with Capturing() as output:
            function(*args, **kwrd)
            pass

        result['output'] = output

        redirect_output(result)
        
        return function(*args, **kwrd)

    sys.stdout = sys.__stdout__
    return wrapper


def stat_complexity(function):
    
    sys.stdout = open(os.devnull, "w")
    @wraps(function)
    def wrapper(*args, **kwrd):
        # with Capturing() as output:
        #     function(*args, **kwrd)

        result = {}
        analysis = StaticAnalysis(function)
        result['operators'] = {}
        result['operands'] = {}
        result['program'] = {}

        result['operators']['calls'] = analysis.calc_calls()
        result['operators']['assign'] = analysis.calc_assign()
        result['operators']['arithmetic'] = analysis.calc_arithmetic()
        result['operators']['logic'] = analysis.calc_logic()
        result['operators']['N1'] = analysis.calc_N1()

        result['operands']['inlinedocs'] = analysis.calc_inlinedocs()
        result['operands']['literals'] = analysis.calc_literals()
        result['operands']['entities'] = analysis.calc_entities()
        result['operands']['args'] = analysis.calc_args()
        result['operands']['docs'] = analysis.calc_docs()

        result['program']['vocabulary'] = analysis.calc_vocabulary()
        result['program']['length'] = analysis.calc_length()
        result['program']['calc_length'] = analysis.calc_calc_length()
        result['program']['volume'] = analysis.calc_volume()
        result['program']['difficulty'] = analysis.calc_difficulty()
        result['program']['effort'] = analysis.calc_effort()
        # function(*args, **kwrd)
        redirect_output(result)
        
        return function(*args, **kwrd)
    
    sys.stdout = sys.__stdout__
    return wrapper


results = []

# def add_result(result):
#     results.append(result)

def redirect_output(msg):
    sys.stdout = sys.__stdout__
    # sys.stdout.write(str(msg))
    print(str(msg))
    sys.stdout = open(os.devnull, "w")

# stat_object(stat_complexity(foo))
