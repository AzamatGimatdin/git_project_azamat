import pygame
import sys


FPS = 50
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, tile_height * pos_y + 5)
        

def terminate():
    pygame.quit()
    sys.exit()

def start_screen():
    intro_text = ["ЗАСТАВКА", "",
                  "Правила игры",
                  "Если в правилах несколько строк,",
                  "приходится выводить их построчно"]

    fon = pygame.transform.scale(pygame.image.load('Lesson7/data/fon.jpg'), (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 100
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 80
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(FPS)


def load_level(filename):
    filename = "Lesson7/data/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
 
    max_width = max(map(len, level_map))

    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)         
    return new_player, x, y


pygame.init()
pygame.display.set_caption('Передвижение героя')
tile_images = {
    'wall': pygame.image.load('Lesson7/data/box.png'),
    'empty': pygame.image.load('Lesson7/data/grass.png')
}
tile_width = tile_height = 50
player_image = pygame.image.load('Lesson7/data/mar.png')
level = list(load_level('map.txt'))
player, level_x, level_y = generate_level(level)
player_x, player_y = player.rect.x // tile_height - 1, player.rect.y // tile_height - 1
size = width, height = tile_height * level_x, tile_height * level_y
screen = pygame.display.set_mode(size)
running = True
clock = pygame.time.Clock()
start_screen()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == 119:
            if player_y - 1 > 0 and level[player_y - 1][player_x] != '#':
                player_y -= 1
                player.rect.y -= tile_height
        elif event.type == pygame.KEYDOWN and event.key == 115:
            if player_y + 1 < level_y and level[player_y + 1][player_x] != '#':
                player_y += 1
                player.rect.y += tile_height
        elif event.type == pygame.KEYDOWN and event.key == 97:
            if player_x - 1 > 0 and level[player_y][player_x - 1] != '#':
                player_x -= 1
                player.rect.x -= tile_height
        elif event.type == pygame.KEYDOWN and event.key == 100:
            if player_y + 1 < level_x and level[player_y][player_x + 1] != '#':
                player_y += 1
                player.rect.y += tile_height
    tiles_group.draw(screen)
    tiles_group.update()
    player_group.draw(screen)
    player_group.update()
    pygame.display.flip()
pygame.quit()