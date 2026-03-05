import random

print('Seja muito bem-vindo ao Guess Number')
choice_number = input('Digite um número teto de desafio: ')

if choice_number.isdigit(): # retornar true se for um número ou false se for uma string
    choice_number = int(choice_number)
else: 
    print('Digite um número inteiro válido')
    quit()

random_number = random.randint(0, choice_number)

n_choices = 0

while True: 
    answer_user = input('Adivinhe o número: ')

    if answer_user.isdigit():
        answer_user = int(answer_user)
    else:
        print('Digite um número inteiro válido')
        continue
    
    n_choices += 1
    if answer_user == random_number: 
        print('Parabéns, você acertou o número!')
        break
    elif answer_user > random_number:
        print('O número é maior do que o que você digitou.')
    else:
        print('O número é menor do que o que você digitou.')

print(f'N° de tentativas: {n_choices}   | Número sorteado: {random_number}')