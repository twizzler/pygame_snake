import pygame
import textinput
import sys
import json
import random
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    K_n,
    K_o,
    K_w,
    K_a,
    K_s,
    K_d,
    K_RETURN,
)

pygame.init()
pygame.display.set_caption("The snake game !")


class Game:
    def __init__(self):
        self.white = (255, 255, 255)
        self.black = (0, 0, 0)
        self.red = (255, 0, 0)
        self.blue = (0, 0, 255)
        self.green = (0, 255, 0)

        self.background = pygame.image.load("assets/images/home_bg.png")
        self.apple_image = pygame.image.load("assets/images/apple.png")
        self.original_snake_head_image = pygame.image.load("assets/images/snake_head.png")
        self.snake_body_image = pygame.image.load("assets/images/snake_body.png")
        self.original_snake_tail = pygame.image.load("assets/images/snake_tail.png")
        self.snake_tail = self.original_snake_tail
        self.snake_head_image = self.original_snake_head_image

        self.apple_sound = pygame.mixer.Sound("assets/sounds/apple_sound.wav")

        self.direction = "up"

        self.SCREEN_WIDTH = 800
        self.SCREEN_HEIGHT = 500

        self.screen = pygame.display.set_mode([self.SCREEN_WIDTH, self. SCREEN_HEIGHT])

        self.running = True
        self.paused = False
        self.agreed = False

        self.snake_block = 25
        self.apple_block = 25

        self.snake_x = 0
        self.snake_y = 0
        self.apple_x = 0
        self.apple_y = 0

        self.center = (self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2)

        self.width_grid = 0
        self.height_grid = 0

        self.snake_x_change = 0
        self.snake_y_change = 0

        self.snake_list = list()
        self.snake_head = list()
        self.snake_length = 2

        self.score = 0
        self.show_score_page = False
        with open('scores.json') as f:
            self.scores = json.load(f)
        self.name = ""

        self.clock = pygame.time.Clock()

        self.velocity = 400

        self.text_input = textinput.TextInput()

    def rotate(self):
        """ If you want to get rid of the snake tail for now since it's buggy, you can simply remove each
            self.snake_tail = ... line. Check the draw method also, I've left some comments.
        """

        if self.direction == "down":
            self.snake_head_image = pygame.transform.rotate(self.original_snake_head_image, 180)
            self.snake_tail = pygame.transform.rotate(self.original_snake_tail, 180)
        elif self.direction == "up":
            self.snake_head_image = self.original_snake_head_image
            self.snake_tail = self.original_snake_tail
        elif self.direction == "left":
            self.snake_head_image = pygame.transform.rotate(self.original_snake_head_image, 90)
            self.snake_tail = pygame.transform.rotate(self.original_snake_tail, 90)
        elif self.direction == "right":
            self.snake_head_image = pygame.transform.rotate(self.original_snake_head_image, 270)
            self.snake_tail = pygame.transform.rotate(self.original_snake_tail, 270)

    def draw_grid(self):
        self.width_grid = [x * 25 for x in range(0, self.SCREEN_WIDTH)]
        self.height_grid = [y * 25 for y in range(0, self.SCREEN_WIDTH)]

        # You can uncomment this to see the grid

        """for grid_x in self.width_grid:
            pygame.draw.line(self.screen, self.white, [0, grid_x], [self.SCREEN_WIDTH, grid_x], 2)
            if grid_x >= 600:
                break
        for grid_y in self.height_grid:
            pygame.draw.line(self.screen, self.white, [grid_y, 0], [grid_y, self.SCREEN_WIDTH], 2)
            if grid_y >= 600:
                break"""

    def set_position(self, thing):
        if thing == "snake":
            self.snake_x = self.SCREEN_WIDTH / 2
            self.snake_y = self.SCREEN_HEIGHT / 2
        if thing == "apple":
            self.apple_x = random.choice(self.width_grid[2:24])
            self.apple_y = random.choice(self.height_grid[2:16])

    def draw(self, obj):
        """Get rid of the self.snake_tail line if you want to get rid of the tail: ref. rotate method."""

        if obj == "snake":
            self.screen.blit(self.snake_head_image, (self.snake_list[-1][0], self.snake_list[-1][1]))
            for XnY in self.snake_list[:-1]:
                x, y = round(XnY[0] / 25) * 25, round(XnY[1] / 25) * 25
                if len(self.snake_list) == 2:
                    self.screen.blit(self.snake_tail, (x, y))
            if len(self.snake_list) > 2:
                for XnY in self.snake_list[1:-1]:
                    x, y = round(XnY[0] / 25) * 25, round(XnY[1] / 25) * 25
                    pygame.draw.rect(self.screen, self.green, (x, y, self.snake_block, self.snake_block))
                x, y = round(self.snake_list[0][0] / 25) * 25, round(self.snake_list[0][1] / 25) * 25
                self.screen.blit(self.snake_tail, (x, y))
        elif obj == "apple":
            self.screen.blit(self.apple_image, (self.apple_x, self.apple_y))
            # pygame.draw.rect(self.screen, self.red, (self.apple_x, self.apple_y, self.apple_block, self.apple_block))

    def set_keys_direction(self):
        """
           You can easily add keys here and make them do things, whatever you'd like. However, make sure the key
           is imported at the beginning of the file if you want to keep my way of doing things.
        """

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == KEYDOWN:
                if self.agreed:
                    if event.key == K_DOWN:
                        self.snake_y_change = self.velocity
                        self.snake_x_change = 0
                        self.direction = "down"
                    if event.key == K_RIGHT:
                        self.snake_x_change = self.velocity
                        self.snake_y_change = 0
                        self.direction = "right"
                    if event.key == K_UP:
                        self.snake_y_change = -self.velocity
                        self.snake_x_change = 0
                        self.direction = "up"
                    if event.key == K_LEFT:
                        self.snake_x_change = -self.velocity
                        self.snake_y_change = 0
                        self.direction = "left"
                    if event.key == K_s:
                        if not self.paused:
                            self.direction = "down"
                            self.snake_y_change = self.velocity
                            self.snake_x_change = 0
                        else:
                            self.show_score_page = True
                    if event.key == K_w:
                        self.direction = "up"
                        self.snake_y_change = -self.velocity
                        self.snake_x_change = 0
                    if event.key == K_d:
                        self.direction = "right"
                        self.snake_x_change = self.velocity
                        self.snake_y_change = 0
                    if event.key == K_a:
                        self.direction = "left"
                        self.snake_x_change = -self.velocity
                        self.snake_y_change = 0
                    if event.key == K_n:
                        sys.exit()
                        pygame.quit()  # unreachable, but I keep it because I am a lazy coder
                    if event.key == K_o:
                        self.paused = False
                        self.score = 0
                    if event.key == K_ESCAPE:
                        self.snake_length += 1
                else:
                    if event.key == K_ESCAPE:
                        self.show_score_page = False
                    if event.key == K_RETURN:
                        self.agreed = True

        if not self.agreed:
            self.pick_name(events)

    def show_score(self):
        """
        Obviously this still has to be correctly implemented. Good luck or wait for me to push updates, if I do.
        """

        test = [25, 50, 75, 100, 125, 150]
        if self.show_score_page:
            self.screen.blit(self.background, (0, 0))
            self.show_text("Scores:", (self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2 - 100), self.white)
            for name, score in self.scores.items():
                print("{0}: {1}".format(name, score))
                for y in test:
                    self.show_text("{0}: {1}".format(name, score),
                                   (self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2 + y), self.white)

    def build_snake(self):
        x, y = round(self.snake_x / 25) * 25, round(self.snake_y / 25) * 25

        snake_head = list()
        snake_head.append(x)
        snake_head.append(y)
        if len(self.snake_list) <= 0 or snake_head != self.snake_list[-1]:
            self.snake_list.append(snake_head)

        """
            You could place the 2 blocks of code below in the snake_bit_check method, however make sure
            you call it here: self.snake_bit_check()
        """

        if len(self.snake_list) > self.snake_length:
            del self.snake_list[0]

        for snake in self.snake_list[:-1]:
            if snake == snake_head:
                self.snake_reset()

        self.rotate()
        self.draw("snake")

    def check_apple_eaten(self):
        x, y = round(self.snake_x / 25) * 25, round(self.snake_y / 25) * 25
        if x == self.apple_x and y == self.apple_y:
            self.apple_sound.play()
            self.set_position("apple")
            self.snake_length += 1
            self.score += 1

    def snake_borders_check(self):
        x, y = round(self.snake_x / 25) * 25, round(self.snake_y / 25) * 25
        if x < 50 or x > self.SCREEN_WIDTH - 75:
            self.snake_reset()
        if y < 50 or y > self.SCREEN_HEIGHT - 75:
            self.snake_reset()

    def snake_reset(self):
        """When the snake dies, do what you want."""

        self.paused = True
        self.set_position("snake")
        self.set_position("apple")
        del self.snake_list[1:]
        self.snake_length = 2

    def snake_bit_check(self):
        pass

        """
            The code below isn't working and it is improved in the build_snake function if you want to put it here.
            You can remove the code below.
        """

        """if len(self.snake_list) >= 6:
            for snake in self.snake_list[2:]:
                if self.snake_list[0][0] == snake[0] and self.snake_list[0][1] == snake[1]:
                    print("SnakeList[0][0]: {0} || SnakeList[0][1]: {0}".format(self.snake_list[0][0],
                                                                                self.snake_list[0][1]))
                    print("snake: {0}".format(snake))

                    self.snake_reset()"""

    # Could be improved so it aligns the text automatically I suppose
    def show_text(self, message, position, font_color, font_name="assets/fonts/arial_narrow_7.ttf", font_size=32):
        font = pygame.font.Font(font_name, font_size)
        text = font.render(message, True, font_color)
        text_rect = text.get_rect(center=position)

        self.screen.blit(text, text_rect)

    def game_over(self):
        test = [25, 50, 75, 100, 125, 150]
        self.screen.blit(self.background, (0, 0))

        # Well, to be continued
        """self.show_text("Scores:",
                       (self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2 - 100), self.white)
        for name, score in self.scores.items():
            print("{0}: {1}".format(name, score))
            for y in test:
                self.show_text("{0}: {1}".format(name, score),
                               (self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2 + y), self.white)"""

        self.show_text("You lost. Would you like to play again ?",
                       (self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2 - 100), self.white)
        self.show_text("Hit O - for Yes or hit - N for No",
                       (self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2), self.white)
        self.show_text("To see the score, hit S",
                       (self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2 + 100), self.white)

    def pick_name(self, events):
        self.text_input.update(events)

        self.show_text("Name: ", [300, 250], self.black)
        pygame.draw.rect(self.screen, self.black, (350, 230, 200, 40), 2)
        self.screen.blit(self.text_input.get_surface(), (360, 240))

        self.name = self.text_input.get_text()

    def check_agreement(self):
        pass
        # Useless for now

    def save_score(self):
        self.scores[self.name] = self.score

        with open('scores.json', 'w', encoding='utf-8') as f:
            json.dump(self.scores, f, ensure_ascii=False, indent=4)

            """
            You should continue working on this. Unless I push an update first.
            """

    def game(self):
        self.draw_grid()
        self.set_position("snake")
        self.set_position("apple")

        while self.running:
            """Game loop, everything goes through this."""
            delta_t = self.clock.tick(60)

            self.screen.blit(self.background, (0, 0))
            self.set_keys_direction()

            if self.agreed:
                self.screen.blit(self.background, (0, 0))

                self.show_text("Your score: {0}".format(self.score), (125, 20), self.white)
                self.show_text("Your name: {0}".format(self.name), (350, 20), self.white)

                self.draw_grid()

                self.draw("apple")

                self.build_snake()

                self.check_apple_eaten()

                self.snake_bit_check()

                self.snake_borders_check()
            else:
                self.check_agreement()

            if not self.paused:
                """step is used to control the snake's velocity and maintain a good amount of FPS which is 60 in 
                   our case
                """

                step = delta_t / 1000
                self.snake_x += self.snake_x_change * step
                self.snake_y += self.snake_y_change * step
            else:
                self.save_score()
                self.game_over()
                if self.show_score_page:
                    self.show_score()

            self.clock.tick(60)  # 60 FPS

            pygame.display.flip()


game = Game()

game.game()


pygame.quit()
