import ply.yacc as yacc
import calc_analex as lex
from calc_analex import tokens

precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
    ('right', 'UMINUS')
)

def p_expression_calc(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression'''
    if p[2] == '+':
        p[0] = p[1] + p[3]
    elif p[2] == '-':
        p[0] = p[1] - p[3]
    elif p[2] == '*':
        p[0] = p[1] * p[3]
    elif p[2] == '/':
        if p[3] == 0:
            print("Divisão por zero")
            p[0] = None
        else:
            p[0] = p[1] / p[3]

def p_expression_num(p):
    'expression : NUM'
    p[0] = int(p[1])
    
def p_expression_uminus(p):
    'expression : MINUS expression %prec UMINUS'
    p[0] = -p[2]

def p_error(p):
    if p:
        print(f"Erro de sintaxe: Token inesperado '{p.value}' na linha {p.lineno}")
    else:
        print("Erro de sintaxe: Entrada inesperada")

lexer = lex.lexer
parser = yacc.yacc()

def main():
    while True:
        try:
            s = input('>> ').strip()
            if not s:
                continue
            result = parser.parse(s, lexer=lexer)
            if result is not None:
                print(result)
        except EOFError:
            break

main()