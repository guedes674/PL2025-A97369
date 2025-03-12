import re, sys, json

token_specification = [
    ('LISTAR', r'LISTAR'),
    ('MOEDA', r'MOEDA'),
    ('SELECIONAR', r'SELECIONAR'),
    ('SAIR', r'SAIR'),
    ('NUMBER', r'\d+'),
    ('PRODUCT_CODE', r'[A-Z]\d+'),
    ('SKIP', r'[ \t]+'),  # Espaços e tabs
    ('NEWLINE', r'\n'),  # Quebra de linha
    ('MISMATCH', r'.'),  # Qualquer outro caractere
]

def tokenizer(code):
    token_regex = '|'.join([f'(?P<{id}>{expreg})' for (id, expreg) in token_specification])
    recognized = []
    line = 1
    match_object = re.finditer(token_regex, code)

    for match in match_object:
        dic = match.groupdict()
        if dic.get('LISTAR') is not None:
            t = ("LISTAR", dic['LISTAR'], line, match.span())
        elif dic.get('MOEDA') is not None:
            t = ("MOEDA", dic['MOEDA'], line, match.span())
        elif dic.get('SELECIONAR') is not None:
            t = ("SELECIONAR", dic['SELECIONAR'], line, match.span())
        elif dic.get('SAIR') is not None:
            t = ("SAIR", dic['SAIR'], line, match.span())
        elif dic.get('NUMBER') is not None:
            t = ("NUMBER", int(dic['NUMBER']), line, match.span())
        elif dic.get('CURRENCY') is not None:
            t = ("CURRENCY", dic['CURRENCY'], line, match.span())
        elif dic.get('PRODUCT_CODE') is not None:
            t = ("PRODUCT_CODE", dic['PRODUCT_CODE'], line, match.span())
        elif dic.get('NEWLINE') is not None:
            t = ("NEWLINE", '\n', line, match.span())
            line += 1
        elif dic.get('SKIP') is not None:
            continue
        else:
            t = ("MISMATCH", match.group(), line, match.span())

        recognized.append(t)

    return recognized

def carregar_stock():
    with open('stock.json', 'r') as f:
        return json.load(f)
    
def guardar_stock(stock):
    with open('stock.json', 'w') as f:
        json.dump(stock, f)

def listar_stock(stock):
    print(f"{'cod':<5} | {'nome':<20} | {'preço':<6} | {'quantidade':<10}")
    print("-" * 50)
    for item in stock:
        print(f"{item['cod']:<5} | {item['nome']:<20} | {item['preco']:<6} | {item['quant']:<10}")

def main():
    stock = carregar_stock()
    saldo = 0
    
    while True:
        comando = input(">>").strip()
        tokens = tokenizer(comando)
        
        if tokens[0][0] == 'LISTAR':
            listar_stock(stock)
        elif tokens[0][0] == 'MOEDA':
            valid_coins = [1,2,5,10,20,50,100,200]
            for token in tokens[1:]:
                if token[0] == 'NUMBER':
                    valor = int(token[1])
                    if valor in valid_coins:
                        saldo += valor
                    else:
                        print("Moeda inválida")
            print(f"Saldo: {saldo}")
        elif tokens[0][0] == 'SELECIONAR':
            cod = tokens[1][1]
            for produto in stock:
                if produto['cod'] == cod:
                    if saldo >= produto['preco'] and produto['quant'] > 0:
                        produto['quant'] -= 1
                        saldo -= produto['preco']*100
                    else:
                        print("Quantidade insuficiente")
                    break
            print(f"Saldo: {saldo}")
        elif tokens[0][0] == 'SAIR':
            guardar_stock(stock)
            break
        else:
            print("Comando inválido")

main()