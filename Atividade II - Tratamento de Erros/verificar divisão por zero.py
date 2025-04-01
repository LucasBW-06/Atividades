num = int(input('Digite um inteiro: '))
try:
    print(10/num)
except ZeroDivisionError:
    print('Erro: divisão por zero')