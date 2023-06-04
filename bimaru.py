# bimaru.py: Template para implementação do projeto de Inteligência Artificial 2022/2023.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes já definidas, podem acrescentar outras que considerem pertinentes.

# Grupo 35:
# 92552 Rodrigo Miguel Machado Santos
# 99192 Cláudio Cohen Campos

import sys
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
    def __init__(self, row, col, hints, table, boats_remaining):
        self.row = row
        self.col = col
        self.hints = hints
        self.table = table
        self.boats_remaining = boats_remaining

    def get_value(self, row: int, col: int) -> str:
        """Devolve o valor na respetiva posição do tabuleiro."""
        if (isNone(self, row, col)):
            return None
        elif (self.table[row][col] == "."):
            return 'w'
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
    
    def nBoatsOfSize(boat_size: int):
        """Verifica quantos barcos de tamanho 'boat_size' estão presentes na tabela"""

        

    def fillCell(self, row: int, col: int, move: str):
        """Preenche uma posição no tabuleiro, a posição a preencher está vazia inicialmente (None)"""

        if (not self.insideBoardLimits(row, col)): return
        if (self.get_value(row, col) != None): return
        
        if (move == 'w'):
            self.table[row][col] = '.'
        else:
            self.table[row][col] = move

        return
    
    def copy(self):
        """Copia os atributos de Board para uma nova referência Board"""

        row_copy = self.row.copy()
        col_copy = self.col.copy()
        hints_copy = []
        table_copy = []
        boats_remaining_copy = []

        for hint in self.hints:
            hints_copy.append(hint.copy())

        for row in self.table: 
            table_copy.append(row.copy())

        for boat in self.boats_remaining: 
            boats_remaining_copy.append(boat.copy())

        return Board(row_copy, col_copy, hints_copy, table_copy, boats_remaining_copy)

    def insideBoardLimits(self, row: int, col: int):
         """Inspeciona limites da tabela"""
         return row >= 0 and col >= 0 and row < len(self.row) and col < len(self.col)
    
    def print(self):
        """Imprime a visualização externa de um tabuleiro Board"""
        for i in range(len(self.table)):
            for j in range(len(self.table[0])):
                print(self.table[i][j], end = '')
            print('\n')

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
        boats_remaining = [[1, 1, 1, 1], [2, 2, 2], [3, 3], [4]]

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
            hints.append(hint_values)
            table[hint_values[0]][hint_values[1]] = hint_values[2]

            # Tratar de imediato os casos dos barcos de tamanho 1
            if (hint_values[2] == 'C'):
                boats_remaining[0].pop()
        
        return Board(row, col, hints, table, boats_remaining)



