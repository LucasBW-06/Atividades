class tamanho(Exception):
    pass

str_1 = input('Digite uma string: ')
str_2 = input(f'Digite uma string que tenha o mesmo tamanho de "{str_1}": ')
try:
    if len(str_1) == len(str_2):
        print(f'As strings "{str_1}" e "{str_2}" tem o mesmo tamanho')
    else:
        raise tamanho(f'Erro: as strings "{str_1}" e "{str_2}" tem tamanhos diferentes')
except tamanho as e:
    print(e)