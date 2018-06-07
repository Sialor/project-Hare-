import pygame
import time
import os
import random


class Vector2:
    def __init__(self, _x=0, _y=0):
        self.x, self.y = _x, _y


class Transform:
    def __init__(self, _x=0, _y=0, _xd=0, _yd=0, _s=1):
        self.position = Vector2(_x, _y)
        self.direction = Vector2(_xd, _yd)
        self.side = _s


class Animation:
    def __init__(self, _prfx="", _skip=1):
        self.prfx = _prfx
        self.frame = 0
        self.frames = 1
        self.skip = _skip
        self.skip_frames = self.skip
        self.animation = []
        self.canvas = None

        for name in os.listdir(self.prfx[:len(self.prfx) - 2]):
            if os.path.isfile(os.path.join(self.prfx[:len(self.prfx) - 2], name)):
                self.animation.append(pygame.image.load(self.prfx[:len(self.prfx) - 2] + name))
                self.frames += 1

    def play(self, _object):
        self.canvas = pygame.Surface((_object.size.x, _object.size.y), pygame.SRCALPHA, 32)

        if self.skip_frames == 0:
            self.skip_frames = self.skip

        if self.frame == self.frames - 1:
            self.frame = 0

        self.canvas.blit(self.animation[self.frame], (0, 0))

        window.blit(self.canvas, (graph_width // 2 - player.size.x // 2 + _object.transform.position.x - player.transform.position.x, graph_height // 2 - player.size.y // 2 + _object.transform.position.y - player.transform.position.y))

        if self.skip_frames == self.skip:
            self.frame += 1

        self.skip_frames -= 1

    def play_centre(self, _side):
        self.canvas = pygame.Surface((player.size.x, player.size.y), pygame.SRCALPHA, 32)

        if self.skip_frames == 0:
            self.skip_frames = self.skip

        if self.frame == self.frames - 1:
            self.frame = 0

        self.canvas.blit(self.animation[self.frame], (0, 0))

        if _side == 0:
            self.canvas = pygame.transform.flip(self.canvas, 1, 0)

        window.blit(self.canvas, (graph_width // 2 - player.size.x // 2, graph_height // 2 - player.size.y // 2))

        if self.skip_frames == self.skip:
            self.frame += 1

        self.skip_frames -= 1


class Block:
    def __init__(self, _x=0, _y=0, _w=0, _h=0):
        self.transform = Transform(_x, _y)
        self.size = Vector2(_w, _h)

    def render(self):
        pygame.draw.rect(window, (150, 75, 0), (graph_width // 2 - player.size.x // 2 + self.transform.position.x - player.transform.position.x, graph_height // 2 - player.size.y // 2 + self.transform.position.y - player.transform.position.y, self.size.x, self.size.y), 0)


class Fruit:
    def __init__(self, _x=0, _y=0, _w=0, _h=0):
        self.transform = Transform(_x, _y)
        self.size = Vector2(_w, _h)

        self.state = "stay"
        self.animator = {
            "stay": Animation("anim/fruit/stay/00", 1),
            "rotate": Animation("anim/fruit/rotate/00", 1)
        }

        self.count = random.randint(1, self.animator["stay"].frames - 1)

        self.sound_pickup = pygame.mixer.Sound(sounds["pickup_coin"])

    def render(self):
        if self.state == "stay":
            if self.count == 3 * self.animator["stay"].frames:
                self.animator["stay"].frame = 0
                self.state = "rotate"
                self.count = 0
        elif self.state == "rotate":
            if self.count == self.animator["rotate"].frames:
                self.animator["rotate"].frame = 0
                self.state = "stay"
                self.count = 0

        self.count += 1

        self.animator[self.state].play(self)


class Player:
    def __init__(self, _x=0, _y=0, _w=0, _h=0, _max_speed=5, _speed=1, _max_gravity=9.8, _gravity=0.3, _max_jump=10, _jump=2.5, _health=3, _side=0):
        self.transform = Transform(_x, _y, 0, 0, _side)
        self.size = Vector2(_w, _h)
        self.max_speed = _max_speed
        self.speed = _speed
        self.max_gravity = _max_gravity
        self.gravity = _gravity
        self.max_jump = _max_jump
        self.jump = _jump

        self.health = _health

        self.state = "idle"
        self.animator = {
                "idle": Animation("anim/hare/idle/00", 20),
                "walk": Animation("anim/hare/walk/00", 4),
                "jump": Animation("anim/hare/jump/00", 16)
                }

        self.isJumping = False
        self.isGrounding = False
        self.isWalking = False

        self.sound_step1 = pygame.mixer.Sound(sounds["step1"])
        self.sound_step2 = pygame.mixer.Sound(sounds["step2"])
        self.sound_jump = pygame.mixer.Sound(sounds["jump"])

    def render(self):
        self.animator[self.state].play_centre(self.transform.side)


# ===========GAME SETTINGS====================
graph_width = 1024
graph_height = 768
# ==

# =========WORLD======
world = [
    '----------------------------------------------------------------------------------------------',
    '----------------------------------------------------------------------------------------------',
    '----------------------------------------------------------------------------------------------',
    '----------------------------------------------------------------------------------------------',
    '-----------000000----------------#000--000#---------------------------------------------------',
    '-----------######----------------#000--000#---------------------------------------------------',
    '---------------------------------#000--000#-----------------------------------------####------',
    '---------------------------------#00-00-00#----------------------------------------#----#-----',
    '---------------------------------#0-0000-0#----------------------------------------#----#-----',
    '--------------------------------#--000000--#---------------------------------------#----#-----',
    '--------------------------------#-00000000-#----###-----------------------------###-----#-----',
    '--------------------------------#0000000000#-------#---------------------------#--------#-----',
    '---------------------------------##########--------#---------------------------#--------#-----',
    '---------------------------------------------------#---------------------------#--------#-----',
    '-###-----------------------------------------------###-0----0-##-0----0-##-0---#--------#-----',
    '-------------0----0--------------------------------#---0----0----0----0----0---#--------#-----',
    '-----------##########------------------------------#---------------------------#--------#-----',
    '---------------------------------------------------#---------------------------#--------#-----',
    '--------###----------#-----------------------------#0---##---00---##---00---##-#--------#-----',
    '----------------------###------------------#####---#---------------------------#--------#-----',
    '---------------------------------------------------#---------------------------#--------#-----',
    '---------------------------------------------------#---------------------------#--------#-----',
    '####---------------0000000---------###-------------###--------##--------##-----#--------#-----',
    '---------------------------------------------------#0-------------------------0#--------#-----',
    '----------------################--------------------############################--------#-----',
    '---#####-----------------------#-----------------------------------------------#--------#-----',
    '-------------------------------#-----------------------------------------------#--------#-----',
    '-------------------------------#-----------------------------------------------#--------#-----',
    '-------------####--------------#-----------------------------------------------#--------#-----',
    '-------------------------------#------------------------0----0----0000---0---0-#--------#-----',
    '-------------------------------#------------------------#----#---0####---#--0#-#--------#-----',
    '-------------------------------#00----------------------#----#---#-------#00#--#--------#-----',
    '-------#####-------------------######-------------------#----#---#-------###0--#--------#-----',
    '--------------------------------------------------------#0000#---#0000---#--#0-#--------#-----',
    '-----------------------######----------------------------####-----####---#---#-#--------#-----',
    '-------------------------------------------------------------------------------#-------#------',
    '----------------------------0000------------------------------------------------#######-------',
    '----------------------------0000-----------------------####-----------------------------------',
    '------------#####000000000000000000000000000--------------------------------------------------'
]

world_size = 32

world_x = len(world[0]) - 1
world_y = len(world) - 1
# ==

# =======PYGAME==========
pygame.init()
font_debug = pygame.font.SysFont("Times New Roman", 16)
window = pygame.display.set_mode((graph_width, graph_height), pygame.DOUBLEBUF, 32)
clock = pygame.time.Clock()
# ==

window.blit(font_debug.render("жди...", True, (255, 255, 255)), (graph_width // 2, graph_height // 2))
pygame.display.flip()

# =========SOUNDS======
sounds = {
    "pickup_coin": "sounds/pickup_coin.ogg",
    "step1": "sounds/hit_hurt1.ogg",
    "step2": "sounds/hit_hurt2.ogg",
    "jump": "sounds/jump.ogg",
    "music": "sounds/music.ogg"
}

pygame.mixer.music.load(sounds["music"])
pygame.mixer.music.play(-1)

# =========ITEMS========
blocks = []
fruits = []

w = 0
s = 0

for w in range(len(world)):
    for s in range(len(world[w])):
        if world[w][s] == '#':
            blocks.append(Block(s * world_size + s, w * world_size + w, world_size, world_size))

        if world[w][s] == '0':
            fruits.append(Fruit(s * world_size + s, w * world_size + w, world_size, world_size))
# ==

player = Player(32, 32, 64, 128)

# =========CAMERA=============
cam_transform = Transform(0, 0)
# ==

chanel1 = None
chanel2 = None

debug = False
play = True
while play:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            play = False

        if e.type == pygame.KEYDOWN:

            # Событие "Прыжок"
            if e.key == pygame.K_UP or e.key == pygame.K_w:
                if player.isGrounding:
                    chanel1 = player.sound_jump.play()
                    player.isGrounding = False
                    time.sleep(0.019)
                    player.isJumping = True
                    player.state = "jump"

            # Событие "Ходьба"
            if e.key == pygame.K_LEFT or e.key == pygame.K_a:
                player.isWalking = True
                player.state = "walk"
                player.transform.side = 0

            if e.key == pygame.K_RIGHT or e.key == pygame.K_d:
                player.isWalking = True
                player.state = "walk"
                player.transform.side = 1

            # Вкл/Выкл Debug
            debug = not debug if e.key == pygame.K_F1 else debug

        if e.type == pygame.KEYUP:

            # Событие "Прыжок"
            if e.key == pygame.K_UP or e.key == pygame.K_w:
                player.isJumping = False
                player.animator["jump"].frame = 0
                player.animator["jump"].skip_frames = 0

            # Событие "Ходьба"
            if e.key == pygame.K_LEFT or e.key == pygame.K_a or e.key == pygame.K_RIGHT or e.key == pygame.K_d:
                player.isWalking = False
                player.animator["walk"].frame = 0
                player.animator["walk"].skip_frames = 0
                player.state = "idle"

    # Движ вправо
    if pygame.key.get_pressed()[pygame.K_RIGHT] or pygame.key.get_pressed()[pygame.K_d]:
        player.transform.side = 1

        if player.transform.direction.x < player.max_speed:
            player.transform.direction.x += player.speed
        else:
            player.transform.direction.x = player.max_speed

    # Движ влево
    elif pygame.key.get_pressed()[pygame.K_LEFT] or pygame.key.get_pressed()[pygame.K_a]:
        player.transform.side = 0

        if player.transform.direction.x > -player.max_speed:
            player.transform.direction.x -= player.speed
        else:
            player.transform.direction.x = -player.max_speed
    else:
        if abs(player.transform.direction.x) - 0.5 <= 0.5:
            player.transform.direction.x = 0

        if player.transform.direction.x > 0:
            player.transform.direction.x -= player.speed * 0.9
        elif player.transform.direction.x < 0:
            player.transform.direction.x += player.speed * 0.9

    # Нарастание прыжка
    if pygame.key.get_pressed()[pygame.K_UP] or pygame.key.get_pressed()[pygame.K_w]:
        if player.transform.direction.y > -player.max_jump and player.isJumping:
            player.transform.direction.y -= player.jump
        else:
            player.isJumping = False

    player.transform.position.x += player.transform.direction.x
    player.transform.position.y += player.transform.direction.y

    player.isGrounding = False

    # Ограничение прохода за границы уровня
    if player.transform.position.x < 0:
        player.transform.position.x = 0
    elif player.transform.position.x + player.size.x > (world_x + 1) * world_size + s:
        player.transform.position.x = (world_x + 1) * world_size - player.size.x + s

    if player.transform.position.y < 0:
        player.transform.position.y = 0
    elif player.transform.position.y + player.size.y > (world_y + 1) * world_size + w:
        if not player.isJumping:
            player.isGrounding = True
        player.transform.position.y = (world_y + 1) * world_size - player.size.y + w

    # Гравитация
    if not player.isJumping:
        if player.transform.direction.y < player.max_gravity:
            player.transform.direction.y += player.gravity

        if abs(player.transform.direction.y - player.max_gravity) <= 0.05:
            player.transform.direction.y = player.max_gravity

    # Взаимодействие с твердыми объектами
    for block in blocks:
        if block.transform.position.x + block.size.x > player.transform.position.x > block.transform.position.x or block.transform.position.x + block.size.x > player.transform.position.x + player.size.x > block.transform.position.x or block.transform.position.x + block.size.x > player.transform.position.x + player.size.x // 2 > block.transform.position.x:
            if block.transform.position.y + block.size.y > player.transform.position.y + player.size.y > block.transform.position.y:
                if not player.isJumping:
                    player.isGrounding = True
                player.transform.position.y = block.transform.position.y - player.size.y
            elif block.transform.position.y + block.size.y > player.transform.position.y > block.transform.position.y:
                if not player.isGrounding and not player.isJumping:
                    player.transform.position.y = block.transform.position.y + block.size.y
                    player.transform.direction.y = 0

    # Взаимодействие с твердыми объектами на оси OX на отдельном цикле (Необходимо для правильного расчета
    # Расчитывать физику по оси OX необходимо после )
    for block in blocks:
        if block.transform.position.y + block.size.y > player.transform.position.y > block.transform.position.y or block.transform.position.y + block.size.y > player.transform.position.y + player.size.y - 2 > block.transform.position.y or block.transform.position.y + block.size.y > player.transform.position.y + player.size.y // 2 > block.transform.position.y or block.transform.position.y + block.size.y > player.transform.position.y + player.size.y // 4 > block.transform.position.y or block.transform.position.y + block.size.y > player.transform.position.y + player.size.y // 4 * 3 > block.transform.position.y:
            if block.transform.position.x + block.size.x > player.transform.position.x > block.transform.position.x:
                player.transform.position.x = block.transform.position.x + block.size.x
            elif block.transform.position.x + block.size.x > player.transform.position.x + player.size.x > block.transform.position.x:
                player.transform.position.x = block.transform.position.x - player.size.x
        elif player.isGrounding:
            if block.transform.position.y + block.size.y >= player.transform.position.y > block.transform.position.y:
                if block.transform.position.x + block.size.x > player.transform.position.x > block.transform.position.x:
                    player.transform.position.x = block.transform.position.x + block.size.x
                elif block.transform.position.x + block.size.x > player.transform.position.x + player.size.x > block.transform.position.x:
                    player.transform.position.x = block.transform.position.x - player.size.x

    # Взаимодействие с ягодой
    for fruit in fruits:
        if fruit.transform.position.x < player.transform.position.x < fruit.transform.position.x + fruit.size.x or fruit.transform.position.x < player.transform.position.x + player.size.x < fruit.transform.position.x + fruit.size.x or fruit.transform.position.x < player.transform.position.x + player.size.x // 2 < fruit.transform.position.x + fruit.size.x:
            if fruit.transform.position.y < player.transform.position.y < fruit.transform.position.y + fruit.size.y or fruit.transform.position.y < player.transform.position.y + player.size.y - 2 < fruit.transform.position.y + fruit.size.y or fruit.transform.position.y < player.transform.position.y + player.size.y // 4 < fruit.transform.position.y + fruit.size.y or fruit.transform.position.y < player.transform.position.y + player.size.y // 2 < fruit.transform.position.y + fruit.size.y or fruit.transform.position.y < player.transform.position.y + player.size.y // 4 * 3 < fruit.transform.position.y + fruit.size.y:
                if pygame.mixer.get_busy():
                    chanel2.stop()
                chanel2 = fruit.sound_pickup.play()
                player.health += 1
                fruits.remove(fruit)

    # Изменение состояния игрока
    if player.isGrounding and player.state == "jump":
        player.state = "idle"

    pygame.draw.rect(window, (0, 0, 0), (graph_width // 2 - player.size.x // 2 - player.transform.position.x, graph_height // 2 - player.size.y // 2 - player.transform.position.y, (world_x + 1) * world_size + s, (world_y + 1) * world_size + w), 1)

    if debug:
        for block in blocks:
            pygame.draw.rect(window, (0, 0, 0), (graph_width // 2 - player.size.x // 2 + block.transform.position.x - player.transform.position.x, graph_height // 2 - player.size.y // 2 + block.transform.position.y - player.transform.position.y, block.size.x, block.size.y), 1)

        for fruit in fruits:
            pygame.draw.rect(window, (255, 255, 0), (graph_width // 2 - player.size.x // 2 + fruit.transform.position.x - player.transform.position.x, graph_height // 2 - player.size.y // 2 + fruit.transform.position.y - player.transform.position.y, fruit.size.x, fruit.size.y), 0)

        pygame.draw.rect(window, (255, 0, 0), (graph_width // 2 - player.size.x // 2, graph_height // 2 - player.size.y // 2, player.size.x, player.size.y), 0)

        info_player_position = font_debug.render("player_pos ({}, {})".format(player.transform.position.x, player.transform.position.y), True, (0, 0, 0))
        info_player_direction = font_debug.render("player_dir ({}, {})".format(player.transform.direction.x, player.transform.direction.y), True, (0, 0, 0))
        info_player_isJumping = font_debug.render("player_isJumping is {}".format(player.isJumping), True, (0, 0, 0))
        info_player_isWalking = font_debug.render("player_isWalking is {}".format(player.isWalking), True, (0, 0, 0))
        info_player_isGrounding = font_debug.render("player_isGrounding is {}".format(player.isGrounding), True, (0, 0, 0))

        window.blit(info_player_position, (128, 0))
        window.blit(info_player_direction, (128, 12 * 2))
        window.blit(info_player_isJumping, (128, 12 * 3))
        window.blit(info_player_isWalking, (128, 12 * 4))
        window.blit(info_player_isGrounding, (128, 12 * 5))

        pygame.draw.line(window, (0, 255, 0), (0, graph_height // 2), (graph_width, graph_height // 2), 1)
        pygame.draw.line(window, (0, 255, 0), (graph_width // 2, 0), (graph_width // 2, graph_height), 1)
    else:
        for block in blocks:
            block.render()

        for fruit in fruits:
            fruit.render()

        player.render()

    pygame.display.flip()
    window.fill((255 - 32, 255 - 32, 255))
    clock.tick(90)