class Bimaru(Problem):
    def __init__(self, board: Board):
        """O construtor especifica o estado inicial."""
        self.initial = BimaruState(board)

    def actions(self, state: BimaruState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""
        moves = checkLargestBoat(state.board.copy())
        return moves
                
    def result(self, state: BimaruState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""
        board_played = state.board.copy()
        fillLargestBoat(board_played, action) # board_played passado por referência
        return BimaruState(board_played)

    def goal_test(self, state: BimaruState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas de acordo com as regras do problema."""
        return len(state.board.boats_remaining) == 0 and countEmptyCells(state.board) == 0

    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
        # TODO
        pass

    # TODO: outros metodos da classe

"""
----------------------------------------------------------------------------------------------
--------------------------- Funções Auxiliares -----------------------------------------------
----------------------------------------------------------------------------------------------
"""

def checkLargestBoat(board: Board):
    
    fillCompletedLines(board)
    fillAdjacents(board)
    largest_boat_yet = removeBoat(board)

    moves = []

    # Verificar existência de espaços horizontais para hipóteses de colocação do maior barco até agora
    for i in range(len(board.row)):
        count_ship_size = 0
        for j in range(len(board.col)):
            if (board.get_value(i, j) in [None] + [c for c in "LRM"]):

                if (board.get_value(i, j) == None):
                    count_ship_size += 1

                elif (board.get_value(i, j) == 'L'):
                    count_ship_size = 1

                elif (board.get_value(i, j) == 'R'):
                    if (largest_boat_yet >= 2 and count_ship_size == largest_boat_yet - 1):
                        count_ship_size += 1
                    else:
                        count_ship_size = 0

                elif (board.get_value(i, j) == 'M' and
                      board.adjacent_horizontal_values(i, j)[0] != '.' and
                      board.adjacent_horizontal_values(i, j)[1] != '.' and
                      j != 0 and j!= len(board.col) -1
                      ):
                      count_ship_size += 1

                if (largest_boat_yet == 4 and
                    count_ship_size >= 4 and
                    board.row[i] - countRowShipPieces(board, i) >= 4
                    ):
                    moves.append([(i, j - 3, 'l'), (i, j - 2, 'm'), (i, j - 1, 'm'), (i, j, 'r')])

                elif (largest_boat_yet == 3 and
                      count_ship_size >= 3 and
                      board.row[i] - countRowShipPieces(board, i) >= 3
                      ):
                      moves.append([(i, j - 2, 'l'), (i, j - 1, 'm'), (i, j, 'r')])
                          
                elif (largest_boat_yet == 2 and
                      count_ship_size >= 2 and
                      board.row[i] - countRowShipPieces(board, i) >= 2
                      ):
                      moves.append([(i, j - 1, 'l'), (i, j, 'r')])

                elif (largest_boat_yet == 1 and
                      count_ship_size >= 1 and
                      board.row[i] - countRowShipPieces(board, i) >= 1 and
                      board.adjacent_horizontal_values(i, j)[0] == 'w' and
                      board.adjacent_horizontal_values(i, j)[1] == 'w' and
                      board.adjacent_vertical_values(i, j)[0] == 'w' and
                      board.adjacent_vertical_values(i, j)[1] == 'w'
                      ):
                      moves.append([(i, j, 'c')])     
            else:
                count_ship_size = 0
    
    # Verificar existência de espaços verticais para hipóteses de colocação do maior barco até agora
    for i in range(len(board.col)):
        count_ship_size = 0
        for j in range(len(board.row)):
            if (board.get_value(j, i) in [None] + [c for c in "TBM"]):

                if (board.get_value(j, i) == None):
                    count_ship_size += 1

                elif (board.get_value(j, i) == 'T'):
                    count_ship_size = 1

                elif (largest_boat_yet >= 2 and board.get_value(j, i) == 'B'):
                    if (count_ship_size == largest_boat_yet - 1):
                        count_ship_size += 1
                    else:
                        count_ship_size = 0

                elif (board.get_value(j, i) == 'M' and 
                      board.adjacent_vertical_values(j, i)[0] != '.' and
                      board.adjacent_vertical_values(j, i)[1] != '.' and
                      j != 0 and j!= len(board.row) - 1
                      ):
                      count_ship_size += 1

                if (largest_boat_yet == 4 and
                    count_ship_size >= 4 and
                    board.col[i] - countColShipPieces(board, i) >= 4):
                        moves.append([(j - 3, i, 't'), (j - 2, i, 'm'), (j - 1, i, 'm'), (j, i, 'b')])

                elif (largest_boat_yet == 3 and
                      count_ship_size >= 3 and
                      board.col[i] - countColShipPieces(board, i) >= 3
                      ):
                      moves.append([(j - 2, i, 't'), (j - 1, i, 'm'), (j, i, 'b')])

                elif (largest_boat_yet == 2 and
                      count_ship_size >= 2 and
                      board.col[i] - countColShipPieces(board, i) >= 2
                      ):
                      moves.append([(j - 1, i, 't'), (j, i, 'b')])

                elif (largest_boat_yet == 1 and
                      count_ship_size >= 1 and
                      board.col[i] - countColShipPieces(board, i) >= 1 and
                      board.adjacent_horizontal_values(j, i)[0] == 'w' and
                      board.adjacent_horizontal_values(j, i)[1] == 'w' and
                      board.adjacent_vertical_values(j, i)[0] == 'w' and
                      board.adjacent_vertical_values(j, i)[1] == 'w'
                      ):
                      moves.append([(j, i, 'c')])
            else:
                count_ship_size = 0

    return moves

def fillLargestBoat(board: Board, boat):

    for move in boat:

        row = move[0]
        col = move[1]
        step = move[2]

        if (board.table[row][col].isupper()): continue
        
        board.fillCell(row, col, step)
    
    fillCompletedLines(board)
    fillAdjacents(board)
    removeBoat(board)
    
    return
    

def fillAdjacents(board: Board):

    for i in range(len(board.row)):
        for j in range(len(board.col)):
            if (board.get_value(i, j) != None and board.get_value(i, j) in "TMLRBCtmlrbc"):

                if (board.get_value(i, j) in "Tt"):
                    for i_offset in [-1, 0, 1]:
                        for j_offset in [-1, 1]:
                            board.fillCell(i + i_offset, j + j_offset, 'w')
                    board.fillCell(i - 1, j, "w")

                elif (board.get_value(i, j) in "Mm"):
                    for i_offset in [-1, 1]:
                        for j_offset in [-1, 1]:
                            board.fillCell(i + i_offset, j + j_offset, 'w')

                elif (board.get_value(i, j) in "Ll"):
                    for i_offset in [-1, 1]:
                        for j_offset in [-1, 0, 1]:
                            board.fillCell(i + i_offset, j + j_offset, 'w')
                    board.fillCell(i , j - 1, "w")

                elif (board.get_value(i, j) in "Rr"):
                    for i_offset in [-1, 1]:
                        for j_offset in [-1, 0, 1]:
                            board.fillCell(i + i_offset, j + j_offset, 'w')
                    board.fillCell(i , j + 1, "w")

                elif (board.get_value(i, j) in "Bb"):
                    for i_offset in [-1, 0, 1]:
                        for j_offset in [-1, 1]:
                            board.fillCell(i + i_offset, j + j_offset, 'w')
                    board.fillCell(i + 1, j, "w")

                elif (board.get_value(i, j) in "Cc"):
                    for i_offset in [-1, 0, 1]:
                        for j_offset in [-1, 0, 1]:
                            if (i_offset == 0 and j_offset == 0): continue
                            board.fillCell(i + i_offset, j + j_offset, 'w')
    return

def fillCompletedLines(board: Board):
    """Assegura que linhas ou colunas completas com peças de navios sejam preenchidas com água"""

    # Verifica para cada linha da tabela
    for i in range(len(board.row)):
        pieces = countRowShipPieces(board, i)
        if (board.row[i] == pieces):
            for j in range(len(board.col)):
                if (isNone(board, i, j)):
                    board.fillCell(i, j, 'w')

    # Verifica para cada coluna da tabela
    for i in range(len(board.col)):
        pieces = countColShipPieces(board, i)
        if (board.col[i] == pieces):
            for j in range(len(board.row)):
                if (isNone(board, j, i)):
                    board.fillCell(j, i, 'w')
    return

def removeBoat(board: Board):

    no_boats = 0

    if (len(board.boats_remaining) == 0): 
        return no_boats

    if (len(board.boats_remaining[-1]) == 0):
        board.boats_remaining.pop()

    last_boat = board.boats_remaining[-1].pop()

    return last_boat

def countEmptyCells(board: Board):
    count = 0
    for i in range(len(board.row)):
        for j in range(len(board.col)):
            if (isNone(board, i, j)):
                count += 1
    return count

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
    return board.table[row][col] == '~'

"""
----------------------------------------------------------------------------------------------
---------------------------------- Função Main -----------------------------------------------
----------------------------------------------------------------------------------------------
"""

if __name__ == "__main__":
    # TODO:
    # Ler o ficheiro do standard input,
    # Usar uma técnica de procura para resolver a instância,
    # Retirar a solução a partir do nó resultante,
    # Imprimir para o standard output no formato indicado.

    """
    # EXEMPLO TESTE
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

    print('\n')

    second_st.board.print()
    """
    """
    # EXEMPLO 1
    # Ler a instância a partir do ficheiro 'i1.txt' (Figura 1):
    # $ python3 bimaru.py < i1.txt
    board = Board.parse_instance()
    # Imprimir valores adjacentes
    print(board.adjacent_vertical_values(3, 3))
    print(board.adjacent_horizontal_values(3, 3))
    print(board.adjacent_vertical_values(1, 0))
    print(board.adjacent_horizontal_values(1, 0))
    """

    board = Board.parse_instance()

    problem = Bimaru(board)

    orig_state = problem.initial

    #result_state = problem.result(orig_state, [(1,1,'w')])
    
    #print(problem.actions(orig_state))

    #print("Actions to perform:", len(problem.actions(orig_state)))

    print('\nThis board table is supposed to remain unchanged:\n')

    orig_state.board.print()

    print(orig_state.board.table[7][8])

    #print("\nBoard table after the result\n")

    #result_state.board.print()
    #                                                SEARCH ALGOS NOT WORKING YET (WHEN IN USE PROGRAM NEVER ENDS)
    goal_state = breadth_first_tree_search(problem)

    print("\nBFS table result:\n")

    goal_state.state.board.print()

    print("\nIs goal?", problem.goal_test(goal_state.state))

    print(goal_state.state.board.table[8][7])

    print(goal_state.state.board.boats_remaining, len(goal_state.state.board.boats_remaining))
    