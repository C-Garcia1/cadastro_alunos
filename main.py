import os 
import sqlite3


def conectar_banco():
    conexao = sqlite3.connect('sql/banco.db')
    conexao.execute("PRAGMA foreign_keys = ON")
    return conexao

def exibir_nome_programa():
    titulo = 'SISTEMA DE ALUNOS'
    linha = '-' * len(titulo)
    print(linha, titulo, linha)

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

def listar_cursos_disponiveis(): 
    conexao = conectar_banco()
    cursor = conexao.cursor()

    cursor.execute("SELECT id_curso, nome_curso FROM cursos")

    cursos_disponiveis = cursor.fetchall()
    
    print('Cursos Disponiveis:')
    for curso in cursos_disponiveis:
        print(f'\nID: {curso[0]} - Nome: {curso[1]}')
    
    conexao.close()

def cadastrar_alunos(conexao):

    cursor = conexao.cursor()
    while True:
        
        exibir_titulo('CADASTRO DE ALUNOS')

        nome_aluno = input('Informe o nome do aluno: ').strip()
        
        while True: 
            try:
                idade_aluno = int(input('Informe a idade do aluno: '))
                if idade_aluno < 17 or idade_aluno > 60:
                    print('\nNão é possivel cadastrar o aluno devido sua idade!')
                    continue
                break
            except ValueError as v:
                print(v)
                continue
            
        listar_cursos_disponiveis()
        
        while True:
            try:
                curso_cadastrar = int(input('Informe o ID do curso: '))
            except (ValueError, TypeError) as v: 
                v = 'Digite apenas números posititos!'
                print(f'\n{v}')
                continue
            
            cursor.execute("SELECT id_curso, nome_curso FROM cursos")

            cursos_disponiveis = cursor.fetchall()
            curso_encontrado = False

            for curso in cursos_disponiveis:            
                if curso_cadastrar == curso[0]:
                    nome_curso = curso[1]
                    cursor.execute("""INSERT INTO alunos (nome_aluno, idade_aluno, id_curso)
                                VALUES (?, ?, ?)
                                """, (nome_aluno, idade_aluno, curso_cadastrar))
                    conexao.commit()
                    print(f'Aluno (a) {nome_aluno} foi cadastrado com sucesso no curso de {nome_curso}!')
                    curso_encontrado = True
                    break
            
            if not curso_encontrado:
                print("\nCurso não encontrado!")
                continue
            break
                
        opcao = input('Deseja cadastrar mais alunos (S/N)? ').lower()
        if opcao == 's':
            continue
        else:
            break
            
def listar_alunos(conexao): 
    cursor = conexao.cursor()
    
    exibir_titulo('LISTA DE ALUNOS')

    cursor.execute("""
        SELECT alunos.id_aluno,
               alunos.nome_aluno,
               alunos.idade_aluno,
               cursos.nome_curso
        FROM alunos
        JOIN cursos
        ON alunos.id_curso = cursos.id_curso
    """)
    
    alunos = cursor.fetchall()
    for aluno in alunos:
        print(f'\nId: {aluno[0]} - Nome: {aluno[1]} - Idade: {aluno[2]} - Curso: {aluno[3]}')

