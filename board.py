from cell import Cell
from gametypes import CellType
from gametypes import DirectionType
from snake import Snake
from random import randrange
from random import choice
from collections import deque

class Board:
    def __init__(self, width = 25, height = 25):
        self.width = width
        self.height = height
        self.board = []
        self.food = None
        self.bsf_result = None
    
    def initBoard(self):
        head_x = randrange(1, self.width - 1)
        head_y = randrange(1, self.height - 1)

        self.snake = Snake(Cell(head_x, head_y), Cell(head_x, head_y - 1))

        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(Cell(i, j, CellType.EMPTY))
            self.board.append(row)

        self.food = self.generateFood()
        self.bsf_result = self.snake.yieldDirection(self.BSF())
        self.refresh()
    
    def refresh(self):
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i][j].getType() != CellType.EMPTY:
                    self.board[i][j] = Cell(i, j, CellType.EMPTY)

        for part in self.snake.getBody():
            self.board[part.getX()][part.getY()] = part
        
        if self.food is not None:
            self.board[self.food.getX()][self.food.getY()] = self.food
                
    def generateFood(self) -> Cell:
        def _rep_board_as_list() -> list:
            _list = list()
            for i in range(self.width):
                for j in range(self.height):
                    _list.append(self.board[i][j])
            return _list
        
        new_food = choice([cell for cell in _rep_board_as_list() if cell not in self.snake])
        new_food.setType(CellType.FOOD)
        return new_food
    
    def update(self, auto, direction = None):
        if direction:
            self.snake.changeDirection(direction)
        self.snake.move()

        if self.snake.detectCrash(self.width, self.height, None):
            return None

        if self.snake.eat(self.food):
            self.food = self.generateFood()
        
        if auto:
            self.bsf_result = self.snake.yieldDirection(self.BSF())

        self.refresh()
        return self
    
    def BSF(self) -> [Cell]:
        def _check_availability(c):
            if not self.snake.detectCrash(self.width, self.height, c):
                if not self.board[c.getX()][c.getY()].isVisited() and not self.board[c.getX()][c.getY()] in q:
                    q.append(self.board[c.getX()][c.getY()])
                    pcmap[self.board[c.getX()][c.getY()]] = cur
        pcmap = dict()  # parent-child mapping
        res = list()

        for row in self.board:
            for cell in row:
                cell.setVisit(False)
        q = deque()
        q.append(self.snake.getHead())

        while q:
            cur = q.popleft()

            if cur == self.food:
                c = pcmap[cur]
                res.append(cur)
                while c != self.snake.getHead():
                    res.append(c)
                    c = pcmap[c]

                res.reverse()
                return res

            cur.setVisit(True)
            x = cur.getX()
            y = cur.getY()

            _check_availability(Cell(x - 1, y))
            _check_availability(Cell(x + 1, y))
            _check_availability(Cell(x, y - 1))
            _check_availability(Cell(x, y + 1))

        return res

    def getBFSResults(self) -> DirectionType:
        if not self.bsf_result:
            return None
            
        for direction in self.bsf_result:
            return direction
    
    def getBoard(self):
        return self.board
    
    def getWidth(self):
        return self.width
    
    def getHeight(self):
        return self.height