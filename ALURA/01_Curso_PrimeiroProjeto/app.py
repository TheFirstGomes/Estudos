# imports necessários
import os

# Variáveis globais
restaurantes = [
    {'nome': 'Praça', 'categoria':'Japonesa', 'ativo': False},
    {'nome': 'Pizza Suprema', 'categoria':'Pizza', 'ativo': True}, 
    {'nome': 'Cantina', 'categoria':'Italiano', 'ativo': False} 
    ]

# Menus
def exibir_nome_programa():
    '''
    Mostrar o título criado no site fsymbols.com
    '''

    print('''

    ██████████████████████████████████████████████████████████████████████████
    █─▄▄▄▄██▀▄─██▄─▄─▀█─▄▄─█▄─▄▄▀███▄─▄▄─█▄─▀─▄█▄─▄▄─█▄─▄▄▀█▄─▄▄─█─▄▄▄▄█─▄▄▄▄█
    █▄▄▄▄─██─▀─███─▄─▀█─██─██─▄─▄████─▄█▀██▀─▀███─▄▄▄██─▄─▄██─▄█▀█▄▄▄▄─█▄▄▄▄─█
    ▀▄▄▄▄▄▀▄▄▀▄▄▀▄▄▄▄▀▀▄▄▄▄▀▄▄▀▄▄▀▀▀▄▄▄▄▄▀▄▄█▄▄▀▄▄▄▀▀▀▄▄▀▄▄▀▄▄▄▄▄▀▄▄▄▄▄▀▄▄▄▄▄▀
    ''')

def exibir_opcoes():
    '''
    Exibir as opções do menu
    '''

    print('1. Cadastrar restaurante')
    print('2. Listar restaurante')
    print('3. Ativar restaurante')
    print('4. Sair\n')

def escolher_opcao():
    '''
    Função para escolha da opção do menu de opções, e utilizando do match para chamar a função 
    específica
    '''

    while True: 
        try:
            opcao_escolhida = int(input('Escolha uma opção: '))
        except ValueError: 
            os.system('cls')
            main()
        else:
            match opcao_escolhida: 
                case 1: 
                    cadastrar_restaurante()
                case 2: 
                    listar_restaurante()
                case 3: 
                    ativar_restaurante()
                case 4: 
                    finalizar_app()
                case _: 
                    print('\nOpção inválida')
                    input("Digite uma tecla para voltar ao menu: ")
                    os.system('cls')
                    main()
            break

def menu_principal():
    '''
    Função para voltar ao menu principal e limpar a tela
    '''

    input('\nDigite uma tecla para voltar ao menu: ')
    os.system('cls')
    main()

def exibir_texto_titulo(texto):
    '''
    Função para imprimir o subtitulo de cada função abaixo com separados de *
    '''
    
    os.system('cls')
    linha = '*' * (len(texto))
    print(f'{linha}\n{texto}\n{linha}\n')

# Processos internos:         
def finalizar_app(): 
    '''
    Usado para encerrar o programa
    '''

    exibir_texto_titulo('Encerrando o sistema, obrigado por utilizar nossos sistemas!')

def cadastrar_restaurante():
    '''
    Cadastro de restaurantes na lista restaurantes[]

    Inputs: 
    -> nome do restaurante
    -> categoria

    Outputs: 
    -> Adiciona um novo restaurante e sua categoria na lista de restaurantes
    '''

    exibir_texto_titulo('Cadastrar restaurantes')

    nome_do_restaurante = str(input('Digite o nome do restaurante que deseja cadastrar: '))
    categoria = str(input(f'Digite o nome da categoria do restaurante {nome_do_restaurante}: '))
    restaurantes.append({'nome': nome_do_restaurante, 'categoria':categoria, 'ativo':False})

    print(f'O restaurante {nome_do_restaurante} foi cadastrado com sucesso!')
    menu_principal()

def listar_restaurante():
    '''
    Lista o nome dos restaurantes, juntamente da sua categoria e seu status (Ativado/Desativado)
    '''

    exibir_texto_titulo('Listar restaurantes')

    print(f"{'Nome do Restaurante'.ljust(23)} | {'Categoria'.ljust(20)} | {'Status'}")
    for _, restaurante in enumerate(restaurantes): 
        print(f"{_+1}. {restaurante['nome'].ljust(20)} | {restaurante['categoria'].ljust(20)} | {'Ativado' if restaurante['ativo'] else 'Desativado'}")
    
    menu_principal()

def ativar_restaurante():
    '''
    Usado para mudar a flag do restaurante de False para True ou vice-versa
    '''

    exibir_texto_titulo('Ativar restaurantes')
    nome_restaurante = str(input('Digite o nome do restaurante que deseja alterar o estado: '))
    restaurante_encontrado = False 

    for restaurante in restaurantes: 
        if nome_restaurante == restaurante['nome']:
            restaurante_encontrado = True
            restaurante['ativo'] = not restaurante['ativo']
            mensagem = f'O restaurante {nome_restaurante} foi ativado com sucesso!' if restaurante['ativo'] else f'O restaurante foi desativo com sucesso!'
            print(mensagem)

    if not restaurante_encontrado:
        print('Restaurante não foi encontrado')

    menu_principal()

# Função principal
def main():
    '''
    Função para encapsular toda a lógica dos componentes acima para rodar o programa final
    '''
    exibir_nome_programa()
    exibir_opcoes()
    escolher_opcao()

if __name__ == '__main__':
    main()
    