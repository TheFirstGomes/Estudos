# imports necessários
import os

# Variáveis globais
restaurantes = ['Lasanha', 'Sardinha', 'Pizza']

# Menus
def exibir_nome_programa():
    print('''

    ██████████████████████████████████████████████████████████████████████████
    █─▄▄▄▄██▀▄─██▄─▄─▀█─▄▄─█▄─▄▄▀███▄─▄▄─█▄─▀─▄█▄─▄▄─█▄─▄▄▀█▄─▄▄─█─▄▄▄▄█─▄▄▄▄█
    █▄▄▄▄─██─▀─███─▄─▀█─██─██─▄─▄████─▄█▀██▀─▀███─▄▄▄██─▄─▄██─▄█▀█▄▄▄▄─█▄▄▄▄─█
    ▀▄▄▄▄▄▀▄▄▀▄▄▀▄▄▄▄▀▀▄▄▄▄▀▄▄▀▄▄▀▀▀▄▄▄▄▄▀▄▄█▄▄▀▄▄▄▀▀▀▄▄▀▄▄▀▄▄▄▄▄▀▄▄▄▄▄▀▄▄▄▄▄▀
    ''')

def exibir_opcoes():
    print('1. Cadastrar restaurante')
    print('2. Listar restaurante')
    print('3. Ativar restaurante')
    print('4. Sair\n')

def escolher_opcao():
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
    input('\nDigite uma tecla para voltar ao menu: ')
    os.system('cls')
    main()

def exibir_texto_titulo(texto):
    os.system('cls')
    print(f'{texto}\n')

# Processos internos:         
def finalizar_app(): 
    exibir_texto_titulo('Encerrando o sistema, obrigado por utilizar nossos sistemas!')

def cadastrar_restaurante():
    exibir_texto_titulo('Cadastrar restaurantes')

    nome_do_restaurante = str(input('Digite o nome do restaurante que deseja cadastrar: '))
    restaurantes.append(nome_do_restaurante)

    print(f'O restaurante {nome_do_restaurante} foi cadastrado com sucesso!')
    menu_principal()

def listar_restaurante():
    exibir_texto_titulo('Listar restaurantes')

    for _, restaurante in enumerate(restaurantes): 
        print(f'{_+1}. {restaurante}')
    
    menu_principal()

def ativar_restaurante():
    exibir_texto_titulo('Ativar restaurantes')

# Função principal
def main():
    exibir_nome_programa()
    exibir_opcoes()
    escolher_opcao()

if __name__ == '__main__':
    main()
    