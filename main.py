import pygame, random, sys
from pygame.math import Vector2


cells_size = 40
cells_number = 20


class Snake:
    def __init__(self) -> None:
        self.body = [Vector2(5, 10), Vector2(4,10), Vector2(3, 10)]
        self.direction = Vector2(1, 0 )
        self.more_blocks = False

        self.head_up = pygame.image.load('Graphics/head_up.png').convert_alpha()
        self.head_down = pygame.image.load('Graphics/head_down.png').convert_alpha()
        self.head_right = pygame.image.load('Graphics/head_right.png').convert_alpha()
        self.head_left = pygame.image.load('Graphics/head_left.png').convert_alpha()
		
        self.tail_up = pygame.image.load('Graphics/tail_up.png').convert_alpha()
        self.tail_down = pygame.image.load('Graphics/tail_down.png').convert_alpha()
        self.tail_right = pygame.image.load('Graphics/tail_right.png').convert_alpha()
        self.tail_left = pygame.image.load('Graphics/tail_left.png').convert_alpha()

        self.body_vertical = pygame.image.load('Graphics/body_vertical.png').convert_alpha()
        self.body_horizontal = pygame.image.load('Graphics/body_horizontal.png').convert_alpha()
        
        self.body_tr = pygame.image.load('Graphics/body_tr.png').convert_alpha()
        self.body_tl = pygame.image.load('Graphics/body_tl.png').convert_alpha()
        self.body_br = pygame.image.load('Graphics/body_br.png').convert_alpha()
        self.body_bl = pygame.image.load('Graphics/body_bl.png').convert_alpha()
        
        self.crunch_sound = pygame.mixer.Sound('Sound/crunch.wav')
   
    def draw_snake(self):
        self.upgrade_head_graphics()
        self.upgrade_tail_graphics()

        for index,block in enumerate(self.body):
            #we still need a rectangle for the position
            #what direction is the face heading
            x_pos = int(block.x * cells_size)
            y_pos = int(block.y * cells_size)
            block_rect = pygame.Rect(x_pos,y_pos,cells_size,cells_size)
            
            if index == 0:
                screen.blit(self.head, block_rect)
            elif index == len(self.body) -1:
                screen.blit(self.tail, block_rect)
            else:
                prev_block = self.body[index + 1] - block
                next_block = self.body[index - 1] - block
                if prev_block.x == next_block.x:
                    screen.blit(self.body_vertical, block_rect)
                elif prev_block.y == next_block.y:
                    screen.blit(self.body_horizontal, block_rect)
                else:
                    if prev_block.x == -1 and next_block.y == -1 or prev_block.y == -1 and next_block.x == -1:
                        screen.blit(self.body_tl, block_rect)
                    elif prev_block.x == -1 and next_block.y == 1 or prev_block.y == 1 and next_block.x == -1:
                        screen.blit(self.body_bl, block_rect)
                    elif prev_block.x == 1 and next_block.y == -1 or prev_block.y == -1 and next_block.x == 1:
                        screen.blit(self.body_tr, block_rect)
                    elif prev_block.x == 1 and next_block.y == 1 or prev_block.y == 1 and next_block.x == 1:
                        screen.blit(self.body_br, block_rect)

    def upgrade_head_graphics(self):
        head_relation = self.body[1] - self.body[0]
        if head_relation == Vector2(1,0): self.head = self.head_left
        elif head_relation == Vector2(-1,0): self.head = self.head_right
        elif head_relation == Vector2(0,1): self.head = self.head_up
        elif head_relation == Vector2(0,-1): self.head = self.head_down

    def upgrade_tail_graphics(self):
        tail_r = self.body[-2] - self.body[-1]
        if tail_r == Vector2(1,0): self.tail = self.tail_left
        elif tail_r == Vector2(-1,0): self.tail = self.tail_right
        elif tail_r == Vector2(0,1): self.tail = self.tail_up
        elif tail_r == Vector2(0,-1): self.tail = self.tail_down
     
    def move_snake(self):
        if self.more_blocks == True:
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.more_blocks = False
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
    
    def add_block(self):
        self.more_blocks = True

    def reset(self):
        self.body = [Vector2(5, 10), Vector2(4,10), Vector2(3, 10)]

