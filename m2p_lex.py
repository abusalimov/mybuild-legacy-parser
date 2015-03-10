import sys
sys.path.append("../mybuild")

from _compat import *

import ply.lex


# Derived from ANSI C example.

tokens = [
    # Literals (identifier, number, string)
    'ID', 'NUMBER', 'STRING',

    # Delimeters ( ) { } , . $ = ; |
    'LPAREN',   'RPAREN',
    'LBRACE',   'RBRACE',
    'COMMA', 'PERIOD', 'EQUALS',

    #######

    'E_AT',
    'E_WILDCARD',

]

# Completely ignored characters
t_ignore           = ' \t'
t_ignore_COMMENT   = r'//.*'

# Newlines (including block comments)
def t_NEWLINE(t):
    r'(\n|/\*(.|\n)*?\*/)+'
    nr_newlines = t.value.count('\n')
    t.lexer.lineno += nr_newlines


# Paren/bracket counting
def t_LPAREN(t):   r'\('; t.lexer.ignore_newline_stack[-1] += 1;  return t
def t_RPAREN(t):   r'\)'; t.lexer.ignore_newline_stack[-1] -= 1;  return t
def t_LBRACKET(t): r'\['; t.lexer.ignore_newline_stack[-1] += 1;  return t
def t_RBRACKET(t): r'\]'; t.lexer.ignore_newline_stack[-1] -= 1;  return t
def t_LBRACE(t):   r'\{'; t.lexer.ignore_newline_stack.append(0); return t
def t_RBRACE(t):   r'\}'; t.lexer.ignore_newline_stack.pop();     return t

# Delimeters
t_COMMA            = r','
t_PERIOD           = r'\.'
t_COLON            = r':'
t_DOUBLECOLON      = r'::'
t_EQUALS           = r'='
t_SEMI             = r';'


reserved = {
    'true': 'E_BOOL',
    'false': 'E_BOOL',
    'package': 'E_PACKAGE',
    'import': 'E_IMPORT',
    'annotation': 'E_ANNOTATION',
    'interface': 'E_INTERFACE',
    'extends': 'E_EXTENDS',
    'feature': 'E_FEATURE',
    'module': 'E_MODULE',
    'static': 'E_STATIC',
    'abstract': 'E_ABSTRACT',
    'depends': 'E_DEPENDS',
    'provides': 'E_PROVIDES',
    'requires': 'E_REQUIRES',
    'source': 'E_SOURCE',
    'object': 'E_OBJECT',
    'option': 'E_OPTION',
    'string': 'E_STRING',
    'number': 'E_NUMBER',
    'boolean': 'E_BOOLEAN',
}
tokens.extend(set(reserved.values()))

t_E_AT = r'@'
t_E_WILDCARD = r'\.\*'

# Identifiers
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'ID')    # Check for reserved words
    return t

# A regular expression rule with some action code
def t_NUMBER(t):
    r'0x[0-9a-f]+|\d+'
    t.value = int(t.value, base=0)
    return t

# String literal
def t_STRING(t):
    r'\"([^\\\n]|(\\.))*?\"'
    t.value = str(t.value[1:-1].encode().decode("unicode_escape"))
    return t

def t_error(t):
    raise SyntaxError("Illegal character {0!r}".format(t.value[0]),
                      loc(t).to_syntax_error_tuple())


lexer = ply.lex.lex(optimize=1, lextab=None)
lexer.ignore_newline_stack = [0]

if __name__ == "__main__":
    ply.lex.runmain(lexer)