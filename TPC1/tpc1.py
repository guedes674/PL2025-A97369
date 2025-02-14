import sys

text = "Hoje, 7 de Fevereiro de 2025, o professor de Processamento de Linguagens deu-nos este trabalho para fazer.=OfF E deu-nos 7= dias para o fazer... ON Cada trabalho destes vale 0.25 valores da nota final!"

def somador_on_off(text):
    soma = 0
    ativado = True
    num = ""
    i = 0
    text = text.strip().lower()
    print(text)

    for i,c in enumerate(text):
        if c == "o":
            if text[i+1] == "n":
                ativado = True
            elif text[i+1] == "f" and text[i+2] == "f":
                ativado = False
            if num != "":
                soma += int(num)
                num = ""
        elif c.isdigit() and ativado:
            num += c
        elif text[i] == "=":
            print(soma)
        elif num != "":
            soma += int(num)
            num = ""
    print(soma)

if __name__ == "__main__":
    somador_on_off(text)