import os
import random
import pygame


SCREEN_WIDTH, SCREEN_HEIGHT = 600, 600
GAME_WIDTH, GAME_HEIGHT = 300, SCREEN_HEIGHT
GAME_START_X, GAME_END_X = int((SCREEN_WIDTH - GAME_WIDTH)/2), int((SCREEN_WIDTH - GAME_WIDTH)/2 + GAME_WIDTH)
HORIZONTAL_BOXES = 10
VERTICAL_BOXES = 20
BOX_WIDTH, BOX_HEIGHT = int(GAME_WIDTH/HORIZONTAL_BOXES), int(GAME_HEIGHT/VERTICAL_BOXES)
random = random.Random()
pygame.init()
pygame.font.init()
large_font = pygame.font.SysFont("comicsans", 75)
normal_font = pygame.font.SysFont("comicsans", 50)
smaller_font = pygame.font.SysFont("comicsans", 35)

DORIE = pygame.image.load(r'C:\Users\mile5\Desktop\Coding Projects\Python Prjects\Tetris\assets\Dorie.JPG')
DORIE1 = pygame.image.load(r'C:\Users\mile5\Desktop\Coding Projects\Python Prjects\Tetris\assets\Dorie1.PNG')
DORIE2 = pygame.image.load(r'C:\Users\mile5\Desktop\Coding Projects\Python Prjects\Tetris\assets\Dorie2.PNG')
DORIE3 = pygame.image.load(r'C:\Users\mile5\Desktop\Coding Projects\Python Prjects\Tetris\assets\Dorie3.PNG')
DORIE4 = pygame.image.load(r'C:\Users\mile5\Desktop\Coding Projects\Python Prjects\Tetris\assets\Dorie4.jpg')
DORIE5 = pygame.image.load(r'C:\Users\mile5\Desktop\Coding Projects\Python Prjects\Tetris\assets\Dorie5.JPG')
DORIE6 = pygame.image.load(r'C:\Users\mile5\Desktop\Coding Projects\Python Prjects\Tetris\assets\Dorie6.PNG')


pygame.display.set_caption("Tetris")
WIN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


