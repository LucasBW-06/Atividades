class minuscula(Exception):
    pass

palavra = input("Digite uma string contendo apenas letras maiusculas: ")
try:
    if any(i.islower() for i in palavra):
        raise minuscula(f'Erro: a string "{palavra}" contém letras minúsculas')
    else:
        print(f'A string "{palavra}" tem apenas letras mauisculas')
except minuscula as e:
    print(e)