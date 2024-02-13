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

OPERATIONS = ['ADD', 'SUB', 'DIV', 'MULT']
PARS       = ['LPAR', 'RPAR', 'LSQB', 'RSQB']