def background(window):
    border_color = (100, 100, 100)
    pygame.draw.rect(window, (0, 0, 0), (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
    # Setting up the game panel
    pygame.draw.rect(window, border_color, (GAME_START_X - 1, 0, 1, GAME_HEIGHT))
    pygame.draw.rect(window, border_color, (GAME_END_X + 1, 0, 1, GAME_HEIGHT))
    pygame.draw.rect(window, (10, 10, 10), (GAME_START_X, 0, GAME_WIDTH, GAME_HEIGHT))
    for line in range(HORIZONTAL_BOXES):
        pygame.draw.rect(window, (0, 0, 0), (int(GAME_START_X + BOX_WIDTH * line), 0, 1, GAME_HEIGHT))
    for line in range(VERTICAL_BOXES):
        pygame.draw.rect(window, (0, 0, 0), (GAME_START_X, int(BOX_HEIGHT * line), GAME_WIDTH, 1))

    score_label = normal_font.render("Score:", True, (255, 255, 255))
    level_label = normal_font.render("Level:", True, (255, 255, 255))
    next_label = smaller_font.render("Next Block:", True, (255, 255, 255))
    drought_label = smaller_font.render("Drought", True, (255, 255, 255))
    difficulty_label = smaller_font.render("Difficulty:", True, (255, 255, 255))
    window.blit(score_label,
             ((GAME_START_X - score_label.get_width()) / 2, SCREEN_HEIGHT / 2 - score_label.get_height()))
    window.blit(level_label,
             ((GAME_START_X - level_label.get_width()) / 2, SCREEN_HEIGHT / 2 + level_label.get_height() + 10))
    window.blit(next_label, ((GAME_END_X + 10), next_label.get_height() + 10))
    window.blit(drought_label,
             (((GAME_START_X - drought_label.get_width()) / 2) + GAME_END_X, SCREEN_HEIGHT / 2 + drought_label.get_height() * 6 + 20))
    window.blit(difficulty_label, ((GAME_START_X - difficulty_label.get_width())/2, 75))
    pygame.draw.rect(window, border_color, (GAME_END_X + 10, BOX_HEIGHT*2 + 5, BOX_WIDTH*4 + 15, BOX_HEIGHT*3))
    pygame.draw.rect(window, (0, 0, 0), (GAME_END_X + 12, BOX_HEIGHT*2 + 7, BOX_WIDTH*4 + 11, BOX_HEIGHT*3-4))


def check_empty(x, y, other_xys):
    if GAME_START_X > x or x >= GAME_END_X or y >= GAME_HEIGHT - 5:
        return False
    if len(other_xys) > 0:
        for block in other_xys:
            if block.x == x and block.y == y:
                return False
    return True


class Block:
    def __init__(self, x, y, color, picture):
        self.x = x
        self.y = y
        self.color = color
        self.picture = picture
        self.right = False
        self.left = False
        self.below = False
        self.stationary = False

    def draw(self, window):
        lighter_color = (150, 150, 150)
        pygame.draw.rect(window, lighter_color, (self.x + 1, self.y + 1, int(BOX_WIDTH) - 2, int(BOX_HEIGHT) - 2))
        pygame.draw.rect(window, self.color, (self.x + 2, self.y + 2, int(BOX_WIDTH) - 4, int(BOX_HEIGHT) - 4))
        #tiny_dorie = pygame.transform.scale(self.picture, (28, 28))
        #WIN.blit(tiny_dorie, (self.x+1, self.y+1))

    def draw_fake(self, window, x_diff, y_diff):
        lighter_color = (150, 150, 150)
        pygame.draw.rect(window, lighter_color, (self.x + 1 + x_diff, self.y + 1 + y_diff, int(BOX_WIDTH) - 2, int(BOX_HEIGHT) - 2))
        pygame.draw.rect(window, self.color, (self.x + 2 + x_diff, self.y + 2 + y_diff, int(BOX_WIDTH) - 4, int(BOX_HEIGHT) - 4))
        #tiny_dorie = pygame.transform.scale(self.picture, (28, 28))
        #WIN.blit(tiny_dorie, (self.x + 2 + x_diff, self.y + 2 + y_diff))


# S block, Z block, L block, J block, O block, I block, T block
class Cluster:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.blocks = []

    def set_xy(self, x, y):
        self.x = x
        self.y = y

    def update_blocks_next_to(self):
        for block1 in self.blocks:
            block1.right = False
            block1.left = False
            block1.below = False
            for block2 in self.blocks:
                if block1.x + BOX_WIDTH == block2.x and block1.y == block2.y:
                    block1.right = True
                if block1.x - BOX_WIDTH == block2.x and block1.y == block2.y:
                    block1.left = True
                if block1.x == block2.x and block1.y + BOX_HEIGHT == block2.y:
                    block1.below = True

    def find_side(self, direction):
        self.update_blocks_next_to()
        blocks_to_check = []
        if direction == 'R':
            for block in self.blocks:
                if not block.right:
                    blocks_to_check.append(block)
        elif direction == 'L':
            for block in self.blocks:
                if not block.left:
                    blocks_to_check.append(block)
        elif direction == 'D':
            for block in self.blocks:
                if not block.below:
                    blocks_to_check.append(block)
        return blocks_to_check

    def move(self, direction, other_blocks):
        # Move Right
        can_move = True
        if direction == 'R':
            spaces = self.find_side('R')
            for space in spaces:
                if not check_empty(space.x + BOX_WIDTH, space.y, other_blocks):
                    can_move = False
            if can_move:
                self.x += BOX_WIDTH
                for block in self.blocks:
                    block.x += BOX_WIDTH

        # Move Left
        if direction == 'L':
            spaces = self.find_side('L')
            for space in spaces:
                if not check_empty(space.x - BOX_WIDTH, space.y, other_blocks):
                    can_move = False
            if can_move:
                self.x -= BOX_WIDTH
                for block in self.blocks:
                    block.x -= BOX_WIDTH

        # Move Down
        if direction == 'D':
            spaces = self.find_side('D')
            for space in spaces:
                if not check_empty(space.x, space.y + BOX_HEIGHT, other_blocks):
                    can_move = False
            if can_move:
                self.y += BOX_HEIGHT
                for block in self.blocks:
                    block.y += BOX_HEIGHT
        return can_move

    def rotate(self, other_blocks):
        clear = []
        all_positions_clear = True

        # Checks if blocks future positions are clear and puts it in a list
        for block in self.blocks:
            if block.x == self.x - BOX_WIDTH and block.y == self.y - BOX_HEIGHT:  # upper left --> lower left
                clear.append(check_empty(block.x, block.y + 2 * BOX_HEIGHT, other_blocks))

            elif block.x == self.x - BOX_WIDTH and block.y == self.y:
                clear.append(check_empty(block.x + BOX_WIDTH, block.y + BOX_HEIGHT, other_blocks))

            elif block.x == self.x - BOX_WIDTH and block.y == self.y + BOX_WIDTH:
                clear.append(check_empty(block.x + 2*BOX_WIDTH, block.y, other_blocks))

            elif block.x == self.x and block.y == self.y + BOX_HEIGHT:
                clear.append(check_empty(block.x + BOX_WIDTH, block.y - BOX_HEIGHT, other_blocks))

            elif block.x == self.x + BOX_WIDTH and block.y == self.y + BOX_HEIGHT:
                clear.append(check_empty(block.x, block.y - 2*BOX_HEIGHT, other_blocks))

            elif block.x == self.x + BOX_WIDTH and block.y == self.y:
                clear.append(check_empty(block.x - BOX_WIDTH, block.y - BOX_HEIGHT, other_blocks))

            elif block.x == self.x + BOX_WIDTH and block.y == self.y - BOX_HEIGHT:
                clear.append(check_empty(block.x - 2*BOX_WIDTH, block.y, other_blocks))

            elif block.x == self.x and block.y == self.y - BOX_HEIGHT:
                clear.append(check_empty(block.x - BOX_WIDTH, block.y + BOX_HEIGHT, other_blocks))

            # IBlocks only
            elif block.x == self.x + BOX_WIDTH*2 and block.y == self.y:
                clear.append(check_empty(self.x, block.y + BOX_HEIGHT*2, other_blocks))

            elif block.x == self.x and block.y == self.y - BOX_HEIGHT*2:
                clear.append(check_empty(self.x + BOX_WIDTH*2, self.y, other_blocks))

            elif block.x == self.x - BOX_WIDTH * 2 and block.y == self.y:
                clear.append(check_empty(self.x, block.y - BOX_HEIGHT * 2, other_blocks))

            elif block.x == self.x and block.y == self.y + BOX_HEIGHT * 2:
                clear.append(check_empty(self.x - BOX_WIDTH * 2, self.y, other_blocks))

        for pos in clear:
            if not pos:
                all_positions_clear = False

        # if path is clear, rotates blocks
        if all_positions_clear:
            for block in self.blocks:
                if block.x == self.x - BOX_WIDTH and block.y == self.y - BOX_HEIGHT:
                    block.y += BOX_HEIGHT * 2
                elif block.x == self.x - BOX_WIDTH and block.y == self.y:
                    block.x += BOX_WIDTH
                    block.y += BOX_HEIGHT
                elif block.x == self.x - BOX_WIDTH and block.y == self.y + BOX_WIDTH:
                    block.x += BOX_WIDTH * 2
                elif block.x == self.x and block.y == self.y + BOX_HEIGHT:
                    block.x += BOX_WIDTH
                    block.y -= BOX_HEIGHT
                elif block.x == self.x + BOX_WIDTH and block.y == self.y + BOX_HEIGHT:
                    block.y -= BOX_HEIGHT * 2
                elif block.x == self.x + BOX_WIDTH and block.y == self.y:
                    block.x -= BOX_WIDTH
                    block.y -= BOX_HEIGHT
                elif block.x == self.x + BOX_WIDTH and block.y == self.y - BOX_HEIGHT:
                    block.x -= BOX_WIDTH*2
                elif block.x == self.x and block.y == self.y - BOX_HEIGHT:
                    block.x -= BOX_WIDTH
                    block.y += BOX_HEIGHT

                # IBlocks only
                elif block.x == self.x - BOX_WIDTH * 2 and block.y == self.y:
                    block.x += BOX_WIDTH*2
                    block.y -= BOX_HEIGHT*2
                elif block.x == self.x and block.y == self.y - BOX_HEIGHT * 2:
                    block.x += BOX_WIDTH * 2
                    block.y += BOX_HEIGHT * 2
                elif block.x == self.x + BOX_WIDTH * 2 and block.y == self.y:
                    block.x -= BOX_WIDTH*2
                    block.y += BOX_HEIGHT*2
                elif block.x == self.x and block.y == self.y + BOX_HEIGHT * 2:
                    block.x -= BOX_WIDTH * 2
                    block.y -= BOX_HEIGHT * 2
        self.update_blocks_next_to()

    def draw(self, window):
        for block in self.blocks:
            block.draw(window)

    def draw_fake(self, window):
        current_pos = GAME_START_X + BOX_WIDTH*4
        for block in self.blocks:
            block.draw_fake(window, GAME_END_X + 50 - current_pos, BOX_HEIGHT*3.5)


class SBlock(Cluster):
    def __init__(self, x, y, color):
        super().__init__(x, y, color)
        self.blocks = [Block(x - BOX_WIDTH, y, color, DORIE),
                       Block(x, y, color, DORIE),
                       Block(x, y - BOX_HEIGHT, color, DORIE),
                       Block(x + BOX_WIDTH, y - BOX_HEIGHT, color, DORIE)]


class ZBlock(Cluster):
    def __init__(self, x, y, color):
        super().__init__(x, y, color)
        self.blocks = [Block(x - BOX_WIDTH, y - BOX_HEIGHT, color, DORIE1),
                       Block(x, y - BOX_HEIGHT, color, DORIE1),
                       Block(x, y, color, DORIE1),
                       Block(x + BOX_WIDTH, y, color, DORIE1)]


class LBlock(Cluster):
    def __init__(self, x, y, color):
        super().__init__(x, y, color)
        self.blocks = [Block(x - BOX_WIDTH, y - BOX_HEIGHT, color, DORIE2),
                       Block(x - BOX_WIDTH, y, color, DORIE2),
                       Block(x, y, color, DORIE2),
                       Block(x + BOX_WIDTH, y, color, DORIE2)]


class JBlock(Cluster):
    def __init__(self, x, y, color):
        super().__init__(x, y, color)
        self.blocks = [Block(x - BOX_WIDTH, y, color, DORIE3),
                       Block(x, y, color, DORIE3),
                       Block(x + BOX_WIDTH, y, color, DORIE3),
                       Block(x + BOX_WIDTH, y - BOX_HEIGHT, color, DORIE3)]


class OBlock(Cluster):
    def __init__(self, x, y, color):
        super().__init__(x, y, color)
        self.blocks = [Block(x, y, color, DORIE4),
                       Block(x - BOX_WIDTH, y, color, DORIE4),
                       Block(x, y - BOX_HEIGHT, color, DORIE4),
                       Block(x - BOX_WIDTH, y - BOX_HEIGHT, color, DORIE4)]
        self.update_blocks_next_to()

    def rotate(self, other_blocks):
        return other_blocks


class IBlock(Cluster):
    def __init__(self, x, y, color):
        super().__init__(x, y, color)
        self.blocks = [Block(x - BOX_WIDTH*2, y, color, DORIE5),
                       Block(x - BOX_WIDTH, y, color, DORIE5),
                       Block(x, y, color, DORIE5),
                       Block(x + BOX_WIDTH, y, color, DORIE5)]


class TBlock(Cluster):
    def __init__(self, x, y, color):
        super().__init__(x, y, color)
        self.blocks = [Block(x, y - BOX_HEIGHT, color, DORIE6),
                       Block(x - BOX_WIDTH, y, color, DORIE6),
                       Block(x, y, color, DORIE6),
                       Block(x + BOX_WIDTH, y, color, DORIE6)]
        self.update_blocks_next_to()


def random_block(prev_block):
    start_x = GAME_START_X + BOX_WIDTH * 4
    start_y = 0
    block = random.choice((OBlock(start_x + BOX_WIDTH, start_y, (150, 150, 0)),
                           SBlock(start_x, start_y, (25, 150, 25)),
                           ZBlock(start_x, start_y, (150, 0, 0)),
                           LBlock(start_x, start_y, (150, 125, 0)),
                           JBlock(start_x, start_y, (0, 0, 150)),
                           IBlock(start_x + BOX_WIDTH, start_y, (0, 150, 150)),
                           TBlock(start_x, start_y, (75, 0, 150))
                           ))
    if prev_block.color == block.color:
        block = random_block(prev_block)
    return block


def clear_row_animation(window, y, time):
    if time > 50:
        pygame.draw.rect(window, (255, 255, 255), (GAME_START_X, y, GAME_WIDTH, BOX_HEIGHT))
    elif time > 30:
        pygame.draw.rect(window,
                         (255, 255, 255),
                         (int(GAME_START_X + GAME_WIDTH/2 * ((30-(time-30))/30)),
                          y,
                          GAME_WIDTH * ((time-30)/30),
                          BOX_HEIGHT))


def start_menu():
    potential_choice = 0
    choice = int
    prev_click = 'none'
    first_click = True

    def redraw(window):
        background(window)
        easy_label = large_font.render("Easy", True, (255, 255, 255))
        medium_label = large_font.render("Medium", True, (255, 255, 255))
        hard_label = large_font.render("Hard", True, (255, 255, 255))

        easy_xy = ((SCREEN_WIDTH - easy_label.get_width())/2, SCREEN_HEIGHT/4)
        medium_xy = ((SCREEN_WIDTH - medium_label.get_width())/2, SCREEN_HEIGHT/2)
        hard_xy = ((SCREEN_WIDTH - hard_label.get_width())/2, 3*SCREEN_HEIGHT/4)

        if potential_choice == 1:
            pygame.draw.rect(window, (255, 255, 255), (easy_xy[0] - 10, easy_xy[1] - 10, easy_label.get_width() + 20, easy_label.get_height() + 20))
            pygame.draw.rect(window, (0, 150, 0), (easy_xy[0] - 5, easy_xy[1] - 5, easy_label.get_width() + 10, easy_label.get_height() + 10))
        if potential_choice == 2:
            pygame.draw.rect(window, (255, 255, 255), (medium_xy[0] - 10, medium_xy[1] - 10, medium_label.get_width() + 20, medium_label.get_height() + 20))
            pygame.draw.rect(window, (150, 150, 0), (medium_xy[0] - 5, medium_xy[1] - 5, medium_label.get_width() + 10, medium_label.get_height() + 10))

        if potential_choice == 3:
            pygame.draw.rect(window, (255, 255, 255), (hard_xy[0] - 10, hard_xy[1] - 10, hard_label.get_width() + 20, hard_label.get_height() + 20))
            pygame.draw.rect(window, (150, 0, 0), (hard_xy[0] - 5, hard_xy[1] - 5, hard_label.get_width() + 10, hard_label.get_height() + 10))

        window.blit(easy_label, (easy_xy[0], easy_xy[1]))
        window.blit(medium_label, (medium_xy[0], medium_xy[1]))
        window.blit(hard_label, (hard_xy[0], hard_xy[1]))

        pygame.display.update()

    while choice == int:
        keys = pygame.key.get_pressed()
        click = 'none'

        if keys[pygame.K_w] or keys[pygame.K_UP]:
            if first_click:
                potential_choice = 1
                first_click = False
            click = 'w'
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            if first_click:
                potential_choice = 3
                first_click = False
            click = 's'
        if keys[pygame.K_RETURN]:
            choice = potential_choice
        if keys[pygame.K_ESCAPE]:
            choice = 0

        if click != prev_click:
            if click == 'w':
                if potential_choice > 1:
                    potential_choice -= 1
            if click == 's':
                if potential_choice < 3:
                    potential_choice += 1

        prev_click = click
        redraw(WIN)

        # Checks if window is closed
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                choice = 0
    return choice


def main(difficulty):
    running = True
    fps = 60
    timer1, timer2, timer3 = 0, 0, -1
    times_still = 0
    stationary_blocks = []
    paused = False
    click = "None"
    clears = []
    need_new_block = False
    original_speed = 60
    speed = original_speed
    score = 0
    level = 1
    game_over = False
    multiplier = 2
    drought = 0

    clock = pygame.time.Clock()

    block = random_block(LBlock(GAME_START_X + BOX_WIDTH * 4, BOX_HEIGHT * 2, (153, 1, 152)))
    next_block = random_block(LBlock(GAME_START_X + BOX_WIDTH * 4, BOX_HEIGHT * 2, (153, 1, 152)))

    if difficulty == 0:
        running = False

    def redraw(window, animations, timer):
        background(window)
        block.draw(window)
        next_block.draw_fake(window)

        for blocks in stationary_blocks:
            blocks.draw(window)

        # draws animations
        for pos in animations:
            clear_row_animation(window, pos, timer)

        difficulty_level = normal_font.render("", True, (255, 255, 255))
        score_num = normal_font.render(str(score), True, (255, 255, 255))
        level_num = normal_font.render(str(level), True, (255, 255, 255))
        drought_num = smaller_font.render(str(drought), True, (255, 255, 255))
        if difficulty == 1:
            difficulty_level = smaller_font.render("Easy", True, (0, 150, 0))
        elif difficulty == 2:
            difficulty_level = smaller_font.render("Medium", True, (150, 150, 0))
        elif difficulty == 3:
            difficulty_level = smaller_font.render("Hard", True, (150, 0, 0))
        window.blit(score_num,
                 ((GAME_START_X - score_num.get_width()) / 2, SCREEN_WIDTH / 2 + 10))
        window.blit(level_num,
                 ((GAME_START_X - level_num.get_width()) / 2, SCREEN_WIDTH / 2 + level_num.get_height()*2 + 20))

        window.blit(drought_num,
                 (((GAME_START_X - drought_num.get_width()) / 2) + GAME_END_X,
                  SCREEN_HEIGHT / 2 + drought_num.get_height() * 8 + 20))
        window.blit(difficulty_level, ((GAME_START_X - difficulty_level.get_width()) / 2, 110))

        if paused:
            if game_over:
                paused_label = normal_font.render("Game Over", True, (255, 255, 255))
            else:
                paused_label = normal_font.render("Paused", True, (255, 255, 255))
            WIN.blit(paused_label,
                     ((SCREEN_WIDTH - paused_label.get_width())/2, SCREEN_WIDTH/2 - paused_label.get_height()))
        pygame.display.update()

    while running:
        clock.tick(fps)

        block_last_y = block.y
        last_click = click
        click = 'None'

        # Key Inputs
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE] and not game_over:
            click = 'pause'
        elif keys[pygame.K_r] and paused:
            click = 'reset'
        elif keys[pygame.K_h] and paused:
            click = 'home'
        if last_click != click:
            if click == 'pause':
                paused = not paused
            elif click == 'reset':
                stationary_blocks.clear()
                level = 1
                score = 0
                drought = 0
                speed = original_speed
                need_new_block = True
                paused = False
                game_over = False
            elif click == 'home':
                difficulty = start_menu()
                stationary_blocks.clear()
                level = 1
                score = 0
                drought = 0
                speed = original_speed
                need_new_block = True
                paused = False
                game_over = False

        if not paused:
            if len(clears) == 0:
                if (keys[pygame.K_a] or keys[pygame.K_LEFT]) and timer2 <= 0:  # Left
                    block.move('L', stationary_blocks)
                    timer2 = 5

                elif (keys[pygame.K_d] or keys[pygame.K_RIGHT]) and timer2 <= 0:  # Right
                    block.move('R', stationary_blocks)
                    timer2 = 5

                elif (keys[pygame.K_w] or keys[pygame.K_UP]) and timer2 <= 0:  # Rotates
                    block.rotate(stationary_blocks)
                    timer2 = 10

                elif keys[pygame.K_s] or keys[pygame.K_DOWN]:  # Down
                    block.move('D', stationary_blocks)
                    score += 1

                elif keys[pygame.K_SPACE]:   # Fall
                    click = 'space'

            if last_click != click:
                if click == 'space':
                    can_move = True
                    while can_move:
                        can_move = block.move('D', stationary_blocks)
                        score += 2
                    for piece in block.blocks:
                        stationary_blocks.append(piece)
                    times_still = 0
                    need_new_block = True

            timer2 -= 1

            # Move auto move
            if timer1 <= 0 and len(clears) == 0:
                block.move('D', stationary_blocks)
                timer1 = speed
            timer1 -= 1

            # New block condition
            if len(clears) != 0:
                times_still = 0
            elif block.y == block_last_y:
                times_still += 1
            else:
                times_still = 0
            if times_still >= speed*multiplier:
                for piece in block.blocks:
                    stationary_blocks.append(piece)
                need_new_block = True
                times_still = 0

            # Checks if need to clear row
            row_list = []
            for apple in stationary_blocks:
                row_list.append(apple.y)
            for element in row_list:
                if row_list.count(element) >= 10:
                    block = OBlock(1000, 0, (255, 255, 255))
                    for apple in stationary_blocks:
                        if apple.y == element:
                            stationary_blocks.remove(apple)
                    if clears.count(element) == 0:
                        clears.append(element)
                    timer3 = 60

            # Makes new block
            if need_new_block and len(clears) == 0:
                for piece in stationary_blocks:
                    if 0 == piece.y:
                        paused = True
                        game_over = True
                prev_block = block
                block = next_block
                next_block = random_block(prev_block)
                if block.__class__ != IBlock:
                    drought += 1
                else:
                    drought = 0

                if level >= 15:
                    if score > level*10000:
                        level += 1
                elif level >= 5:
                    if score > level*5000:
                        level += 1
                elif score >= 10000:
                    level += 1
                elif score >= 5000:
                    level += 1
                elif score >= 2000:
                    level += 1
                elif score >= 1000:
                    level += 1
                if level < 60/difficulty:
                    speed = original_speed - difficulty*level
                else:
                    speed = 2
                need_new_block = False

            redraw(WIN, clears, timer3)
            # Moves all blocks down when row clears
            if 15 >= timer3 > 0:
                for apple in stationary_blocks:
                    i = 0
                    clears.sort(reverse=True)
                    for element in clears:
                        if apple.y < element + BOX_HEIGHT*i:
                            apple.y += (BOX_HEIGHT/15)
                        i += 1

            if timer3 >= 0:
                timer3 -= 1
            else:
                if len(clears) == 1:
                    score += 100*level
                elif len(clears) == 2:
                    score += 300*level
                elif len(clears) == 3:
                    score += 500*level
                elif len(clears) == 4:
                    score += 800*level
                clears.clear()

        else:
            redraw(WIN, clears, timer3)

        # Checks if window is closed
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False


main(start_menu())
