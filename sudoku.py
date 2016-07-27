#!/usr/bin/env python3

#Lucia Pal, 2016
from copy import deepcopy

class Stack:
    s = []
    top = 0
    def __init__(self):
        self.top = 0
        self.s = []

    def push(self, e):
        self.s.append(e)
        self.top += 1

    def pop(self):
        self.top -= 1
        return self.s.pop()

    def empty(self):
        return (self.top <= 0)

class Queue:
    q = []
    first = 0
    last = 0
    def __init__(self):
        self.first = 0
        self.last = 0
        self.q = []

    def push(self, e):
        self.q.append(e)
        self.last += 1

    def pop(self):
        res = self.q[self.first]
        self.first += 1
        return res

    def empty(self):
        if (self.first >= self.last):
            return True
        return False


class Sudoku:
    input_sudoku = []
    solution = []
    solutionString = ''

    def __init__(self):
        self.input_sudoku = [9*[-1] for i in range(9)]
        self.solution = [9*[-1] for i in range(9)]

    '''
    Reads input from standard input.
    '''
    def readInputSudoku(self, sudoku):
        lines = sudoku.split('\n')
        for i, line in enumerate (lines):
            if (i % 2 == 1):
                a = line.split('|')
                for j, x in enumerate(a):
                    if (x == ''):
                        a.remove(x)
                for j, x in enumerate(a):
                    y = x.replace(" ", "")
                    if (len(y) > 0):
                        self.input_sudoku[(i-1)//2][j] = int(y)
        #print('input', self.input_sudoku)

    def getPossibleNubersForOneSquare(self, sud, possibleNumbers): #[0, 0] is the first nubmer = left top corner
        for x in range(9):
            for y in range(9):
                if (sud[x][y] != -1):
                    possibleNumbers[x][y] = [sud[x][y]] # we've already solved what should be at [x][y]
                else:
                    for i in range(9):
                        if (sud[i][y] in possibleNumbers[x][y]):
                            possibleNumbers[x][y].remove(sud[i][y])

                        if (sud[x][i] in possibleNumbers[x][y]):
                            possibleNumbers[x][y].remove(sud[x][i])
                    square_x = x // 3
                    square_y = y // 3
                    for i in range(3):
                        for j in range(3):
                            if (sud[3*square_x + i][3*square_y + j] in possibleNumbers[x][y]):
                                possibleNumbers[x][y].remove(sud[3*square_x + i][3*square_y + j])
        return possibleNumbers

    def fillTheOnlyNumber(self, a, b, num, possibleNumbers):
        ps = deepcopy(possibleNumbers)
        q = Queue()
        q.push((a, b))
        ps[a][b] = [num]
        while not q.empty():
            x, y = q.pop()
            if (len(ps[x][y]) != 1):
                print('Something is terribly wrong!')
                break
            else:
                number = ps[x][y][0]
                for i in range(9):
                    if (number in ps[i][y]) and (i != x):
                        ps[i][y].remove(number)
                        if (len(ps[i][y]) <= 1):
                            q.push((i, y))
                    if (number in ps[x][i]) and (i != y):
                        ps[x][i].remove(number)
                        if (len(ps[x][i]) <= 1):
                            q.push((x, i))

                square_x = x // 3
                square_y = y // 3
                for i in range(3):
                    for j in range(3):
                        if (((3*square_x + i) != x) and ((3*square_y + j) != y)):
                            if (number in ps[3*square_x + i][3*square_y + j]):
                                ps[3*square_x + i][3*square_y + j].remove(number)
                                if (len(ps[3*square_x + i][3*square_y + j]) <= 1):
                                    q.push(((3*square_x + i), (3*square_y + j)))

        return ps

    def checkFeasibilityOfSolution(self, possibleNumbers):
        for i in range(9):
            for j in range(9):
                if (len(possibleNumbers[i][j]) < 1):
                    return False
        return True

    def isSolutionUnclear(self, possibleNumbers):
        for i in range(9):
            for j in range(9):
                if (len(possibleNumbers[i][j]) < 1):
                    return False #there is no solution
        for i in range(9):
            for j in range(9):
                if (len(possibleNumbers[i][j]) > 1):
                    return True
        return False # there is exactly one solution

    def solveSudoku(self):
        isSolution = False
        possibleNumbers  = [[[1, 2, 3, 4, 5, 6, 7, 8, 9] for i in range(9)] for j in range(9)]
        solution = [[[] for i in range(9)] for j in range(9)]
        possibleNumbers = deepcopy(self.getPossibleNubersForOneSquare(self.input_sudoku, possibleNumbers))
        for i in range(9):
            for j in range(9):
                if (len(possibleNumbers[i][j]) == 1):
                    possibleNumbers = deepcopy(self.fillTheOnlyNumber(i, j, possibleNumbers[i][j][0], possibleNumbers))

        s = Stack()
        s.push(possibleNumbers)
        while not s.empty():
            possibleNumbers = deepcopy(s.pop())
            if not self.isSolutionUnclear(possibleNumbers):
                if self.checkFeasibilityOfSolution(possibleNumbers):
                    solution = deepcopy(possibleNumbers) # we have solution!!!!!
                    isSolution = True
                    break
                else:
                    continue
            else:
                m = 10
                x = -1
                y = -1
                a = []
                for i in range(9):
                    for j in range(9):
                        if (len(possibleNumbers[i][j]) < m) and (len(possibleNumbers[i][j]) > 1):
                            m = len(possibleNumbers[i][j])
                            a = deepcopy(possibleNumbers[i][j])
                            x = i
                            y = j
                for i in range(len(a)):
                    s.push(self.fillTheOnlyNumber(x, y, a[i], possibleNumbers))
        if isSolution:
            for i in range(9):
                for j in range(9):
                    self.solution[i][j] = solution[i][j][0]
        else:
            self.solution = []

        self.solutionToString()
        #print(self.solutionString)
        return(self.solution)

    def solutionToString(self):
        self.solutionString = ''
        if (self.solution[0][0] == -1):
            self.solutionString = 'NO'
        for i in range(9):
            for j in range(9):
                self.solutionString += str(self.solution[i][j])
            self.solutionString += '\n'
        return(self.solutionString)
    '''
    Writes solution to standard output.
    '''
    def writeSolution(self):
        for i in range(19):
            if (i % 2 == 0):
                if (i == 6) or (i == 12):
                    print(' ===================================== ')
                else:
                    print(' ------------------------------------- ')
            else:
                for j in range(3):
                    print('| ' + str(self.solution[i][j]) + ' | ' + str(self.solution[i][j+1]) + ' | ' + str(self.solution[i][j+2]) + ' |', end = '')
                print()
