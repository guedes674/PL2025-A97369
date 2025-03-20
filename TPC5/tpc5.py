import re, json

token_specification = [
    ('LISTAR', r'LISTAR'),
    ('MOEDA', r'MOEDA'),
    ('SELECIONAR', r'SELECIONAR'),
    ('SAIR', r'SAIR'),
    ('NUMBER', r'\d+'),
    ('CURRENCY', r'[eE]|[cC]'),
    ('PRODUCT_CODE', r'[A-Z]\d+'),
    ('COMMA', r','),
    ('STOP', r'\.'),
    ('SKIP', r'[ \t]+'),
    ('NEWLINE', r'\n'),
    ('MISMATCH', r'.')
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
        elif dic.get('COMMA') is not None:
            t = ("COMMA", dic['COMMA'], line, match.span())
        elif dic.get('STOP') is not None:
            t = ("STOP", dic['STOP'], line, match.span())
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
        
def calcular_troco(saldo):
    troco = []
    moedas = [200, 100, 50, 20, 10, 5, 2, 1]
    saldo = int(saldo * 100)
    for moeda in moedas:
        while saldo >= moeda:
            troco.append(moeda)
            saldo -= moeda
    return troco

def main():
    stock = carregar_stock()
    saldo = 0
    
    while True:
        comando = input(">>").strip()
        tokens = tokenizer(comando)
        if tokens[0][0] == 'LISTAR':
            listar_stock(stock)
        elif tokens[0][0] == 'MOEDA':
            i = 1
            while i < len(tokens):
                if tokens[i][0] == 'NUMBER':
                    if i+1 >= len(tokens):
                        print("Moeda inválida")
                        break
                    elif tokens[i+1][0] == 'CURRENCY' and tokens[i+1][1].lower() == 'e' and tokens[i][1] in [1,2]:
                        saldo += tokens[i][1]
                    elif tokens[i+1][0] == 'CURRENCY' and tokens[i+1][1].lower() == 'c' and tokens[i][1] in [1,2,5,10,20,50]:
                        saldo += tokens[i][1]/100
                    else:
                        print("Moeda inválida")
                        break
                    i += 2
                elif tokens[i][0] == 'COMMA':
                    i += 1
                elif tokens[i][0] == 'STOP':
                    break
                else:
                    print("Moeda inválida")
            print(f"Saldo: {saldo:.2f}e")
        elif tokens[0][0] == 'SELECIONAR':
            cod = tokens[1][1]
            for produto in stock:
                if produto['cod'] == cod:
                    if saldo >= produto['preco'] and produto['quant'] > 0:
                        produto['quant'] -= 1
                        saldo -= produto['preco']
                        print(f"Pode retirar o produto dispensado \"{produto['nome']}\"")
                    else:
                        print("Quantidade insuficiente")
                    break
            print(f"Saldo: {saldo:.2f}e")
        elif tokens[0][0] == 'SAIR':
            guardar_stock(stock)
            troco = calcular_troco(round(saldo, 2))
            if troco:
                troco_str = ', '.join([f"{moeda // 100}e" if moeda >= 100 else f"{moeda}c" for moeda in troco])
                print(f"Pode retirar o troco: {troco_str}")
            break
        else:
            print("Comando inválido")

main()