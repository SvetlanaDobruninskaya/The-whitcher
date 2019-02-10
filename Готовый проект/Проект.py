import pygame
import os
import random


def load_image(name, colorkey=None):
    fullname = os.path.join('Data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)
    image = image.convert_alpha()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    return image


def terminate():
    pygame.quit()


def start_screen():
    fon = pygame.transform.scale(load_image('fon.png'), (320, 570))
    screen.blit(fon, (0, 0))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()


class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self. board = [[0]*width for _ in range(height)]
        self.left = 10
        self.top = 5
        self.cell_size = 50

    def render(self):
        y = 0
        for i in range(self.height):
            x = 0
            for j in range(self.width):
                pygame.draw.rect(screen, (87, 145, 12), (self. left + x,
                                                         self.top + y,
                                                         self.cell_size,
                                                         self.cell_size), 1)
                x += self.cell_size
            y += self.cell_size

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def get_cell(self, mouse_pos):
        x, y = None
        for i in range(1, self.width + 1):
            if (self.left + self.cell_size * (i-1) < mouse_pos[0] <
                    self.left + self.cell_size * i):
                x = self.left + (i - 1) * self.cell_size
                break
        for i in range(1, self.height + 1):
            if (self.top + self.cell_size * (i - 1) < mouse_pos[1] <
                    self.top + self.cell_size * i):
                y = self.top + (i - 1) * self.cell_size
                break
        if x is None or y is None:
            return None
        return (x, y)

    def get_clicked(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        self.on_click(self, cell)

    def on_click(self, cell_coords):
        pass

class monsters_actions:
    def __init__(self):
        pass

    def new_level(monster_coords, castle_xp):
        n = 0
        coords_monsters1 = []
        monsters = pygame.sprite.Group()
        n1 = len(monster_coords)

        while n != n1 and flag_inboard:  # перемещение монстров вперед
            sprite = pygame.sprite.Sprite()
            x, y, image = monster_coords[n]
            if image == "troll":
                sprite.image = load_image("troll.png")
            elif image == "knight":
                sprite.image = load_image("Knight.png")
            sprite.rect = sprite.image.get_rect()
            sprite.rect.x = x
            y += 50
            sprite.rect.y = y
            sprite.add(monsters)
            if y < 450:
                coords_monsters1.append([x, y, image])
            else:
                if image == "troll":
                    castle_xp += -1
                elif image == "knight":
                    castle_xp += -5
            n += 1

        new_monster_draw = True
        monster_coords = coords_monsters1
        coords_monsters1 = []
        x_coords = []
        for i in range(3):  # пририсовка нового монстра
            image = random.choice(monster_choice)
            y = 5
            x = random.randrange(10, 310, 50)
            sprite = pygame.sprite.Sprite()
            if image == "troll":
                sprite.image = load_image("troll.png")
            elif image == "knight":
                sprite.image = load_image("Knight.png")
            elif image == "dragon":
                sprite.image = load_image("Dragon.png")
            sprite.rect = sprite.image.get_rect()
            if x not in x_coords:
                sprite.rect.x = x
            sprite.rect.y = y
            sprite.add(monsters)
            if x not in x_coords:
                monster_coords.append([x, y, image])
        return monsters, monster_coords, castle_xp
    
    def monster_fire_crash(monster_coords, points, k_x, k_y):
        monster_coords1 = monster_coords
        for j in monster_coords:
            monster_x, monster_y, image = j
            if ((y > monster_y and y < monster_y + 50) or
               (y + 40 < monster_y and y + 40 > monster_y + 50)):
                if ((x > monster_x and x < monster_x + 50) and
                   (y > monster_y and y < monster_y + 50)):
                    points += 1
                    del monster_coords1[monster_coords1.index(j)]
                    k_x = -k_x
                    k_y = -k_y
                elif ((x + 40 > monster_x and x + 40 <
                      monster_x + 50) and
                      (y > monster_y and y < monster_y + 50)):
                    points += 1
                    del monster_coords1[monster_coords1.index(j)]
                    k_x = -k_x
                    k_y = -k_y
                elif ((x + 40 > monster_x and x + 40 <
                      monster_x + 50) and
                      (y + 40 > monster_y and y + 40 <
                      monster_x + 50)):
                    points += 1
                    del monster_coords1[monster_coords1.index(j)]
                    k_x = -k_x
                    k_y = -k_y
                elif ((x > monster_x and x < monster_x + 50) and
                      (y + 40 > monster_y and y + 40 <
                      monster_y + 50)):
                    points += 1
                    del monster_coords1[monster_coords1.index(j)]
                    k_x = -k_x
                    k_y = -k_y
                monster_coords = monster_coords1

        monsters = pygame.sprite.Group()
        for k in monster_coords:
            sprite = pygame.sprite.Sprite()
            x_monster, y_monster, image_monster = k
            if image_monster == "knight":
                sprite.image = load_image("Knight.png")
            elif image_monster == "troll":
                sprite.image = load_image("troll.png")
            sprite.rect = sprite.image.get_rect()
            sprite.rect.x = x_monster
            sprite.rect.y = y_monster
            sprite.add(monsters)
        return monsters, monster_coords, points, k_x, k_y


pygame.init()
size = w, h = 320, 570
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
board = Board(6, 9)
board.set_view(10, 5, 50)
screen.fill((71, 37, 0))

points = 0

pygame.draw.rect(screen, (124, 252, 0), (10, 5, w-20, h-60), 0)
pygame.draw.rect(screen, (87, 145, 12), (10, 355, w-20, h-110), 0)

#music = False
# этот флаг отвечает за музыку.
# Если хотите другую смените флаг на True
#if music:
#    pygame.mixer.music.load(os.path.join('Data', 'Night_Witches.mp3'))
#    pygame.mixer.music.play(-1)
#elif not music:
#    pygame.mixer.music.load(os.path.join('Data', 'fon_music.mp3'))
#    pygame.mixer.music.play(-1)

castle = pygame.sprite.Group()
castle1 = pygame.sprite.Sprite()
castle1.image = load_image("замок.png")
castle1.rect = castle1.image.get_rect()
castle.add(castle1)
x = 10
y = 455
castle1.rect.x = x
castle1.rect.y = y
castle_xp = 10

fireman = pygame.sprite.Group()
fireman1 = pygame.sprite.Sprite()
fireman1.image = load_image("witcher.png")
fireman1.rect = fireman1.image.get_rect()
fireman.add(fireman1)
x = 135
y = 510
fireman1.rect.x = x
fireman1.rect.y = y

fires = pygame.sprite.Group()
fire = pygame.sprite.Sprite()
fire.image = load_image("fire.png")
fires.add(fire)

monster_coords = []
coords_monsters1 = []
x_coords = []
monster_choice = ["troll", "knight", "troll", "troll",
                  "knight", "troll", "troll", "troll", "troll", "knight"]
for i in range(3):
    x = random.randrange(10, 310, 50)
    if x not in x_coords:
        monster_coords.append([x, 5, "troll"])
    x_coords.append(x)

monsters = pygame.sprite.Group()
for i in monster_coords:
    sprite = pygame.sprite.Sprite()
    sprite.image = load_image("troll.png")
    x, y, image = i
    sprite.rect = sprite.image.get_rect()
    sprite.rect.x = x
    sprite.rect.y = y
    sprite.add(monsters)

game_over_group = pygame.sprite.Group()
game_over = pygame.sprite.Sprite()
game_over.image = load_image("Game_over.png")
game_over.rect = game_over.image.get_rect()
gameover_x = -320
game_over.rect.x = -320
game_over.rect.y = 0


coords1 = []
to_del = []

start_screen()

move = 20

flag_bdown = False
flag1 = True
flag_inboard = True
new_monster_draw = False
gameover_flag = False
you_can_push = False
have_nlevel = False

n = 1
pygame.time.set_timer(move, 10)
running = True
k_x = 1
k_y = -1

board.render()

castle.draw(screen)
fireman.draw(screen)
monsters.draw(screen)
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if gameover_flag:
            if event.type == pygame.MOUSEBUTTONDOWN:
                flag_bdown = True
                if event.pos[0] >= 150:
                    k_x = 1
                else:
                    k_x = -1
                k_y = -1
                x = 150
                y = 405
                coords = [[x, y, k_x, k_y, event.pos[0], event.pos[1]]]
                flag1 = True
            if event.type == move and flag_bdown:
                screen = pygame.display.set_mode(size)
                for i in coords:
                    x = int(i[0])
                    y = int(i[1])
                    if flag1:
                        if int(i[4]) >= 150:
                            mouse_x = int(i[4]) - 150
                        else:
                            mouse_x = 150 - int(i[4])
                        mouse_y = int(i[5])
                        plus_x = 2
                        if mouse_x == 0:
                            mouse_x = 1
                        plus_y = (plus_x * (410 - mouse_y)) / mouse_x
                    k_x = int(i[2])
                    k_y = int(i[3])
                    if x <= 10:
                        k_x = 1
                    if x >= 270:
                        k_x = -1
                    if y <= 5:
                        y = y + 1
                        k_y = 1

                    monsters, monster_coords, points, k_x, k_y = monsters_actions.monster_fire_crash(monster_coords, points, k_x, k_y)
                    
                    x = x + (plus_x * k_x)
                    if int(y) != int(y + (plus_y * k_y)):
                        y = y + (plus_y * k_y)
                    else:
                        y = y + 1

                    screen.fill((71, 37, 0))

                    pygame.draw.rect(screen, (124, 252, 0),
                                     (10, 5, w-20, h-60), 0)
                    pygame.draw.rect(screen,
                                     (87, 145, 12),
                                     (10, 455, w-20, 210), 0)

                    board.render()

                    fire.rect = fire.image.get_rect()
                    fire.rect.x = x
                    fire.rect.y = y
                    fires.draw(screen)
                    monsters.draw(screen)

                    if y <= 420:
                        coords1.append([x, y, k_x, k_y])
                    else:
                        have_nlevel = True
                    flag1 = False
                coords = coords1
                coords1 = []
            screen.fill((71, 37, 0))

            pygame.draw.rect(screen, (124, 252, 0), (10, 5, w-20, h-60), 0)
            pygame.draw.rect(screen, (87, 145, 12), (10, 455, w-20, 210), 0)
            fire.rect = fire.image.get_rect()
            fire.rect.x = x
            if y < 410:
                fire.rect.y = y
            else:
                fire.rect.y = -400
                if have_nlevel:
                    monster_coords1 = monster_coords
                    for i in to_del:
                        del (monster_coords1[monster_coords1.
                             index(monster_coords[i])])
                    monster_coords = monster_coords1
                    to_del = []
                    flag_bdown = False
                    fire.rect.y = 4000
                    y = 4000
                    monsters, monster_coords, castle_xp = monsters_actions.new_level(monster_coords, castle_xp)
                    have_nlevel = False

            fires.draw(screen)

            board.render()

            monsters.draw(screen)
            castle.draw(screen)
            fireman.draw(screen)
            font = pygame.font.Font(None, 34)
        else:
            screen.fill((255, 255, 255))
            if gameover_x != 0:
                gameover_x += 1
            else:
                you_can_push = True
            font = pygame.font.Font(None, 24)
            file_name = os.path.join('Data', 'max_point.txt')
            max_point = int(open(file_name, "r").read())            
            if points > max_point:
                max_point = points
                file = open(file_name, "w")
                file.write(str(max_point))
                file.close()
            end_text = ["Вы убили {} монстров.".format(points), "Ваш максимальный счет равен {}.".format(max_point)]
            game_over.rect.x = gameover_x
            game_over.rect.y = 0
            game_over.add(game_over_group)
            game_over_group.draw(screen)            
            text_y = 405
            for end in end_text:
                text = font.render(end, 1, (255, 255, 255))
                text_x = 35
                text_y += 20       
                screen.blit(text, (text_x, text_y))
        if castle_xp > 0:
            font = pygame.font.Font(None, 24)
            text = font.render("{}xp".format(castle_xp), 1, (255, 255, 255))
            text_x = 15
            text_y = 465
            screen.blit(text, (text_x, text_y))
            gameover_flag = True
        else:
            gameover_flag = False
        if event.type == pygame.MOUSEBUTTONDOWN and you_can_push:
            points = 0
            gameover_flag = True
            castle_xp = 10
            monster_coords = []
            coords_monsters1 = []
            x_coords = []
            monster_choice = ["troll", "knight", "troll", "troll",
                              "knight", "troll", "troll", "troll",
                              "troll", "knight"]
            for i in range(3):
                x = random.randrange(10, 310, 50)
                if x not in x_coords:
                    monster_coords.append([x, 5, "troll"])
                x_coords.append(x)

            monsters = pygame.sprite.Group()
            for i in monster_coords:
                sprite = pygame.sprite.Sprite()
                sprite.image = load_image("troll.png")
                x, y, image = i
                sprite.rect = sprite.image.get_rect()
                sprite.rect.x = x
                sprite.rect.y = y
                sprite.add(monsters)
            you_can_push = False
    clock.tick(50)
    pygame.display.flip()
pygame.quit()
