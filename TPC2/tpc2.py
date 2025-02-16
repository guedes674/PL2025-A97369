import re

def read_csv_data(file_path):
    with open(file_path, encoding='utf-8') as file:
        lines = file.readlines()
        lines.pop(0)
        info = []
        dict_info = {}
        individual = []
        atributte = 1

        for line in lines:
            vals = re.split(r';', line.strip())
            info.append(vals)
            
        for element in info:
            for i in element:
                if atributte == 2:
                    if re.match(r'^(1[0-9]{3}|20[0-2][0-5])$', i):
                        individual.append(i)
                        atributte += 1
                    else:
                        continue
                elif re.match(r'^O[0-9]+$', i):
                    dict_info[i] = individual
                    individual = []
                    atributte = 1
                else:
                    individual.append(i)
                    atributte += 1
    return dict_info

def compositores_alfabetico(dict):
    compositores = set()
    for obra in dict.values():
        compositores.add(obra[3])
    return sorted(compositores)

def distribuicao_periodo(dict):
    distribuicao = {}
    for obra in dict.values():
        periodo = obra[2]
        if periodo not in distribuicao:
            distribuicao[periodo] = 0
        distribuicao[periodo] += 1
    return distribuicao

def obras_periodo(dict):
    periodo_obra = {}
    for obra in dict.values():
        periodo = obra[2]
        titulo = obra[0]
        if periodo not in periodo_obra:
            periodo_obra[periodo] = []
        periodo_obra[periodo].append(titulo)
    
    for periodo in periodo_obra:
        periodo_obra[periodo].sort()

    return periodo_obra

def main():
    dict = read_csv_data("obras.csv")
    op = input("qual das 3 fubções deseja testar? ")
    if op == "1":
        compositores = compositores_alfabetico(dict)
        print(compositores)
    elif op == "2":
        obras = distribuicao_periodo(dict)
        print(obras)
    elif op == "3":
        periodo_obra = obras_periodo(dict)
        print(periodo_obra)

main()