def editar_info_alunos(conexao):
    cursor = conexao.cursor()

    while True: 
        limpar_tela()
        exibir_titulo('MODIFICAÇÃO DE DADOS')
        try: 
            id_aluno= int(input('Informe o ID do aluno:'))
        except ValueError as v: 
            print(v)
            continue

        cursor.execute("""
                        SELECT 
                            alunos.nome_aluno,
                            alunos.idade_aluno,
                            cursos.nome_curso
                        FROM alunos
                        JOIN cursos 
                        ON alunos.id_curso = cursos.id_curso
                        WHERE alunos.id_aluno = ?
                    """, (id_aluno,))

        aluno = cursor.fetchone()

        if aluno: 
            print('Aluno Encontrado!')
            print(f'\nNome: {aluno[0]} | Idade: {aluno[1]} | Curso: {aluno[2]}')
            
            nome_novo = input('Informe o nome do aluno: ')
            
            while True:
                try:
                    idade_nova = int(input('Informe a idade do aluno: '))
                    if idade_nova < 17 or idade_nova > 60:
                        print('Idade inválida!')
                        continue
                except ValueError as v: 
                    print(v)
                    continue
                break

            listar_cursos_disponiveis()
            
            while True:
                try: 
                    curso_novo = int(input('Informe o ID do curso: '))
                except ValueError: 
                    print('Erro!')
                    continue
               
                cursor.execute(
                                "SELECT 1 FROM cursos WHERE id_curso = ?",
                                (curso_novo,)
                                )

                curso_valido = cursor.fetchone()  

                if not curso_valido:
                    print("Curso não encontrado!")
                    continue
                break         
        
            cursor.execute("""UPDATE alunos 
                        SET nome_aluno = ?, idade_aluno = ?, id_curso = ?
                        WHERE id_aluno = ?
                        """, (nome_novo, idade_nova, curso_novo, id_aluno))
            conexao.commit()
            print(f'Aluno (a) {nome_novo} teve seus dados editados com SUCESSO!')

        else: 
            print('Aluno não encontrado!')
            continue
            
        opcao = input('Deseja editar mais alunos (S/N)? ').lower()
        if opcao != 's':
            break

def excluir_aluno(conexao):
    
    while True: 
        cursor = conexao.cursor()
        
        exibir_titulo('LISTA DE ALUNOS')

        cursor.execute("""
            SELECT alunos.id_aluno,
                alunos.nome_aluno,
                alunos.idade_aluno,
                cursos.nome_curso
            FROM alunos
            JOIN cursos
            ON alunos.id_curso = cursos.id_curso
        """)
        
        alunos = cursor.fetchall()
        for aluno in alunos:
            print(f'\nId: {aluno[0]} - Nome: {aluno[1]} - Idade: {aluno[2]} - Curso: {aluno[3]}')

        try: 
            id_aluno = int(input('Informe o ID do Aluno que deseja deletar: '))
        except ValueError:
            print('Erro!')
            continue
                    
        cursor.execute('''
                        SELECT 1 FROM alunos
                        WHERE id_aluno = ?
                        ''', (id_aluno,))
        
        aluno_valido = cursor.fetchone()

        if not aluno_valido:
            print('Aluno não encontrado.')
            confirmacao = input('Deseja tentar novamente? (S/N)').lower().strip()
            if confirmacao == 's':
                continue
            else:
                break

        confirmacao = input('Tem certeza que deseja deletar? (S/N)').lower().strip()
        if confirmacao != 's':
            print('Operação cancelada!')
            continue

        cursor.execute('''
                            DELETE FROM alunos
                            WHERE id_aluno = ?
                            ''', (id_aluno,))
        
        conexao.commit()
        print('Aluno deletado com SUCESSO!')
            
        opcao = input('Deseja excluir mais alunos? (S/N): ').lower()
        if opcao != 's':
            break
        

def menu_principal(conexao):

    while True:
        try:
            print('\n1- Cadastrar aluno')
            print('2- Listar alunos')
            print('3- Editar informações do aluno')
            print('4- Excluir aluno')
            print('5- Sair\n')
            escolha = int(input('Escolha uma das opções:').strip())
            
            if escolha == 1: 
                cadastrar_alunos(conexao)
                voltar_ao_menu_principal()
            elif escolha == 2: 
                listar_alunos(conexao)
                voltar_ao_menu_principal()
            elif escolha == 3: 
                editar_info_alunos(conexao)
                voltar_ao_menu_principal()
            elif escolha == 4: 
                excluir_aluno(conexao)
                voltar_ao_menu_principal()
            elif escolha == 5: 
                print('Encerrando Programa...')
                break
            else: 
                print('Erro! Opção Inválida!')
        except ValueError as v:
            v = 'Erro! Apenas números são aceitos!'
            print(v) 

     

def main():
        conexao = conectar_banco()
        try:
            limpar_tela()
            exibir_nome_programa()
            menu_principal(conexao)
        finally:
            conexao.close()


if __name__ == "__main__":
    main()