class Fruit:
    def __init__(self) -> None:
        self.x = random.randint(0, cells_number-1)
        self.y = random.randint(0, cells_number-1)
        self.pos = Vector2(self.x, self.y)
        #create a x and y position
        #draw a square

    def draw_fruit(self):
        fruit_rect = pygame.Rect(int(self.pos.x * cells_size), int(self.pos.y * cells_size), cells_size, cells_size)
        screen.blit(apple, fruit_rect)
        #pygame.draw.rect(screen, (255, 0, 0), fruit_rect)

    def randomize(self):
        self.x = random.randint(0, cells_number-1)
        self.y = random.randint(0, cells_number-1)
        self.pos = Vector2(self.x, self.y)

class Main:
    def __init__(self) -> None:
        self.snake = Snake()
        self.fruit = Fruit()
        self.moves = 0

    def update(self):
        self.snake.move_snake()
        self.check_collision()
        self.check_fail()

    def draw_elements(self):
        self.draw_grass()
        self.snake.draw_snake()
        self.fruit.draw_fruit()
        self.draw_score()
        self.draw_moves()

    def draw_grass(self):
        grass_color = (167, 209, 61)

        for row in range(cells_number):
            if row % 2 == 0:
                for col in range(cells_number):
                    if col % 2 == 0:
                        grass_rect = pygame.Rect(col * cells_size, row * cells_size, cells_size, cells_size)
                        pygame.draw.rect(screen, grass_color, grass_rect)
            else:
                for col in range(cells_number):
                    if col % 2 != 0:
                        grass_rect = pygame.Rect(col * cells_size, row * cells_size, cells_size, cells_size)
                        pygame.draw.rect(screen, grass_color, grass_rect)


    def draw_score(self):
        score_text = "Score " + str(len(self.snake.body) - 3)
        #True deixa o texto menos quadrático, mas para computadores fracos ou jogos complexos isso pode atrasar o tempo de resposta
        score_surface = game_font.render(score_text, True,(0, 0, 0))
        score_x = int(cells_size)
        score_y = int(cells_size)
        score_rect = score_surface.get_rect(center = (score_x, score_y))
        screen.blit(score_surface, score_rect)

    def draw_moves(self):
        moves_text = "Moves " + str(self.moves)
        #True deixa o texto menos quadrático, mas para computadores fracos ou jogos complexos isso pode atrasar o tempo de resposta
        moves_surface = game_font.render(moves_text, True,(0, 0, 0))
        moves_x = int(cells_size)
        moves_y = int(cells_size*cells_number - 60)
        moves_rect = moves_surface.get_rect(center = (moves_x, moves_y))
        screen.blit(moves_surface, moves_rect)

    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomize()
            self.snake.add_block()

        for block in self.snake.body[1:]:
            if block == self.fruit.pos:
                self.fruit.randomize()

    def check_fail(self):
        if not 0 <= self.snake.body[0].x < cells_number or not 0 <= self.snake.body[0].y < cells_number:
            self.game_over()
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()
        #check if the snake hits itself

    def game_over(self):
        self.moves = 0
        self.snake.reset()

pygame.init()
screen = pygame.display.set_mode((cells_size * cells_number, cells_size * cells_number))
pygame.display.set_caption("Snake")
clock = pygame.time.Clock()

apple = pygame.image.load("Graphics/apple.png").convert_alpha()

game_font = pygame.font.Font(None, 25)

fruit = Fruit()
snake = Snake()

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)

main_game = Main()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == SCREEN_UPDATE:
            main_game.update()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if main_game.snake.direction.y != 1:
                    main_game.moves += 1
                    main_game.snake.direction = Vector2(0, -1)
            if event.key == pygame.K_DOWN:
                if main_game.snake.direction.y != -1:
                    main_game.moves += 1
                    main_game.snake.direction = Vector2(0, 1)
            if event.key == pygame.K_LEFT:
                if main_game.snake.direction.x != 1:
                    main_game.moves += 1
                    main_game.snake.direction = Vector2(-1, 0)
            if event.key == pygame.K_RIGHT:
                if main_game.snake.direction.x != -1:
                    main_game.moves += 1
                    main_game.snake.direction = Vector2(1, 0)
    screen.fill((175, 215, 70))
    #draw all ours elements
    main_game.draw_elements()
    pygame.display.update()
    clock.tick(60)