import sys
import pygame
import os
import random

pygame.init()
pygame.display.set_caption("coffee_game")

SIZE = (WIDTH, HEIGHT) = (450, 450)
screen = pygame.display.set_mode(SIZE)

clock = pygame.time.Clock()



def terminate():
    pygame.quit()
    sys.exit()


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if name == 'fon.jpg':
        image = pygame.transform.scale(image,
                                       (450, 1350))  # тут идет обрезка изображений, а то изначально они гигантские
    elif name == 'kofe1.png':
        image = pygame.transform.scale(image, (40, 40))
    elif name == 'kofe.png':
        image = pygame.transform.scale(image, (80, 80))
    return image


def start_screen():
    intro_text = ["Перемещение героя", "",
                  "Герой двигается",
                  "Карта на месте,"]

    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()


class Player(pygame.sprite.Sprite):
    max_speed = 5

    def __init__(self):
        super(Player, self).__init__()

        self.image = load_image('kofe.png')
        self.rect = self.image.get_rect()

        self.rect.centerx = WIDTH / 2
        self.rect.centery = HEIGHT / 2

    def update(self):
        self.rect.x += self.max_speed
        if self.rect.x >= 450 - 80:
            self.max_speed = -self.max_speed
            self.image = pygame.transform.flip(self.image, True, False)
        if self.rect.x <= 0:
            self.max_speed = -self.max_speed
            self.image = pygame.transform.flip(self.image, True, False)
        if pygame.sprite.spritecollide(self, kofe_objects, False):
            pygame.sprite.spritecollide(self, kofe_objects, True)


class Background(pygame.sprite.Sprite):
    max_speed = 7

    def __init__(self):
        super(Background, self).__init__()

        self.image = load_image('fon.jpg')
        self.rect = self.image.get_rect()
        self.rect.bottom = 900

        self.current_speed = -self.max_speed

    def update(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:
            self.current_speed = self.max_speed
        self.current_speed -= 0.1
        self.rect.bottom += self.current_speed

        if self.rect.bottom >= 1350:
            self.rect.bottom = 900
        if self.rect.bottom <= 450:
            self.rect.bottom = 900


class Kofe(pygame.sprite.Sprite):
    max_speed = 7

    def __init__(self, x, y):
        super(Kofe, self).__init__()

        self.image = load_image('kofe1.png')
        self.rect = self.image.get_rect()

        self.rect.x = (random.randint(x, x + 400))
        self.rect.y = (random.randint(y, y + 400))

        self.count = count

        self.current_speed = -self.max_speed

    def update(self, count):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:
            self.current_speed = self.max_speed
        self.current_speed -= 0.1
        self.rect.bottom += self.current_speed
        for i in kofe_objects:
            if i.rect.top >= 450:
                kofe_objects.remove(i)
                kofe_objects.add(Kofe(0, -450))
        if count > len(list(kofe_objects)):
            for i in range(count - len(list(kofe_objects))):
                kofe_objects.add(Kofe(0, -450))

class Buttons(pygame.sprite.Sprite):
    def __init__(self, name, x):
        super(Buttons, self).__init__()

        self.image = load_image(name)
        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = 385

class Button_text(pygame.sprite.Sprite):
    def __init__(self, x):
        super(Button_text, self).__init__()

        self.price = 10
        intro_text = str(self.price)

        font = pygame.font.Font(None, 70)
        self.image = font.render(intro_text, True, [255, 255, 255])
        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = 400

    def update(self):
        self.price *= 1.5
        self.price = int(self.price)
        intro_text = str(self.price)

        font = pygame.font.Font(None, 70)
        self.image = font.render(intro_text, True, [255, 255, 255])


running = True
start_screen()

count = 10

player = Player()
background = Background()

all_objects = pygame.sprite.Group()
kofe_objects = pygame.sprite.Group()

button_count_coffee = pygame.sprite.Group()
sprite = pygame.sprite.Sprite()
sprite.image = load_image("status_bar.png")
sprite.rect = sprite.image.get_rect()
sprite.rect.bottom = 450
button_count_coffee.add(sprite)

btn1 = Buttons('btn1_count.png', 300)
text1 = Button_text(320)
button_count_coffee.add(btn1)
button_count_coffee.add(text1)

for i in range(count):
    kofe_objects.add(Kofe(0, 0))

all_objects.add(background)
all_objects.add(player)
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if 300<=event.pos[0]<= 390 and 385<=event.pos[1]<=445:
                count *= 1.5
                count = int(count)
                text1.update()

    all_objects.update()
    kofe_objects.update(count)

    all_objects.draw(screen)
    kofe_objects.draw(screen)
    button_count_coffee.draw(screen)

    pygame.display.flip()
    clock.tick(25)
pygame.quit()
