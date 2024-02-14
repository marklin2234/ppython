import string
DIGITS = '0123456789'
LETTERS = string.ascii_letters
LETTERS_DIGITS = LETTERS + DIGITS

TT_INT      = 'INT'
TT_FLOAT    = 'FLOAT'
TT_BOOLEAN  = 'BOOL'
TT_STRING   = "STR"
TT_ADD      = 'ADD'
TT_SUB      = 'SUB'
TT_DIV      = 'DIV'
TT_MULT     = 'MULT'
TT_LPAR     = 'LPAR'
TT_RPAR     = 'RPAR'
TT_LSQB     = 'LSQB'
TT_RSQB     = 'RSQB'
TT_EOF      = 'EOF'
TT_APOS     = 'APOS'
TT_IDEN     = 'VAR'
TT_EQ       = 'EQ'
TT_LEQ      = 'LEQ'
TT_GEQ      = 'GEQ'
TT_GT       = 'GT'
TT_LT       = 'LT'
TT_COMPARE  = 'COMPARE'
TT_NOT      = 'NOT'
TT_AND      = 'AND'
TT_OR       = 'OR'

OPERATIONS = [TT_ADD, TT_SUB, TT_DIV, TT_MULT]
COMPARATORS= [TT_LEQ, TT_GEQ, TT_GT, TT_LT, TT_COMPARE, TT_NOT, TT_AND, TT_OR]