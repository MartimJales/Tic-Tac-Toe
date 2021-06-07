# Função que verifica se alguém ganhou o jogo


def check_winner(game):
    # Contagem dos espaços vazios
    zeros = 0
    # Diagonais:
    sum_dp = game[0][0] + game[1][1] + game[2][2]
    sum_ds = game[0][2] + game[1][1] + game[2][0]
    if (sum_ds == -3 or sum_dp == -3):
        return -1  # PC win
    if (sum_ds == 3 or sum_dp == 3):
        return 1  # Human win
    # Linhas & Colunas:
    sum_l, sum_c = 0, 0
    for i in range(3):
        for j in range(3):
            zeros += 1
            sum_l += game[i][j]
            sum_c += game[j][i]
        if sum_l == 3 or sum_c == 3:
            return 1  # Human win
        if sum_l == -3 or sum_c == -3:
            return -1  # PC win
        sum_l, sum_c = 0, 0
    return 0  # Jogo continua a correr!

# Funbção que verifica se o tabuleiro está totalmente preenchido


def check_fill(game):
    for i in range(3):
        for j in range(3):
            if game[i][j] == 0:
                return False  # existe um espaço vazio
    return True

# Função que encontra a jogada ideal


def best_move(game):
    best = 3
    coords = (-1, -1)
    for i in range(3):
        for j in range(3):
            if game[i][j] == 0:
                game[i][j] = -1
                score = minimax(game, 10, -3, 3, True)
                game[i][j] = 0
                if score < best:
                    best = score
                    coords = (i, j)
    game[coords[0]][coords[1]] = -1

# Função minimax


def minimax(game, depth, alpha, beta, human):
    winner = check_winner(game)
    # Penso que aqui até posso retirar a condição do check_fill!
    if check_fill(game) or depth == 0 or winner != 0:
        return winner  # Retorna o resultado final desse estado
    # HUMAN A JOGAR
    if human:
        maxEval = -3
        for i in range(3):
            for j in range(3):
                # Verifica se está vazio
                if game[i][j] == 0:
                    # Cria estado "hipotético" novo
                    game[i][j] = 1
                    # Aplica minimax a eval
                    eval = minimax(game, depth-1, alpha, beta, False)
                    # Recupera o estado anterior
                    game[i][j] = 0
                    maxEval = max(maxEval, eval)
                    # Função para reduzir computação - Alpha prune
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        break
        return maxEval
    # AI A JOGAR
    else:
        minEval = 3
        for i in range(3):
            for j in range(3):
                # Verifica se está vazio
                if game[i][j] == 0:
                    # Cria estado "hipotético" novo
                    game[i][j] = -1
                    # Aplica minimax a eval
                    eval = minimax(game, depth-1, alpha, beta, True)
                    # Recupera o estado anterior
                    game[i][j] = 0
                    minEval = min(eval, minEval)
                    # Função para reduzir computação - Alpha prune
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break
        return minEval
