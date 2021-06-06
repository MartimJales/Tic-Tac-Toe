import numpy as np
from numpy.core.arrayprint import dtype_short_repr
from os import system


def main():
    game = np.zeros((3, 3), dtype=int)
    game[0][0] = -1
    play = 1
    while 1:
        winner = check_winner(game)
        if winner == 1:
            print('Humano ganhou!')
            print_game(game)
            break
        if winner == 2:
            print('PC ganhou')
            print_game(game)
            break
        print_game(game)
        print('Coloque as coordenadas onde deseja jogar:')
        line = int(input('Linha: '))
        column = int(input('Coluna: '))
        game[line][column] = 1
        attack = check_attack(game)
        if attack != 0:
            go_attack(game, attack)  # Codigo para encontrar o killer spot
        else:
            defense = check_defense(game, line, column)
            if defense == 0:
                if check_corner(line, column):
                    if play == 1:
                        go_corner(game)
                    print('Jogou no canto!')
                elif (check_center(line, column)):
                    print('Jogou no centro')
                    if play == 1:
                        game[2][2] = -1
                    pass
                else:
                    if play == 1:
                        game[1][1] = -1
                    print('Jogou no meio')
            else:
                go_defense(game, defense)
        play += 1
    # system('clear')
    print('Saiu do ciclo')

# Funções par afazer verificiações do estado do jogo


def check_corner(line, column):
    if (line == 0 or line == 2):
        if (column == 0 or column == 2):
            return True
    return False


def check_center(line, column):
    if (line == 1 and column == 1):
        return True
    return False


def check_winner(game):
    # Diagonais:
    sum_dp = game[0][0] + game[1][1] + game[2][2]
    sum_ds = game[0][2] + game[1][1] + game[2][0]
    if (sum_ds == -3 or sum_dp == -3):
        return 2  # PC win
    if (sum_ds == 3 or sum_dp == 3):
        return 1  # Human win
    # Linhas & Colunas:
    sum_l, sum_c = 0, 0
    for i in range(3):
        for j in range(3):
            sum_l += game[i][j]
            sum_c += game[j][i]
        if sum_l == 3 or sum_c == 3:
            return 1  # Human win
        if sum_l == -3 or sum_c == -3:
            return 2  # PC win
        sum_l, sum_c = 0, 0
    return 0  # Jogo continua a correr!


def check_attack(game):
    sum_dp = game[0][0] + game[1][1] + game[2][2]
    sum_ds = game[0][2] + game[1][1] + game[2][0]
    if sum_dp == -2:
        return 1  # Código atacar na diagonal principal
    elif sum_ds == -2:
        return 2  # Código atacar na diagonal secundária
    # Linhas & Colunas:
    sum_l, sum_c = 0, 0
    for i in range(3):
        for j in range(3):
            sum_l += game[i][j]
            sum_c += game[j][i]
        if sum_l == -2:
            return 10 + i  # Código para atacar na linha "i"
        elif sum_c == -2:
            return 20 + i  # Códdigo para atacar na coluna "i"
        sum_l, sum_c = 0, 0
    return 0  # Tudo suave!

# Esta lógica está muito pesada a nivel de computação porque eu estou a considerar a matriz toda e precisava de considerar apenas o estado após a jogada do humano!


def check_defense(game, line, col):
    sum_dp = game[0][0] + game[1][1] + game[2][2]
    sum_ds = game[0][2] + game[1][1] + game[2][0]
    if sum_dp == 2:
        return 1  # Código para ter cuidado com diagonal principal
    elif sum_ds == 2:
        return 2  # Código para ter cuidado com diagonal secundária
    # Linhas & Colunas:
    sum_l, sum_c = 0, 0
    for i in range(3):
        for j in range(3):
            sum_l += game[i][j]
            sum_c += game[j][i]
        if sum_l == 2:
            return 10 + i  # Código para ter cuidado com linha "i"
        elif sum_c == 2:
            return 20 + i  # Códdigo para ter cuidado com a coluna "i"
        sum_l, sum_c = 0, 0
    return 0  # Tudo suave!

# Função para enocntrar ameaças..


# Função para imprimir o estado do jogo no terminal


def print_game(game):
    for i in range(3):
        for j in range(3):
            if (game[i][j] == 0):
                print(' ', end='')
            elif (game[i][j] == 1):
                print('X', end='')
            else:
                print('O', end='')
            if not(j == 2):
                print('|', end='')
        print()
        print('~~~~~~')

# Funções para alterar  estado do jogo


def go_corner(game):
    if game[0][0] == 0:
        game[0][0] = -1
    elif game[2][0] == 0:
        game[2][0] = -1
    elif game[0][2] == 0:
        game[0][2] = -1
    elif game[2][2] == 0:
        game[2][2] = -1
    else:
        print('Deu merda da grossa')
    return


# Aqui tenho que ver a matriz toda, considerando que o jogador humano pode cometer erros e não ser acertivo na jogada que faz:


# Função para encontrar o killer_move

def go_attack(game, attack):
    for i in range(3):
        if attack == 1:
            if game[i][i] == 0:
                game[i][i] = -1
                break
            if i == 2:
                print('go_attack - D Principal com o i: ' + str(i))
        elif attack == 2:
            if game[i][2-i] == 0:
                game[i][2-i] = -1
                break
            if i == 2:
                print('go_attack - D Secundária')
        elif attack == 10 or attack == 11 or attack == 12:
            if game[attack % 10][i] == 0:
                game[attack % 10][i] = -1
                break
            if i == 2:
                print('go_attack - Linhas')
        elif attack == 20 or attack == 21 or attack == 22:
            if game[i][attack % 20] == 0:
                game[i][attack % 20] = -1
                break
            if i == 2:
                print('go_attack - Colunas')
        else:
            print('Deu merda na função go_attack')


def go_defense(game, defense):
    for i in range(3):
        if defense == 1:
            if game[i][i] == 0:
                game[i][i] = -1
                break
            if i == 2:
                print('go_attack - D Principal com o i: ' + str(i))
        elif defense == 2:
            if game[i][2-i] == 0:
                game[i][2-i] = -1
                break
            if i == 2:
                print('go_attack - D Secundária')
        elif defense == 10 or defense == 11 or defense == 12:
            if game[defense % 10][i] == 0:
                game[defense % 10][i] = -1
                break
            if i == 2:
                print('go_attack - Linhas')
        elif defense == 20 or defense == 21 or defense == 22:
            if game[i][defense % 20] == 0:
                game[i][defense % 20] = -1
                break
            if i == 2:
                print('go_attack - Colunas')
        else:
            print('Deu merda na função go_attack')


main()
