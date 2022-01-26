import sys
import pygame
import os
import random

pygame.init()
pygame.display.set_caption("coffee_game")

SIZE = (WIDTH, HEIGHT) = (450, 450)
screen = pygame.display.set_mode(SIZE)

clock = pygame.time.Clock()

count = 10


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
    else:
        image = pygame.transform.scale(image, (80, 80))
    return image


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


player = Player()
background = Background()

all_objects = pygame.sprite.Group()
kofe_objects = pygame.sprite.Group()

for i in range(count):
    kofe_objects.add(Kofe(0, 0))

all_objects.add(background)
all_objects.add(player)
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit(0)

    screen.fill(color="white")

    all_objects.update()
    kofe_objects.update(count)

    all_objects.draw(screen)
    kofe_objects.draw(screen)

    pygame.display.flip()
    clock.tick(25)
