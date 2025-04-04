import pandas as pd
import numpy as np
import os

def input_grade(prt):
    try:
        num = float(input(prt))
        if num > 10 or num < 0:
            raise ValueError
    except ValueError:
        os.system('cls')
        print('Valor inválido')
        num = input_grade(prt)
    return num

def question(prt, options, ans='Opção inválida', invert=False):
    answer = input(prt).strip()
    if answer in options and invert:
        os.system('cls')
        print(ans)
        answer = question(prt, options, ans, True)
    elif answer not in options and not invert:
        os.system('cls')
        print(ans)
        answer = question(prt, options)
    return answer

def add_student(data):
    os.system('cls')
    name = question('Digite o nome do aluno: ',[row['Aluno'] for index, row in data.iterrows()], 'Aluno já registrado!', True)
    grades = [input_grade(f'Digite a nota {i+1}: ') for i in range(3)]
    new = pd.DataFrame({
        'Aluno': [name],
        'Nota 1': [grades[0]],
        'Nota 2': [grades[1]],
        'Nota 3': [grades[2]],
        'Nota exame': [np.nan],
        'Condição': [np.nan],
        'Média': [np.nan]
    })

    if data.empty:
        data = new
    else:
        data = pd.concat([data, new], ignore_index=True)
    
    answer = question('Adicionar outro aluno? S/N\n', ['S', 'N'])
    if answer == 'S':
        data = add_student(data)
    os.system('cls')
    return data

def calculate_grades(data):
    for index, row in data.iterrows():
        if row['Condição'] == 'Exame' and not pd.isna(row['Nota exame']):
            media = round((row['Média'] / 3 + row['Nota exame']) / 2, 2)
            if media >= 5:
                data.at[index, 'Condição'] = 'Aprovado após exame'
            else:
                data.at[index, 'Condição'] = 'Reprovado após exame'
            data.at[index,'Média'] = media
        elif pd.isna(row['Condição']):
            media = round((row['Nota 1'] + row['Nota 2'] + row['Nota 3']) / 3, 2)
            if media >= 7:
                data.at[index, 'Condição'] = 'Aprovado'
            elif media < 5:
                data.at[index, 'Condição'] = 'Reprovado'
            else:
                data.at[index, 'Condição'] = 'Exame'
            data.at[index,'Média'] = media
    os.system('cls')
    return data

def add_exam_grades(data):
    os.system('cls')
    students = [row['Aluno'] for index, row in data.iterrows() if row['Condição'] == 'Exame']
    str = '\n'.join(['Alunos de exame:'] + students + ['\nDigite o nome do aluno: '])
    name = question(str, students, 'Nome inválido!')
    exam = input_grade('Digite a nota: ')
    data.loc[data['Aluno'] == name, 'Nota exame'] = exam
    answer = question('Adicionar outro aluno? S/N\n', ['S','N'])
    data = calculate_grades(data)
    if answer == 'S':
        data = add_exam_grades(data)
    os.system('cls')
    return data

def modify_grades(data):
    os.system('cls')
    students = [row['Aluno'] for index, row in data.iterrows()]
    str = '\n'.join(['Alunos:'] + students + ['\nDigite o nome do aluno: '])
    name = question(str, students, 'Nome inválido!')

    if not pd.isna(data.loc[data['Aluno'] == name, 'Nota exame'].iloc[0]):
        n = 4
        data.loc[data['Aluno'] == name, 'Condição'] = 'Exame'
    else:
        n = 3
        data.loc[data['Aluno'] == name, 'Condição'] = np.nan
    for i in range(n):
        str = f'{data.columns[i+1]}: {data.loc[data["Aluno"] == name, data.columns[i+1]].iloc[0]}\nDigite a nota substituta: '
        grade = input_grade(str)
        data.loc[data['Aluno'] == name, data.columns[i+1]] = grade

    answer = question('Modificar outro aluno? S/N\n',['S','N'])
    if answer == 'S':
        data = modify_grades(data)
    os.system('cls')
    return data

def remove(data):
    os.system('cls')
    students = [row['Aluno'] for index, row in data.iterrows()]
    str = '\n'.join(['Alunos:'] + students + ['\nDigite o nome do aluno: '])
    name = question(str,students,'Nome inválido!')

    data = data.drop(data[data['Aluno'] == name].index)

    answer = question('Remover outro aluno? S/N\n',['S','N'])
    if answer == 'S':
        data = remove(data)
    os.system('cls')
    return data

def verify():
    if not os.path.exists('dados_alunos.xlsx'):
        df = pd.DataFrame(columns=['Aluno', 'Nota 1', 'Nota 2', 'Nota 3', 'Nota exame', 'Condição', 'Média'])
        df = df.set_index('Aluno')
        df.to_excel('dados_alunos.xlsx')

def actions(data):
    os.system('cls')
    if not data.empty:
        print(data)

    answer = question('O que deseja fazer?\nA - adicionar um aluno\nM - modificar notas\nE - adicionar nota de exame\nR - remover aluno\nS - sair\nDigite: ', ['A', 'M', 'E', 'R', 'S'])
    if answer == 'A':
        data = calculate_grades(add_student(data))
    elif answer == 'M':
        data = calculate_grades(modify_grades(data))
    elif answer == 'E':
        data = calculate_grades(add_exam_grades(data))
    elif answer == 'R':
        data = remove(data)
    elif answer == 'S':
        return data

    print(data)

    answer = question('Deseja realizar outra ação? S/N\n', ['S', 'N'])
    if answer == 'S':
        data = actions(data)
    
    return data

def main():
    verify()
    df = pd.read_excel('dados_alunos.xlsx')
    df = actions(df)
    df = df.set_index('Aluno')
    df.to_excel('dados_alunos.xlsx')

main()
