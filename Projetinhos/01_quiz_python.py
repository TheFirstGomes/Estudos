print('Seja bem-vindo ao Quiz do Luan!')
answer_user = input('Quer começar (S/N): ')

if answer_user.upper() != 'S': 
    quit()

score = 0

print('Começando o quiz...')
print('Quem desenvoveu o jogo Grand Theft Auto (GTA)?\n(A) Rockstar Games\n(B) Electronic Arts\n(C) Ubisoft\n(D) Activision\n')
answer_1 = input('Resposta: ')

if answer_1.upper() == 'A':
    print('Correto')
    score += 1
else:
    print('Incorreto')

print('Qual o protagonista do jogo The Legend of Zelda?\n(A) Link\n(B) Zelda\n(C) Ganon\n(D) Epona\n')
answer_2 = input('Resposta: ')
if answer_2.upper() == 'A':
    print('Correto')
    score += 1
else:
    print('Incorreto')

print(f'Seu score final é: {score}/2')