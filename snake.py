from collections import deque
from cell import Cell
from gametypes import DirectionType

DEFAULT_DIRECTION = DirectionType.RIGHT

class Snake:
    def __init__(self, head : Cell, tail : Cell):
        self.snake = deque()
        self.head = head
        self.len = 2
        self.direction = DEFAULT_DIRECTION
    
        self.snake.append(tail)
        self.snake.append(head)
    
    def __contains__(self, cell : Cell):
        return cell in self.snake
    
    def move(self) -> Cell:
        self.snake.popleft()
        new_head = None

        if self.direction == DirectionType.RIGHT:
            new_head = Cell(self.head.getX(), self.head.getY() + 1)
        elif self.direction == DirectionType.LEFT:
            new_head = Cell(self.head.getX(), self.head.getY() - 1)
        elif self.direction == DirectionType.TOP:
            new_head = Cell(self.head.getX() - 1, self.head.getY())
        else:   # DirectionType.BOTTOM
            new_head = Cell(self.head.getX() + 1, self.head.getY())
        
        self.snake.append(new_head)
        self.head = new_head

    def detectCrash(self, wallX, wallY, cell) -> bool:
        if cell is None:
            cell = self.head
            
        head = self.snake.pop()
        if cell in self.snake:
            self.snake.append(head)
            return True

        if cell.getX() >= wallX or cell.getX() < 0 or \
           cell.getY() >= wallY or cell.getY() < 0:
            self.snake.append(head)
            return True
        self.snake.append(head)
        return False
    
    def eat(self, food : Cell) -> bool:
        def _grow():
            new_head = Cell(food.getX(), food.getY())
            self.snake.append(new_head)
            self.head = new_head
            self.len += 1

        if food is not None:
            if self.direction == DirectionType.LEFT:
                if food.getX() == self.head.getX() and food.getY() == self.head.getY() - 1:
                    _grow()
                    return True
            elif self.direction == DirectionType.RIGHT:
                if food.getX() == self.head.getX() and food.getY() == self.head.getY() + 1:
                    _grow()
                    return True
            elif self.direction == DirectionType.TOP:
                if food.getX() == self.head.getX() - 1 and food.getY() == self.head.getY():
                    _grow()
                    return True
            elif self.direction == DirectionType.BOTTOM:
                if food.getX() == self.head.getX() + 1 and food.getY() == self.head.getY():
                    _grow()
                    return True
        if food.getX() == self.head.getX() and food.getY() == self.head.getY():
            _grow()
            return True
        return False
    
    def changeDirection(self, direction : DirectionType):
        def _same_or_opposite():
            if direction == self.direction:
                return True
            if self.direction == DirectionType.LEFT:
                return direction == DirectionType.RIGHT
            elif self.direction == DirectionType.RIGHT:
                return direction == DirectionType.LEFT
            elif self.direction == DirectionType.TOP:
                return direction == DirectionType.BOTTOM
            else: # BOTTOM
                return direction == DirectionType.TOP
            return False           

        if not _same_or_opposite():
            self.direction = direction
    
    # Yield direction for the BSF result.
    def yieldDirection(self, cells : [Cell]) -> DirectionType:
        for c in cells:
            cx = c.getX()
            cy = c.getY()
            hx = self.head.getX()
            hy = self.head.getY()
            if cx == hx and cy < hy:
                yield DirectionType.LEFT
            elif cx == hx and cy > hy:
                yield DirectionType.RIGHT
            elif cx < hx and cy == hy:
                yield DirectionType.TOP
            elif cx > hx and cy == hy:
                yield DirectionType.BOTTOM
            else:
                yield None
    
    def getBody(self):
        return self.snake
    
    def getLength(self):
        return self.len
    
    def getHead(self):
        return self.head
