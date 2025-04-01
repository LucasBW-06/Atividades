class Impar(Exception):
    pass

num = int(input("Digite um número par: "))
try:
    if num % 2 == 0:
        print(f'{num} é par')
    else:
        raise Impar(f'Erro: o número {num} não é par')
except Impar as e:
    print(e)