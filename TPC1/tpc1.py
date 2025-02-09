import re

def somador_on_off(texto):
    ac = []
    a_somar = True

    tokens = re.findall(r'\d+|[Oo][Nn]|[Oo][Ff][Ff]|=', texto)
    for token in tokens:
        if re.fullmatch(r'[Oo][Nn]', token):
            a_somar = True
        elif re.fullmatch(r'[Oo][Ff][Ff]', token):
            a_somar = False
        elif re.fullmatch(r'\d+', token):
            if a_somar:
                ac.append(int(token))
        elif re.fullmatch(r'=', token):
            print(sum(ac))

texto = input("Indique o texto para realizar a soma: ")
somador_on_off(texto)