# This is our custom local modules, so it doesn't count
from custom_tokenizer import tokenize
from custom_token_classes import classes as c
import enums

import sys

code = sys.stdin.read()

results = tokenize(code)

print('[operators]')

checked = []
N1 = 0
for operator in results['tokens']:
    if operator not in enums.ASSIGNMENT_OPERATORS\
        or operator in checked: continue
    
    num = results['tokens'].count(operator)
    print(operator + ":", results['tokens'].count(operator))
    N1 += num
    checked.append(operator)


calls = results['calls'] - results[c.KEYWORD].count('def')
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

print("N1:", N1)




def count_entities(tokens):
    return sum(map(tokens.count, ['def', 'class', '=']))


def find_closing_bracket(tokens, brackets = ['(', ')']):
    inside_brackets = False
    for i, token in enumerate(tokens):
        if token == brackets[0]:
            inside_brackets = True
        if token == brackets[1] and not inside_brackets:
            return i


arguments = []
def get_args(tokens, closing_bracket = ')'):
    closing_bracket = min([tokens.index(closing_bracket)])
    args = [[]]
    i = 0
    for token in tokens[:find_closing_bracket(tokens)]:
        
        if token == "|":
            i += 1
            continue
        if i >= len(args):
            args.append([token])
            arguments.append(token)
        else:
            args[i].append(token)
            arguments.append(token)
    
    return args



def count_args(results):
    counter = 0
    tokens = results['tokens']
    for i in range(len(tokens)):
        if tokens[i] in results[c.CALLABLE] and tokens[i-1] not in ['def','class'] and tokens[i+1] == '(':
            if tokens[i+2] != ')':
                counter += len(get_args(tokens[i+2:]))

        elif tokens[i] in results[c.IDENTIFIER] and tokens[i+1].startswith('['):
                counter += 1

    return counter

docs = []
def count_docs(results):
    counter = 0
    tokens = results['tokens']
    for i in range(len(tokens)):
        if tokens[i] in results[c.DOC]:
            if tokens[i-1] != '=' and (arguments.count(tokens[i]) - docs.count(tokens[i]) > 0):
                counter+= 1
                docs.append(tokens[i])

    return counter


N2 = 0

inlinedocs = results['inlinedocs']
literals = len(results[c.LITERAL]) + len(results[c.INDICE])
entities = count_entities(results['tokens'])
args = count_args(results)
docs_num = count_docs(results)

print('\n[operands]')
print('inlinedocs:', results['inlinedocs'])
print('literals:', len(results[c.LITERAL]) + len(results[c.INDICE]))
print('entities:', count_entities(results['tokens']))
print('args:', count_args(results))
print('docs:', count_docs(results))

N2 = inlinedocs + literals + entities + args + docs_num

print("N2:", N2)




