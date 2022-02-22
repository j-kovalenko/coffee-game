import sys
import pygame
import os
import random

pygame.init()
pygame.display.set_caption("coffee_game")

SIZE = (WIDTH, HEIGHT) = (450, 450)
screen = pygame.display.set_mode(SIZE)

clock = pygame.time.Clock()

max_speed = 7
price_count_speed = 30
count_kofe_on_field = 10
price_count_coffee = 30
coffee_count = 0
count_level = 0

get_coffee = False
is_alive = True


def terminate():
    pygame.quit()
    sys.exit()


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if name == 'status_bar.png':
        colorkey = image.get_at((45, 35))
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    if 'fon' in name:
        image = pygame.transform.scale(image,
                                       (450, 1350))  # тут идет обрезка изображений, а то изначально они гигантские
    elif name == 'kofe1.png':
        image = pygame.transform.scale(image, (40, 40))
    elif name == 'rectangle.png':
        image = pygame.transform.scale(image, (150, 26))
    elif name == 'kofe.png':
        image = pygame.transform.scale(image, (80, 80))
    return image


def start_screen():
    title = 'COFFEE GAME'
    fon = pygame.transform.scale(load_image('fon_new.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 70)
    string_rendered = font.render(title, True, pygame.Color((0, 4, 91)))
    intro_rect = string_rendered.get_rect()
    intro_rect.centerx = 225
    intro_rect.y = 100
    screen.blit(string_rendered, intro_rect)

    pygame.draw.rect(screen, (36, 221, 198), (50, 200, 350, 100))
    pygame.draw.rect(screen, (0, 4, 91), (50, 200, 350, 100), width=5)

    title = 'start'
    font = pygame.font.Font(None, 70)
    string_rendered = font.render(title, True, pygame.Color((0, 4, 91)))
    intro_rect = string_rendered.get_rect()
    intro_rect.centerx = 225
    intro_rect.y = 220
    screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if 50 <= event.pos[0] <= 400 and 200 <= event.pos[1] <= 300:
                    return
        pygame.display.flip()


class Player(pygame.sprite.Sprite):
    def __init__(self, max_speed):
        super(Player, self).__init__()

        self.image = load_image('kofe.png')
        self.rect = self.image.get_rect()

        self.rect.centerx = WIDTH / 2
        self.rect.centery = HEIGHT / 2

        self.max_speed = max_speed

    def update(self, max_speed):
        global get_coffee, is_alive, coffee_count

        if self.max_speed > 0:
            self.max_speed = max_speed
        else:
            self.max_speed = -max_speed

        self.rect.x += self.max_speed
        if self.rect.x >= 450 - 80:
            self.max_speed = -self.max_speed
            self.image = pygame.transform.flip(self.image, True, False)
        if self.rect.x <= 0:
            self.max_speed = -self.max_speed
            self.image = pygame.transform.flip(self.image, True, False)
        if pygame.sprite.spritecollide(self, kofe_objects, False) and is_alive:
            pygame.sprite.spritecollide(self, kofe_objects, True)
            coffee_count += 1
            get_coffee = True


class Background(pygame.sprite.Sprite):
    def __init__(self, max_speed):
        super(Background, self).__init__()

        self.image = load_image('fon_new.jpg')
        self.rect = self.image.get_rect()
        self.rect.bottom = 900

        self.max_speed = max_speed
        self.current_speed = -self.max_speed

    def update(self, max_speed):
        if self.max_speed > 0:
            self.max_speed = max_speed
        else:
            self.max_speed = -max_speed

        keys = pygame.key.get_pressed()
        if is_alive:
            if keys[pygame.K_UP]:
                self.current_speed = self.max_speed
        self.current_speed -= 0.1
        self.rect.bottom += self.current_speed

        if self.rect.bottom >= 1350:
            # global count_score
            # count_score += 1
            self.rect.bottom = 900
        if self.rect.bottom <= 450:
            # global count_score
            # count_score -= 1
            self.rect.bottom = 900


class Kofe(pygame.sprite.Sprite):
    def __init__(self, x, y, max_speed):
        super(Kofe, self).__init__()

        self.image = load_image('kofe1.png')
        self.rect = self.image.get_rect()

        self.rect.x = (random.randint(x, x + 400))
        self.rect.y = (random.randint(y, y + 400))

        self.max_speed = max_speed
        # self.count = count

        self.current_speed = -self.max_speed

    def update(self, count):
        keys = pygame.key.get_pressed()
        if is_alive:
            if keys[pygame.K_UP]:
                self.current_speed = self.max_speed
            for i in kofe_objects:
                if i.rect.top >= 450:
                    kofe_objects.remove(i)
                    kofe_objects.add(Kofe(0, -450, max_speed))
            if count > len(list(kofe_objects)):
                for i in range(count - len(list(kofe_objects))):
                    kofe_objects.add(Kofe(0, -450, max_speed))
        self.current_speed -= 0.1
        self.rect.bottom += self.current_speed


class Buttons(pygame.sprite.Sprite):
    def __init__(self, name, x):
        super(Buttons, self).__init__()

        self.image = load_image(name)
        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = 385


class Button_text(pygame.sprite.Sprite):
    def __init__(self, count, x, y, size):
        super(Button_text, self).__init__()

        intro_text = str(count)

        self.size = size
        font = pygame.font.Font(None, self.size)
        self.image = font.render(intro_text, True, [255, 255, 255])
        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y

    def update(self, count, x=None):
        intro_text = str(count)
        if x:
            self.rect.x = x
        print(self.rect.x, x)
        font = pygame.font.Font(None, self.size)
        self.image = font.render(intro_text, True, [255, 255, 255])


class RunningLine(pygame.sprite.Sprite):

    def __init__(self):
        super(RunningLine, self).__init__()

        self.image = load_image('rectangle.png')
        self.rect = self.image.get_rect()

        self.rect.x = 5
        self.rect.y = 399
        self.speed = 2

    def update(self):
        global is_alive
        global get_coffee
        # global coffeecount

        if is_alive and get_coffee:
            self.rect.x = 5
            self.rect.y = 399
            get_coffee = False
            # coffeecount += 1
        if self.rect.x < -150:
            self.speed = 0
            is_alive = False
        self.rect.x -= self.speed


class Count_Coffee(pygame.sprite.Sprite):

    def __init__(self, count_coffee):
        super(Count_Coffee, self).__init__()

        intro_text = str(count_coffee)

        font = pygame.font.Font(None, 100)
        self.image = font.render(intro_text, True, [0, 4, 91])
        self.rect = self.image.get_rect()

        self.rect.centerx = 225
        self.rect.y = 10

    def update(self, count_coffee):
        intro_text = str(count_coffee)

        font = pygame.font.Font(None, 100)
        self.image = font.render(intro_text, True, [0, 4, 91])


running = True
start_screen()

player = Player(max_speed)
background = Background(max_speed)
rl = RunningLine()
score = Count_Coffee(coffee_count)

all_objects = pygame.sprite.Group()
kofe_objects = pygame.sprite.Group()
status_bar_objects = pygame.sprite.Group()
button_count_coffee = pygame.sprite.Group()
button_speed = pygame.sprite.Group()
counter = pygame.sprite.Group()

counter.add(score)

sprite = pygame.sprite.Sprite()
sprite.image = load_image("status_bar_bg.png")
sprite.rect = sprite.image.get_rect()
sprite.rect.bottom = 450
status_bar_objects.add(sprite)
status_bar_objects.add(rl)
sprite = pygame.sprite.Sprite()
sprite.image = load_image("status_bar.png")
sprite.rect = sprite.image.get_rect()
sprite.rect.bottom = 450
status_bar_objects.add(sprite)

btn1 = Buttons('btn1_count.png', 340)
button_count_coffee.add(btn1)
text1_1 = Button_text(count_kofe_on_field, 390, 393, 25)
button_count_coffee.add(text1_1)
text1_2 = Button_text(price_count_coffee, 366, 410, 50)
button_count_coffee.add(text1_2)

btn2 = Buttons('btn2_speed.png', 240)
button_speed.add(btn2)
text2_1 = Button_text(max_speed, 290, 393, 25)
button_speed.add(text2_1)
text2_2 = Button_text(price_count_speed, 266, 410, 50)
button_speed.add(text2_2)

all_objects.add(background)
all_objects.add(player)

for i in range(count_kofe_on_field):
    kofe_objects.add(Kofe(0, 0, max_speed))

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if (340 <= event.pos[0] <= 426 and 385 <= event.pos[
                1] <= 445 and is_alive and count_kofe_on_field < 70 and coffee_count >= price_count_coffee):
                coffee_count -= price_count_coffee
                price_count_coffee *= 2
                count_kofe_on_field += 10
                text1_1.update(count_kofe_on_field)
                if count_kofe_on_field >= 70:
                    text1_2.update('MAX', 325)
                elif price_count_coffee // 100 > 0:
                    text1_2.update(price_count_coffee, 325)
                else:
                    text1_2.update(price_count_coffee)
            if (240 <= event.pos[0] <= 326 and 385 <= event.pos[
                1] <= 445 and is_alive and max_speed < 50 and coffee_count >= price_count_speed):
                coffee_count -= price_count_speed
                price_count_speed *= 2
                max_speed += 3
                text2_1.update(max_speed)
                if max_speed >= 50:
                    text2_2.update('MAX', 225)
                elif price_count_speed // 100 > 0:
                    text2_2.update(price_count_speed, 225)
                else:
                    text2_2.update(price_count_speed)

    all_objects.update(max_speed)
    kofe_objects.update(count_kofe_on_field)
    rl.update()
    counter.update(coffee_count)

    all_objects.draw(screen)
    kofe_objects.draw(screen)
    status_bar_objects.draw(screen)
    button_count_coffee.draw(screen)
    button_speed.draw(screen)
    counter.draw(screen)

    pygame.display.flip()
    clock.tick(25)
pygame.quit()
