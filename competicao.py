# Funciona para 4 participantes ou mais.

import json

def load(filename):
    try:
        dataFile = open(filename + '.json', 'r')
        data = json.loads(dataFile.read())
        dataFile.close()
        return data
    except:
        return None

def save(filename, data):
    dataFile = open(filename + '.json', 'w')
    dataFile.write(json.dumps(data))
    print('\n\n--- Progress Saved ---\n\n')
    dataFile.close()

def askFor(mensagem):
    while True:
        command = input(f'\n\n{mensagem} (Y/N)\n')
        if command.lower() in ['y','yes']:
            return True
        elif command.lower() in ['n','no']:
            return False

def printMatches(lista):
    print('\nPartidas da próxima fase:\n')
    for i in range(len(lista) // 2):
        print(f'\nPartida {i+1}: [{lista[i] if not lista[i] is None else "_"}] versus [{lista[-1-i] if not lista[-1-i] is None else "_"}].')

loadRetorno = load('competicao')

if loadRetorno is None:
    import math
    import random

    numeroParticipantes = int(input('Insira o número de participantes: '))

    torneioBase = 2**(math.ceil(math.log2(numeroParticipantes)))

    A, B, C, D = ([], [], [], [])

    toGrupo = {0: 'A', 1: 'B', 2: 'C', 3: 'D'}

    size = {'A': torneioBase//4,
            'B': torneioBase//4,
            'C': min(torneioBase//4, numeroParticipantes - torneioBase//2),
            'D': max(0, numeroParticipantes - 3*torneioBase//4)}

    for i, grupo in enumerate([A, B, C, D]):
        print(f'\nInsira os {size[toGrupo[i]]} integrantes do grupo {toGrupo[i]} (não se preocupe em randomizar):\n')

        for j in range(size[toGrupo[i]]):
            grupo.append(input(''))
        
        random.shuffle(grupo)

    faseWinners = 1
    faseLosers = 1 if numeroParticipantes > 3*torneioBase//4 else 0

    winners = []
    losers = []

    for grupo in [A, B, C, D]:
        for i in range(torneioBase//4):
            if len(grupo) > i:
                winners.append(grupo[i])
            else:
                winners.append(None)

    save('competicao', (faseWinners, faseLosers, winners, losers))
else:
    faseWinners, faseLosers, winners, losers = loadRetorno

while len(winners) + len(losers) > 2:
    if len(losers) >= len(winners):
        if faseLosers > 0:
            printMatches(losers)
            if not askFor(f'Começar fase {faseLosers if len(losers) > 2 or len(winners) != 1 else "final"} da Losers Bracket?'):
                exit(0)
        else:
            print('\n\nNão existem perdedores o suficiente para ser necessário fazer uma fase da Losers Bracket, avançando...')

        newLosers = []
        for i in range(len(losers) // 2):
            if losers[i] is None:
                if faseLosers > 0:
                    print(f'\nQue legal, {losers[-1-i]} avança imediatamente de fase.')
                newLosers.append(losers[-1-i])
            elif losers[-1-i] is None:
                if faseLosers > 0:
                    print(f'\nQue legal, {losers[i]} avança imediatamente de fase.')
                newLosers.append(losers[i])
            else:
                print(f'\nFaça {losers[i]} enfrentar {losers[-1-i]}.')
                newLosers.append(input('Qual o nome do vencedor? '))
        losers = newLosers

        faseLosers += 1

    else:
        printMatches(winners)
        if not askFor(f'Começar fase {faseWinners if len(winners) > 2 else "final"} da Winners Bracket?'):
            exit(0)

        newWinners = []
        for i in range(len(winners) // 2):
            if winners[-1-i] is None:
                print(f'\nQue legal, {winners[i]} avança imediatamente de fase.')
                newWinners.append(winners[i])
                losers.append(None)
            else:
                print(f'\nFaça {winners[i]} enfrentar {winners[-1-i]}.')
                newWinners.append(input('Qual o nome do vencedor? '))
                losers.append(input('E do perdedor? '))
        winners = newWinners

        faseWinners += 1
    
    save('competicao', (faseWinners, faseLosers, winners, losers))

print(f'\nA grande final é entre {winners[0]} e {losers[0]}.')

print(f'\nSe {winners[0]} vencer uma vez, {winners[0]} é campeão.')
print(f'Por outro lado, se {losers[0]} vencer duas vezes, {losers[0]} é campeão.')

input('\n\nEnter para encerrar execução.')
