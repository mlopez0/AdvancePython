STRING_BORDERS = [
    '"""', 
    "'''", 
    '"', 
    "'"]

INLINE_COMMENTS = [
    "#", 
    "\n"]

KEYWORDS = [
    'if', 
    'elif', 
    'else', 
    'try', 
    'for', 
    'with', 
    'return', 
    'def', 
    'import', 
    'except',
]

BRACKETS = [
    '(',
    ')',
    '[',
    ']',
    '{',
    '}',
]

BLOCKS = [
    *BRACKETS,
]

RESERVED = [
    'False', 
    'None', 
    'True', 
    'and', 
    'as', 
    'assert', 
    'async', 
    'await', 
    'break', 
    'class', 
    'continue', 
    'def', 
    'del', 
    'elif', 
    'else', 
    'except', 
    'finally', 
    'for', 
    'from', 
    'global', 
    'if', 
    'import', 
    'in', 
    'is', 
    'lambda', 
    'nonlocal', 
    'not', 
    'or', 
    'pass', 
    'raise', 
    'return', 
    'try', 
    'while', 
    'with', 
    'yield'
]


ASSIGNMENT = [
    '*=',
    '/=',
    '+=',
    '-=',
    '='
]

BOOLEAN = [
    '==',
    '!='
]

ARITHMETICS = [
    '+',
    '-',
    '**',
    '*',
    '/',
]

OPERATORS = [
    *BOOLEAN,
    *ASSIGNMENT,
    *ARITHMETICS,
    
]

DELIMETERS = [
    ' ',
    '(',
    ')',
    ',',
    '{',
    '}',
    '[',
    ']',
    ':',
    *OPERATORS,
    *ARITHMETICS,
    *INLINE_COMMENTS,
    *STRING_BORDERS,
    *BOOLEAN,
]

CLOSING_BRACKETS = [
    ')',
    ']',
    '}'
]