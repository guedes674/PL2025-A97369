import sys
import re

def tokenizer(code):
    token_specification = [
        ('KEYWORD', r'(?i)(\bSELECT\b|\bWHERE\b|\bLIMIT\b|\bA\b)'),  # Keywords
        ('VARIABLE', r'\?[a-zA-Z_][a-zA-Z0-9_]*'),  # Variável
        ('PREFIXE_IDENTIFIER', r'[a-zA-Z_][a-zA-Z0-9_]*:[a-zA-Z_][a-zA-Z0-9_]*'),  # Prefixo/Identificador
        ('NAME', r'"[^"]*"(@[a-zA-Z]+)?'),  # String com idioma opcional
        ('NUMBER', r'\d+'),  # Números inteiros
        ('OPERATOR', r'[\{\}\.\:\@]'),  # Operadores
        ('NEWLINE', r'\n'),  # Quebra de linha
        ('SKIP', r'[ \t]+'),  # Espaços e tabs
        ('ERRO', r'.'),  # Qualquer outro caractere
    ]

    token_regex = '|'.join([f'(?P<{id}>{expreg})' for (id, expreg) in token_specification])
    recognized = []
    line = 1
    match_object = re.finditer(token_regex, code)

    for match in match_object:
        dic = match.groupdict()
        if dic['KEYWORD'] is not None:
            t = ("KEYWORD", dic['KEYWORD'], line, match.span())
        elif dic['VARIABLE'] is not None:
            t = ("VAR", dic['VARIABLE'], line, match.span())
        elif dic['PREFIXE_IDENTIFIER'] is not None:
            t = ("PRE/ID", dic['PREFIXE_IDENTIFIER'], line, match.span())
        elif dic['NAME'] is not None:
            t = ("NAME", dic['NAME'], line, match.span())
        elif dic['NUMBER'] is not None:
            t = ("NUM", int(dic['NUMBER']), line, match.span())
        elif dic.get('NEWLINE') is not None:  # Evita KeyError
            t = ("NEWLINE", '\n', line, match.span())
            line += 1
        elif dic['OPERATOR'] is not None:
            t = ("OP", dic['OPERATOR'], line, match.span())
        elif dic.get('SKIP') is not None:  # Evita KeyError
            continue
        else:
            t = ("ERRO", match.group(), line, match.span())

        recognized.append(t)

    return recognized

def main():
    code =     code = """select ?nome ?desc where {
?s a dbo:MusicalArtist.
?s foaf:name "Chuck Berry"@en .
?w dbo:artist ?s.
?w foaf:name ?nome.
?w dbo:abstract ?desc
} LIMIT 1000"""
    tokens = tokenizer(code)
    print(tokens)
"""         
        for linha in sys.stdin:
            tokens = tokenizer(linha)
                for token in tokens:
                print(token) """

main()