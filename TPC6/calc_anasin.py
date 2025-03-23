import calc_analex as lex

tokens = lex.tokens
lexer = lex.lexer

prox_simb = ('Erro', '', 0, 0)

def parserError(simb):
    print("Erro sintático, token inesperado: ", simb)

def rec_term(simb):
    global prox_simb
    if prox_simb.type == simb:
        value = prox_simb.value
        prox_simb = lexer.token()
        return value
    else:
        parserError(prox_simb)

# P1: Expr --> Termo Expr2
def rec_Expr():
    #P1: Expr --> Termo Expr2
    val = rec_Termo()
    val = rec_Expr2(val)
    #P1: Expr --> Termo Expr2
    return val

# P5: Termo --> Fator Termo2
def rec_Termo():
    #P5: Termo --> Fator Termo2
    val = rec_Fator()
    val = rec_Termo2(val)
    #P5: Termo --> Fator Termo2
    return val

# P2: Expr2 --> '+' Termo Expr2
# P3:         | '-' Termo Expr2
# P4:         | epsilon
def rec_Expr2(input_val):
    global prox_simb
    if prox_simb is not None and prox_simb.type == 'PLUS':
        #P2: Expr2 --> '+' Termo Expr2
        rec_term('PLUS')
        termo_val = rec_Termo()
        val = rec_Expr2(input_val + termo_val)
        #P2: Expr2 --> '+' Termo Expr2
        return val
    elif prox_simb is not None and prox_simb.type == 'MINUS':
        #P3: Expr2 --> '-' Termo Expr2
        rec_term('MINUS')
        termo_val = rec_Termo()
        val = rec_Expr2(input_val - termo_val)
        #P3: Expr2 --> '-' Termo Expr2
        return val
    else:
        #P4: Expr2 --> epsilon
        return input_val

# P9: Fator --> '(' Expr ')'
# P10:        | NUM
# P11:        | '-' NUM
def rec_Fator():
    global prox_simb
    if prox_simb.type == 'MINUS':
        #P11: Fator --> '-' Fator (unário)
        rec_term('MINUS')
        val = rec_Fator()
        return -val
    if prox_simb.type == 'PA':
        #P9: Fator --> '(' Expr ')'
        rec_term('PA')
        val = rec_Expr()
        rec_term('PF')
        #P9: Fator --> '(' Expr ')'
        return val
    elif prox_simb.type == 'NUM':
        #P10: Fator --> NUM
        val = int(rec_term('NUM'))
        #P10: Fator --> NUM
        return val
    else:
        parserError(prox_simb)
        return 0

# P6: Termo2 --> '*' Fator Termo2
# P7:          | '/' Fator Termo2
# P8:          | epsilon
def rec_Termo2(input_val):
    global prox_simb
    if prox_simb is None:
        return input_val
    if prox_simb.type == 'TIMES':
        #P6: Termo2 --> '*' Fator Termo2
        rec_term('TIMES')
        fator_val = rec_Fator()
        val = rec_Termo2(input_val * fator_val)
        #P6: Termo2 --> '*' Fator Termo2
        return val
    elif prox_simb.type == 'DIVIDE':
        #P7: Termo2 --> '/' Fator Termo2
        rec_term('DIVIDE')
        fator_val = rec_Fator()
        val = rec_Termo2(input_val / fator_val)
        #P7: Termo2 --> '/' Fator Termo2
        return val
    else:
        #P8: Termo2 --> epsilon
        return input_val

def rec_Parser(data):
    global prox_simb
    lexer.input(data)
    prox_simb = lexer.token()
    result = rec_Expr()
    if prox_simb is not None:
        parserError(prox_simb)
    else:
        print("Resultado =", result)

def main():
    while True:
        try:
            data = input('>> ')
        except EOFError:
            break
        rec_Parser(data)

main()