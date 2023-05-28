# bimaru.py: Template para implementação do projeto de Inteligência Artificial 2022/2023.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes já definidas, podem acrescentar outras que considerem pertinentes.

# Grupo 00:
# 00000 Nome1
# 00000 Nome2

import sys
import copy
from search import (
    Problem,
    Node,
    astar_search,
    breadth_first_tree_search,
    depth_first_tree_search,
    greedy_search,
    recursive_best_first_search,
)

class BimaruState:
    state_id = 0

    def __init__(self, board):
        self.board = board
        self.id = BimaruState.state_id
        BimaruState.state_id += 1

    def __lt__(self, other):
        return self.id < other.id

    # TODO: outros metodos da classe


class Board:
    """Representação interna de um tabuleiro de Bimaru."""
    def __init__(self, row, col, hints, table):
        self.row = row
        self.col = col
        self.hints = hints
        self.table = table

    def get_value(self, row: int, col: int) -> str:
        """Devolve o valor na respetiva posição do tabuleiro."""
        if (isNone(self, row, col)):
            return None
        return self.table[row][col]

    def adjacent_vertical_values(self, row: int, col: int) -> tuple([str, str]):
        """Devolve os valores imediatamente acima e abaixo,
        respectivamente (Out of bounds -> None)."""
        
        return tuple([self.get_value(row - 1, col) if row > 0 else None,
                      self.get_value(row + 1, col) if (row < len(self.row) - 1) else None])

    def adjacent_horizontal_values(self, row: int, col: int) -> tuple([str, str]):
        """Devolve os valores imediatamente à esquerda e à direita,
        respectivamente (Out of bounds -> None)."""
        
        return tuple([self.get_value(row, col - 1) if col > 0 else None,
                      self.get_value(row, col + 1) if (col < len(self.row) - 1) else None])

    @staticmethod
    def parse_instance():
        """Lê o test do standard input (stdin) que é passado como argumento
        e retorna uma instância da classe Board.

        Por exemplo:
            $ python3 bimaru.py < input_T01

            > from sys import stdin
            > line = stdin.readline().split()
        """
        row = []
        col = []
        hints = []
        table = []

        row_raw = sys.stdin.readline().strip()
        row_values = row_raw.split("\t")[1:]   
        row = [int(val) for val in row_values]

        col_raw = sys.stdin.readline().strip()
        col_values = col_raw.split("\t")[1:]
        col = [int(val) for val in col_values]

        hint_num = int(sys.stdin.readline().strip())

        for _ in range(len(row)):
            line = []
            for _ in range(len(col)):
                line.append('~')
            table.append(line)

        for _ in range(hint_num):
            hint_raw = sys.stdin.readline().strip()
            hint_values = hint_raw.split("\t")[1:]
            hint_values = [int(val) if val.isnumeric() else val for val in hint_values]
            table[hint_values[0]][hint_values[1]] = hint_values[2]
            hints.append(hint_values)
        
        return Board(row, col, hints, table)


    def print(self):
        '''Imprime a visualização externa de um tabuleiro Board'''
        for i in range(len(self.table)):
            for j in range(len(self.table[0])):
                print(self.table[i][j], end = '')
            print('\n')


class Bimaru(Problem):
    def __init__(self, board: Board):
        """O construtor especifica o estado inicial."""
        self.initial = BimaruState(board)
        pass

    def actions(self, state: BimaruState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""
        board_filled = checkForCompletedLines(state.board)
        # To do: Check for ship adjancences
        moves = []
        for i in range(len(board_filled.row)):
            for j in range(len(board_filled.col)):
                if (isNone(board, i, j)):
                    for c in "mw": # m: middle, w: water
                        moves.append(tuple([i, j, c]))
        return moves
                

    def result(self, state: BimaruState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""
        board_filled = checkForCompletedLines(state.board)
        return BimaruState(board_filled)

    def goal_test(self, state: BimaruState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas de acordo com as regras do problema."""

        pass

    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
        # TODO
        pass

    # TODO: outros metodos da classe

'''
----------------------------------------------------------------------------------------------
--------------------------- Funções Auxiliares -----------------------------------------------
----------------------------------------------------------------------------------------------
'''

def checkForCompletedLines(board: Board):
    '''Assegura que linhas ou colunas completas com peças de navios sejam preenchidas com água'''
    
    for i in range(len(board.row)):
        pieces = countRowShipPieces(board, i)
        if (board.row[i] == pieces):
            for j in range(len(board.col)):
                if (isNone(board, i, j)):
                    board.table[i][j] = '.'

    for i in range(len(board.col)):
        pieces = countColShipPieces(board, i)
        if (board.col[i] == pieces):
            for j in range(len(board.row)):
                if (isNone(board, j, i)):
                    board.table[j][i] = '.'
    return board

def countRowShipPieces(board: Board, row: int):
    
    count = 0
    for i in range(len(board.col)):
        if (isShipPiece(board.table[row][i])):
            count += 1
    return count

def countColShipPieces(board: Board, col: int):
    
    count = 0
    for i in range(len(board.row)):
        if (isShipPiece(board.table[i][col])):
            count += 1
    return count

def isShipPiece(sample: str):
    
    cell = "W.~" # Everything else is a ship
    for c in cell:
        if sample == c:
            return False
    return True

def isNone(board: Board, row: int, col: int):
    return board.table[row][col] == "~"

'''
----------------------------------------------------------------------------------------------
---------------------------------- Função Main -----------------------------------------------
----------------------------------------------------------------------------------------------
'''

if __name__ == "__main__":
    # TODO:
    # Ler o ficheiro do standard input,
    # Usar uma técnica de procura para resolver a instância,
    # Retirar a solução a partir do nó resultante,
    # Imprimir para o standard output no formato indicado.

    board = Board.parse_instance()

    print(board.row)
    print(board.col)
    print(board.hints)
    
    print('\n')
    board.print()
    print('\n')
          
    print(board.adjacent_vertical_values(3, 3))
    print(board.adjacent_horizontal_values(3, 3))

    print(board.adjacent_vertical_values(1, 0))
    print(board.adjacent_horizontal_values(1, 0))

    print(board.get_value(9, 9))
    print(board.adjacent_vertical_values(8, 5))
    print(board.adjacent_horizontal_values(8, 8))

    print('\n')

    problem = Bimaru(board)
    initial_st = BimaruState(board)

    second_st = problem.result(initial_st, "")

    print(problem.actions(second_st))

    second_st.board.print()


    '''
    print(Board.get_value(b, 9, 9))
    print(Board.adjacent_vertical_values(b, 9, 8))
    print(Board.adjacent_horizontal_values(b, 6, 0))
    '''
    pass
