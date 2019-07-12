import pygame
from cell import Cell
from gametypes import CellType
from gametypes import DirectionType
from gametypes import GameMode
from board import Board
from threading import Thread

class View:
    def __init__(self,  board : Board, width = 800, height = 800):
        self.clock = pygame.time.Clock()
        self.running = False
        self.mode = None
        self.width = width
        self.height = height
        self.board = board
    
    def run(self):
        pygame.init()
        self.surface = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("The Snake Game (F1: auto  F2: manual)")
        self.running = True
        self.pause = False

        while self.running:
            self.clock.tick(30)
            self._handle_events()

            if self.mode == GameMode.MANUAL:
                direction = self._get_direction()
            elif self.mode == GameMode.AUTO:
                direction = self.board.getBFSResults()
            else:
                direction = None
            
            if not self.pause:
                self.surface.fill(pygame.Color("#ffffff"))
                self.displayBoard(self.board)
                
                if self.mode is None:
                    self.mode = self._get_mode()
                else:
                    if self.mode == GameMode.AUTO:
                        updatedBoard = self.board.update(True, direction)
                    elif self.mode == GameMode.MANUAL:
                        updatedBoard = self.board.update(False, direction)

                    if not updatedBoard:    # if updateBoard is None, crash is detected
                        self.pause = True
                    else:
                        self.board = updatedBoard
                
                pygame.display.flip()

        pygame.quit()
    
    def displayBoard(self, board : Board):
        scale_x = self.width / board.getWidth()
        scale_y = self.height / board.getHeight()

        color = None
        left = 0
        top = 0

        for row in board.getBoard():
            for cell in row:
                if cell.getType() == CellType.SNAKEPART:
                    color = pygame.Color('#42a4f5')
                elif cell.getType() == CellType.FOOD:
                    color = pygame.Color('#52eff7')
                elif cell.getType() == CellType.EMPTY:
                    color = pygame.Color('#ffffff')
                else:
                    color = pygame.Color('#f542b0')
                left = cell.getY() * scale_y
                top = cell.getX() * scale_x
                
                self._drawRect(left, top, scale_x, scale_y, color)

    def setBoard(self, board = None):
        if board is not None:
            self.board = board
    
    def _drawRect(self, left, top, width, height, color):
        rect = pygame.Rect(left, top, width, height)
        pygame.draw.rect(self.surface, color, rect)
    
    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
    
    def _get_direction(self) -> DirectionType:
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT]:
            return DirectionType.LEFT
        elif key[pygame.K_RIGHT]:
            return DirectionType.RIGHT
        elif key[pygame.K_UP]:
            return DirectionType.TOP
        elif key[pygame.K_DOWN]:
            return DirectionType.BOTTOM
        return None
    
    def _get_mode(self) -> GameMode:
        key = pygame.key.get_pressed()
        if key[pygame.K_F1]:
            return GameMode.AUTO
        elif key[pygame.K_F2]:
            return GameMode.MANUAL
        return None