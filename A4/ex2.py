# This is our custom local modules, so it doesn't count
from custom_tokenizer import tokenize
from custom_token_classes import classes as c
import enums

import sys

code = sys.stdin.read()

results = tokenize(code)

print('=' * 10 + ' RESULTS ' + '=' * 10)
print('\n\n'.join([key + '\n' + str(results[key]) for key in results.keys()]))

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

print('\n[operands]')
print('inlinedocs:', results['inlinedocs'])
print('literals:', len(results[c.LITERAL]) + len(results[c.INDICE]))

def count_entities(tokens):
    return sum(map(tokens.count, ['def', 'class', '=']))


print('entities:', count_entities(results['tokens']))




