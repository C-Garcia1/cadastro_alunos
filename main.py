import os 
import random

alunos = [  
            {'id': 123, 'nome': 'Luiz Carlos Dos Santos', 'idade': 18, 'curso': 'Engenharia de Software'},
            {'id': 321, 'nome': 'Brenda Pontes', 'idade': 21, 'curso': 'Redes de Computadores'},
            {'id': 213, 'nome': 'Diego Gonçalves', 'idade': 42, 'curso': 'Análise e Desenvolvimento de Sistemas'}
            ]

id_disponiveis = list(range(100, 1000))

cursos_disponiveis = ['Análise e Desenvolvimento de Sistemas', 'Ciência da Computação', 'Engenharia de Computação', 'Engenharia de Software', 'Redes de Computadores']

def exibir_nome_programa():
    titulo = 'SISTEMA DE ALUNOS'
    linha = '-' * len(titulo)
    print(linha, titulo, linha)

def exibir_menu():
    print('\n1- Cadastrar anluno')
    print('2- Listar alunos')
    print('3- Editar aluno')
    print('4- Excluir aluno')
    print('5- Sair\n')

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

def exibir_titulo(opcao):
    limpar_tela()
    linha = '-' *len(opcao)
    print(linha, opcao, linha)
    print()
    
def voltar_ao_menu_principal():
    input('\nPressione uma tecla para retornar ao menu principal: ')
    main()

def cadastrar_alunos():
    exibir_titulo('CADASTRO DE ALUNOS')

    id_aluno = random.choice(id_disponiveis)
    id_disponiveis.remove(id_aluno)


    nome_aluno = input('Informe o NOME COMPLETO do aluno:')
    
    idade_aluno = int(input('Informe a idade do aluno:'))
    if idade_aluno < 17:
        print('Este aluno não pode ser cadastrado devido sua idade.')


    curso_aluno = input('Informe o curso do aluno:')
    
    if curso_aluno in cursos_disponiveis:
        alunos.append({'id': id_aluno,'nome': nome_aluno, 'idade': idade_aluno, 'curso': curso_aluno})
        print(f'O Aluno(a) {nome_aluno} de ID {id_aluno} foi cadastrado no curso de {curso_aluno} com sucesso!')
    else: 
        print('Este curso não está disponivel')


def listar_alunos(): 
    exibir_titulo('LISTA DE ALUNOS')
    for i in alunos:
        id_aluno = i['id']
        nome_aluno = i['nome']
        idade_aluno = i['idade']
        curso_aluno = i['curso']

        print(f'\nId: {id_aluno} - Nome: {nome_aluno} - Idade: {idade_aluno} - Curso: {curso_aluno}')


def escolher_opcao():
    try:
        escolha = int(input('Escolha uma das opções:').strip())
        
        if escolha == 1: 
            cadastrar_alunos()
            voltar_ao_menu_principal()
        elif escolha == 2: 
            listar_alunos()
            voltar_ao_menu_principal()
        elif escolha == 3: 
            print('Editando')
        elif escolha == 4: 
            print('Excluindo')
        elif escolha == 5: 
            print('Encerrando Programa...')
            
        else: 
            print('Erro! Opção Inválida!')
    except ValueError as v:
        v = 'Erro! Apenas números são aceitos!'
        print(v) 

     

def main():
        limpar_tela()
        exibir_nome_programa()
        exibir_menu()
        escolher_opcao()


if __name__ == "__main__":
    main()


