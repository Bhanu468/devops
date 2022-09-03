
import pygame
import  pygame_menu
import random
import sys
pygame.init()
#Size - name of the window
SCREEN = pygame.display.set_mode((600, 400))
pygame.display.set_caption("Example")

# pygame.init()
# SCREEN = pygame.display.set_mode((600, 600))
BG = pygame.image.load("assets/Background.png")
#pygame module is imported
#random module is imported

menu = pygame_menu.Menu('Menu', 600, 400,theme=pygame_menu.themes.THEME_BLUE)
#global vars
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600

GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH / GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT / GRID_SIZE

FPS = 10
# SNAKE STARTS AT CENTER
CENTER = ((SCREEN_WIDTH / 2), (SCREEN_HEIGHT / 2))
#Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

STOP = (0, 0)


class Snake:
    def __init__(self):
        self.length = 1
        self.score = 0
        self.positions = [CENTER]
        # start the snake at random position
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        # make the snake color as darkgreen
        self.color = pygame.Color("darkgreen")
        self.outline_color = pygame.Color("slategrey")

    # to know the head position of snake
    def get_head_position(self):
        return self.positions[0]

    # change the position of snake
    def turn(self, new_dir):
        if self.length > 1 and (new_dir[0] * -1, new_dir[1] * -1) == self.direction:
            return
        else:
            self.direction = new_dir

    def move(self):
        cur = self.get_head_position()
        x, y = self.direction
        new_pos = ((cur[0] + (x * GRID_SIZE)), cur[1] + (y * GRID_SIZE))
        # if we reaches to border
        if new_pos[0] < 0 or new_pos[0] >= SCREEN_WIDTH or new_pos[1] < 0 or new_pos[1] >= SCREEN_HEIGHT:
            self.die()
        # if snake intersect hit itself it will die
        elif len(self.positions) > 2 and new_pos in self.positions[2:]:
            self.die()
        else:
            self.positions.insert(0, new_pos)
            if len(self.positions) > self.length:
                self.positions.pop()

    # after the snake died
    def die(self):
        # set the snake len to 1
        self.length = 1
        # set the position at center
        self.positions = [CENTER]
        # stop the snake
        self.direction = STOP
        self.score = 0

    def draw(self, surface):
        for p in self.positions:
            r = pygame.Rect((p[0], p[1]), (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, self.color, r)
            pygame.draw.rect(surface, self.outline_color, r, 1)


class Food:
    def __init__(self):
        self.position = (0, 0)
        self.color = pygame.Color("darkgoldenrod3")
        self.outline_color = pygame.Color("slategrey")
        self.randomize_position()

    def randomize_position(self):
        rand_x = random.randint(0, int(GRID_WIDTH - 1))
        rand_y = random.randint(0, int(GRID_HEIGHT - 1))
        self.position = (rand_x * GRID_SIZE, rand_y * GRID_SIZE)

    def draw(self, surface):
        r = pygame.Rect((self.position[0], self.position[1]), (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.color, r)
        pygame.draw.rect(surface, self.outline_color, r, 1)


class World:
    def __init__(self):
        # snake object
        self.snake = Snake()
        # food object
        self.food = Food()

    # methods
    def update(self):
        self.snake.move()
        if self.snake.get_head_position() == self.food.position:
            self.snake.length += 1
            self.snake.score += 1
            self.food.randomize_position()

    def draw(self, surface):
        self.snake.draw(surface)
        self.food.draw(surface)

    def score(self):
        return self.snake.score

    def handle_keys(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.snake.turn(UP)
            elif event.key == pygame.K_DOWN:
                self.snake.turn(DOWN)
            elif event.key == pygame.K_LEFT:
                self.snake.turn(LEFT)
            elif event.key == pygame.K_RIGHT:
                self.snake.turn(RIGHT)

#Grid surfaces are created
def draw_grid(surface):
    for y in range(0, int(GRID_HEIGHT)):
        for x in range(0, int(GRID_WIDTH)):
            if (x+y) % 2 == 0:
                r = pygame.Rect((x * GRID_SIZE, y * GRID_SIZE), (GRID_SIZE, GRID_SIZE))
                pygame.draw.rect(surface, pygame.Color("lightslategrey"), r)
            else:
                r = pygame.Rect((x * GRID_SIZE, y * GRID_SIZE), (GRID_SIZE, GRID_SIZE))
                pygame.draw.rect(surface, pygame.Color("slategrey"), r)

pygame.font.init()
def run():
    # pygame constructor is called
    clock = pygame.time.Clock()
    # A window is set with specified size
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Snake Pygame Example")
    # Specified size window should be drawn to display
    surface = pygame.Surface(screen.get_size())
    surface = surface.convert()
    # draw_grid function is called for grid area for first time
    draw_grid(surface)

    world = World()

    font = pygame.font.SysFont("monospace", 16)
    # to exit from the game window capture the events
    running = True
    while running:
        for event in pygame.event.get():
            # when user click x button it will exit
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                # when user click ESC key it will exit
                if event.key == pygame.K_ESCAPE:
                    running = False
                    # other than esc
                else:
                    world.handle_keys(event)

        clock.tick(FPS)
        world.update()
        # clear screen
        draw_grid(surface)
        world.draw(surface)
        # scrren is drawn from 0,0 co-ordinates
        screen.blit(surface, (0, 0))
        # score is display on top left and updated
        text = font.render("Score {0}".format(world.score()), 1, pygame.Color("black"))
        # display the text on top left
        screen.blit(text, (5, 10))
        pygame.display.update()

def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/font.ttf", size)

class Button():
	def __init__(self, image, pos, text_input, font, base_color, hovering_color):
		self.image = image
		self.x_pos = pos[0]
		self.y_pos = pos[1]
		self.font = font
		self.base_color, self.hovering_color = base_color, hovering_color
		self.text_input = text_input
		self.text = self.font.render(self.text_input, True, self.base_color)
		if self.image is None:
			self.image = self.text
		self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
		self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

	def update(self, screen):
		if self.image is not None:
			screen.blit(self.image, self.rect)
		screen.blit(self.text, self.text_rect)

	def checkForInput(self, position):
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			return True
		return False

	def changeColor(self, position):
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			self.text = self.font.render(self.text_input, True, self.hovering_color)
		else:
			self.text = self.font.render(self.text_input, True, self.base_color)


FONT = pygame.font.Font(None, 32)

def runnable():
   # print("runnable")
    run()


def game():
    # Variables
    score = 0
    #user_age = age_input.get_value()
    user_name = user_input.get_value()
    clock = pygame.time.Clock()
    # A window is set with specified size
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Snake Pygame Example")
    # Specified size window should be drawn to display
    surface = pygame.Surface(screen.get_size())
    surface = surface.convert()
    # draw_grid function is called for grid area for first time
    draw_grid(surface)

    world = World()

    font = pygame.font.SysFont("monospace", 16)
    # to exit from the game window capture the events
    running = True
    while running:
        for event in pygame.event.get():
            # when user click x button it will exit
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                # when user click ESC key it will exit
                if event.key == pygame.K_ESCAPE:
                    running = F\alse
                    # other than esc
                else:
                    world.handle_keys(event)

        clock.tick(FPS)
        world.update()
        # clear screen
        draw_grid(surface)
        world.draw(surface)
        # scrren is drawn from 0,0 co-ordinates
        screen.blit(surface, (0, 0))
        # score is display on top left and updated
        text = font.render("Score {0}".format(world.score()), 1, pygame.Color("black"))
        # display the text on top left
        screen.blit(text, (5, 10))
        pygame.display.update()


user_input = menu.add.text_input('User: ')
#age_input = menu.add.text_input('Age: ')
menu.add.button('Start', game)
menu.add.button('Exit', pygame_menu.events.EXIT)

print(user_input)
#print(age_input)

menu.mainloop(SCREEN)


def main_menu():
        print("main menu")
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(30).render("MAIN MENU", True,(0,1,0))
        MENU_RECT = MENU_TEXT.get_rect(center=(200, 75))

        menu.add.label("MAIN MENU")

        print("242")

        menu.add.button('Comencem', runnable,font_name = FONT, font_color = 'green')

       # age_input = menu.add.text_input('Age: ', font_name=FONT, font_color='Black')

        menu.mainloop(SCREEN)
      #  PLAY_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(220, 220),
        #                      text_input="PLAY", font=get_font(30), base_color=(0,1,0), hovering_color=(1,1,1))
        # # OPTIONS_BUTTON = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(640, 400),
        #                         text_input="OPTIONS", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        # QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(640, 550),
        #                      text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        SCREEN.blit(MENU_TEXT,MENU_RECT)
        menu.mainloop(SCREEN)
        SCREEN.blit(menu)

        #PLAY_BUTTON.changeColor(MENU_MOUSE_POS)
       # PLAY_BUTTON.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
               # if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    run()
                    pygame.quit()
                    sys.exit()

        pygame.display.update()



if __name__ == '__main__':
    print("he")
    # this is the starting point
    # run function is called
    main_menu()


    # after using pygame we shutting down
    pygame.quit()