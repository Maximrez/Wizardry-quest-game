# Creator: Reznik Maxim
# Version: 2.0

import pygame, random, time


class Player(pygame.sprite.Sprite):
    def __init__(self, healths, firelevel, waterlevel, lightlevel):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = self.images[1]
        self.rect = self.image.get_rect(center=(32, 527))
        self.rect = self.rect.clamp(screenrect)
        self.reloadwaterball = 0
        self.reloadcloud = 0
        self.reloadfireball = 0
        self.healths = healths
        self.firelevel = firelevel
        self.waterlevel = waterlevel
        self.lightlevel = lightlevel
        self.cdupgrade = 0
        self.unkillable = 0
        self.reloadshield = 0
        self.reloadrainbow = 0

    def move(self, direction):
        for q in range(6):
            go = True
            for block in list(blocks):
                if direction > 0 and ((self.rect.top < block.posy + 16 < self.rect.bottom) or (
                        self.rect.top < block.posy < self.rect.bottom)) and block.rect.left - 1 == self.rect.right:
                    go = False
                    break
                elif direction < 0 and ((self.rect.top < block.posy + 16 < self.rect.bottom) or (
                        self.rect.top < block.posy < self.rect.bottom)) and block.rect.right + 1 == self.rect.left:
                    go = False
                    break
            if go == False:
                break
            self.rect.move_ip(direction, 0)
        self.rect = self.rect.clamp(screenrect)
        if direction < 0:
            self.image = self.images[0]
        elif direction > 0:
            self.image = self.images[1]
        for q in range(7):
            stand = False
            for block in list(blocks):
                if block.posy == self.rect.bottom and ((self.rect.left < block.posx < self.rect.right) or (
                        self.rect.left < block.posx + 40 < self.rect.right)):
                    stand = True
                    break
            if stand == False:
                self.rect.move_ip(0, 1)
        if self.rect.bottom >= screenrect.bottom - 4:
            self.kill()

    def fly(self, descent):
        self.rect.move_ip(0, -5)
        for q in range(5 + self.lightlevel - 1):
            go = True
            for block in list(blocks):
                if descent > 0 and block.posy == self.rect.bottom and (
                        (self.rect.left < block.posx < self.rect.right) or (
                        self.rect.left < block.posx + 40 < self.rect.right)):
                    go = False
                    break
                if descent < 0 and ((self.rect.left < block.posx < self.rect.right) or (
                        self.rect.left < block.posx + 40 < self.rect.right)) \
                        and self.rect.top < block.posy + 18 < self.rect.bottom:
                    go = False
                    break
            if go == False:
                break
            self.rect.move_ip(0, descent)
        self.rect = self.rect.clamp(screenrect)

    def cast(self, sphere1, sphere2, sphere3):
        s1 = int(sphere1.imgback())
        s2 = int(sphere2.imgback())
        s3 = int(sphere3.imgback())
        combo = [s1, s2, s3]
        if sorted(combo) == [1, 1, 1] and self.reloadwaterball == 0:
            if self.image == self.images[0]:
                Waterball(1, self)
            else:
                Waterball(0, self)
            self.reloadwaterball = 65
        elif sorted(combo) == [2, 2, 2] and self.reloadcloud == 0:
            Cloud(110 + (self.lightlevel - 1) * 10, self)
            self.reloadcloud = 170
        elif sorted(combo) == [0, 0, 0] and self.reloadfireball == 0:
            if self.image == self.images[0]:
                Fireball(self, -12 + (self.firelevel - 1) * -2, 0, 'npss', self)
            else:
                Fireball(self, 12 + (self.firelevel - 1) * 2, 0, 'npss', self)
            self.reloadfireball = 50
        elif sorted(combo) == [1, 1, 2] and self.reloadshield == 0:
            Shield(50 + int((self.lightlevel + self.waterlevel) / 2) * 5, self)
            self.unkillable = 60 + int((self.lightlevel + self.waterlevel) / 2) * 5
            self.reloadshield = 140
        elif sorted(combo) == [0, 1, 2] and self.reloadrainbow == 0:
            Rainbow(60, self, 0)
            self.reloadrainbow = 100

    def health(self, change):
        if change < 0 and self.unkillable == 0:
            self.healths -= 1
            if self.healths <= 0:
                self.kill()
            Shield(15, self)
            self.unkillable = 15
        elif change > 0 and self.healths < 3:
            self.healths += 1


class Block(pygame.sprite.Sprite):
    def __init__(self, posx, posy):
        self.posx = posx
        self.posy = posy
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.rect = self.image.get_rect()
        self.rect.move_ip(self.posx, self.posy)


class Sphere(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = self.images[0]
        self.rect = self.image.get_rect(midbottom=(0, screenrect.bottom))
        self.rect.move_ip(pos)

    def change(self, num):
        self.image = self.images[num]

    def imgback(self):
        for q in range(3):
            if self.image == self.images[q]:
                return q


class Waterball(pygame.sprite.Sprite):
    def __init__(self, side, player):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.player = player
        self.image = self.images[side]
        if side == 0:
            self.rect = self.image.get_rect(midleft=self.player.rect.midright)
        else:
            self.rect = self.image.get_rect(midright=self.player.rect.midleft)
        self.side = side
        self.time = 50

    def update(self):
        for q in range(8 + (self.player.waterlevel - 1) * 2):
            go = True
            for block in list(blocks):
                if self.side == 0 and ((self.rect.top < block.posy + 16 < self.rect.bottom) or (
                        self.rect.top < block.posy < self.rect.bottom)) and block.rect.left - 1 == self.rect.right:
                    go = False
                    self.side = 1
                    self.image = self.images[1]
                    break
                elif self.side == 1 and ((self.rect.top < block.posy + 16 < self.rect.bottom) or (
                        self.rect.top < block.posy < self.rect.bottom)) and block.rect.right + 1 == self.rect.left:
                    go = False
                    self.side = 0
                    self.image = self.images[0]
                    break
            for nps in list(npss):
                if self.side == 0 and ((nps.rect.top <= self.rect.top + 16 <= nps.rect.bottom) or (
                        nps.rect.top <= self.rect.bottom <= nps.rect.bottom)) and nps.rect.left - 1 == self.rect.right:
                    nps.health(-self.player.waterlevel * 0.5)
                    go = False
                    self.side = 1
                    self.image = self.images[1]
                    break
                elif self.side == 1 and ((nps.rect.top <= self.rect.top + 16 <= nps.rect.bottom) or (
                        nps.rect.top <= self.rect.bottom <= nps.rect.bottom)) and nps.rect.right + 1 == self.rect.left:
                    nps.health(-self.player.waterlevel * 0.5)
                    go = False
                    self.side = 0
                    self.image = self.images[0]
                    break
            if self.side == 0 and self.rect.right >= screenrect.right:
                self.side = 1
                self.image = self.images[1]
            elif self.side == 1 and self.rect.left <= screenrect.left:
                self.side = 0
                self.image = self.images[0]
            if go == False:
                break
            if self.side == 0:
                self.rect.move_ip(1, 0)
            else:
                self.rect.move_ip(-1, 0)
        self.rect = self.rect.clamp(screenrect)
        self.time -= 1
        if self.time == 0:
            self.player.rect.move_ip(self.rect.centerx - self.player.rect.centerx,
                                     self.rect.centery - self.player.rect.centery)
            self.kill()


class Cloud(pygame.sprite.Sprite):
    def __init__(self, time, player):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.player = player
        self.rect = self.image.get_rect(midtop=(self.player.rect.midbottom[0], self.player.rect.midbottom[1] - 10))
        self.time = time

    def update(self):
        self.time -= 1
        descent = pygame.key.get_pressed()[pygame.K_DOWN] - pygame.key.get_pressed()[pygame.K_UP]
        self.player.fly(descent)
        if self.time == 0:
            self.kill()
        else:
            Cloud(self.time, self.player)
            self.kill()


class BadWizard(pygame.sprite.Sprite):
    def __init__(self, pos, side, player):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.player = player
        self.image = self.images[side]
        self.rect = self.image.get_rect(center=pos)
        self.reload = 120
        self.healths = 4
        if self.player != None:
            Healthbar(self, self.healths)

    def update(self):
        if self.reload > 0:
            self.reload -= 1
        else:
            koeff = ((self.player.rect.centerx - self.rect.centerx) ** 2 + (
                    self.player.rect.centery - self.rect.centery) ** 2) ** 0.5 / 8
            if koeff == 0:
                self.player.health(-1)
            else:
                Fireball(self, int((self.player.rect.centerx - self.rect.centerx) / koeff),
                         int((self.player.rect.centery - self.rect.centery) / koeff), 'player', self.player)
            self.reload = 120

    def health(self, change):
        self.healths += change
        if self.healths <= 0:
            if random.randint(1, 100) <= 70:
                if random.randint(1, 100) <= 60:
                    Tomeofknoledge(self.rect.center, self.player)
                else:
                    Healheart(self.rect.center, self.player)
            self.kill()


class Fireball(pygame.sprite.Sprite):
    def __init__(self, hero, directionx, directiony, victim, player):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.player = player
        self.rect = self.image.get_rect(center=hero.rect.center)
        self.directionx = directionx
        self.directiony = directiony
        self.victim = victim

    def update(self):
        self.rect.move_ip(self.directionx, self.directiony)
        if self.victim == 'player':
            if self.rect.colliderect(self.player):
                self.player.health(-1)
                self.kill()
        else:
            for nps in list(npss):
                if (
                        self.rect.left <= nps.rect.left <= self.rect.right or self.rect.left <= nps.rect.right <= self.rect.right) \
                        and (
                        nps.rect.top <= self.rect.top <= nps.rect.bottom or nps.rect.top <= self.rect.bottom <= nps.rect.bottom):
                    nps.health(-self.player.firelevel)
                    self.kill()
                    break


class Miniskeleton(pygame.sprite.Sprite):
    def __init__(self, pos, side, player):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = self.images[side]
        self.rect = self.image.get_rect(center=pos)
        if side == 1:
            self.speedx = 1
        else:
            self.speedx = -1
        self.speedy = 1
        self.player = player
        self.healths = 2
        if self.player != None:
            Healthbar(self, self.healths)

    def update(self):
        for q in range(4):
            go = True
            for block in list(blocks):
                if self.speedx > 0 and ((((self.rect.top <= block.posy + 16 <= self.rect.bottom) or (
                        self.rect.top <= block.posy <= self.rect.bottom)) \
                                         and block.rect.left - 1 == self.rect.right) or screenrect.right == self.rect.right):
                    go = False
                    break
                elif self.speedx < 0 and ((((self.rect.top <= block.posy + 16 <= self.rect.bottom) or (
                        self.rect.top <= block.posy <= self.rect.bottom)) \
                                           and block.rect.right + 1 == self.rect.left) or screenrect.left == self.rect.left):
                    go = False
                    break
            if go == False:
                self.speedx = -self.speedx
                break
            self.rect.move_ip(self.speedx, 0)
        for q in range(4):
            go = True
            for block in list(blocks):
                if self.speedy > 0 and ((((self.rect.left <= block.posx + 40 <= self.rect.right) or (
                        self.rect.left <= block.posx <= self.rect.right))
                                         and block.rect.top - 1 == self.rect.bottom) or screenrect.bottom == self.rect.bottom):
                    go = False
                    break
                elif self.speedy < 0 and ((((self.rect.left <= block.posx + 40 <= self.rect.right) or (
                        self.rect.left <= block.posx <= self.rect.right))
                                           and block.rect.bottom + 1 == self.rect.top) or screenrect.top == self.rect.top):
                    go = False
                    break
            if go == False:
                self.speedy = -self.speedy
                break
            self.rect.move_ip(0, self.speedy)
        if self.rect.colliderect(self.player):
            self.player.health(-1)
            self.speedy = -self.speedy
            self.speedx = -self.speedx
        if self.speedx > 0:
            self.image = self.images[1]
        else:
            self.image = self.images[0]

    def health(self, change):
        self.healths += change
        if self.healths <= 0:
            if random.randint(1, 100) <= 70:
                if random.randint(1, 100) <= 60:
                    Tomeofknoledge(self.rect.center, self.player)
                else:
                    Healheart(self.rect.center, self.player)
            self.kill()


class Heart(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.rect = self.image.get_rect(center=pos)


class Upgradesphere(pygame.sprite.Sprite):
    def __init__(self, pos, num):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = self.images[num]
        self.rect = self.image.get_rect()
        self.rect.move_ip(pos)


class Healheart(pygame.sprite.Sprite):
    def __init__(self, pos, player):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.rect = self.image.get_rect(center=pos)
        self.player = player

    def update(self):
        for q in range(7):
            stand = False
            for block in list(blocks):
                if self.rect.colliderect(block):
                    stand = True
                    break
            if stand == False:
                self.rect.move_ip(0, 1)
        if self.rect.colliderect(self.player):
            self.player.health(1)
            self.kill()


class Tomeofknoledge(pygame.sprite.Sprite):
    def __init__(self, pos, player):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.rect = self.image.get_rect(center=pos)
        self.player = player

    def update(self):
        for q in range(8):
            stand = False
            for block in list(blocks):
                if self.rect.colliderect(block):
                    stand = True
                    break
            if stand == False:
                self.rect.move_ip(0, 1)
            if self.rect.colliderect(self.player) and self.player.cdupgrade == 0:
                if self.player.firelevel < 5 or self.player.waterlevel < 5 or self.player.lightlevel < 5:
                    self.player.cdupgrade = 10
                    upgrade(self.player)
                self.kill()


class Skeletonboss(pygame.sprite.Sprite):
    def __init__(self, player):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = self.images[1]
        self.rect = self.image.get_rect(center=(540, 335))
        self.player = player
        self.healths = 40
        self.cdspawn = 100
        Healthbar(self, self.healths)

    def update(self):
        if self.cdspawn > 0:
            self.cdspawn -= 1
        if self.cdspawn == 0:
            Miniskeleton(self.rect.center, random.randint(0, 1), self.player)
            self.cdspawn = 100
        koeff = ((self.player.rect.centerx - self.rect.centerx) ** 2 + (
                self.player.rect.centery - self.rect.centery) ** 2) ** 0.5 / 2
        if koeff != 0:
            directionx = int((self.player.rect.centerx - self.rect.centerx) / koeff)
            directiony = int((self.player.rect.centery - self.rect.centery) / koeff)
            self.rect.move_ip(directionx, directiony)
            if directionx > 0:
                self.image = self.images[0]
            else:
                self.image = self.images[1]

    def health(self, change):
        self.healths += change
        if self.healths <= 0:
            for nps in list(npss):
                nps.kill()
            self.kill()


class Healthbar(pygame.sprite.Sprite):
    def __init__(self, nps, maximum):
        pygame.sprite.Sprite.__init__(self, self.containers)
        if nps.healths <= 0:
            length = 0
        else:
            length = nps.healths
        self.image = pygame.transform.scale(self.image, (int(nps.rect.width * length / maximum), 10))
        self.rect = self.image.get_rect(midbottom=nps.rect.midtop)
        self.nps = nps
        self.maximum = maximum

    def update(self):
        if self.nps.alive():
            Healthbar(self.nps, self.maximum)
        self.kill()


class Shield(pygame.sprite.Sprite):
    def __init__(self, time, player):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.player = player
        self.rect = self.image.get_rect(center=(self.player.rect.centerx, self.player.rect.centery + 15))
        self.time = time

    def update(self):
        self.time -= 1
        if self.time == 0:
            self.kill()
        else:
            Shield(self.time, self.player)
            self.kill()


class Rainbow(pygame.sprite.Sprite):
    def __init__(self, time, player, cd):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.player = player
        self.rect = self.image.get_rect(center=self.player.rect.center)
        self.time = time
        self.cddamage = cd

    def update(self):
        if self.cddamage > 0:
            self.cddamage -= 1
        if self.cddamage == 0:
            for nps in list(npss):
                if self.rect.colliderect(nps):
                    nps.health(-int((self.player.firelevel + self.player.waterlevel + self.player.lightlevel) / 3))
                    self.cddamage = 20
        self.time -= 1
        if self.time == 0:
            self.kill()
        else:
            Rainbow(self.time, self.player, self.cddamage)
            self.kill()


screenrect = pygame.Rect(0, 0, 1080, 731)  # 1080, 731
pygame.init()
screen = pygame.display.set_mode(screenrect.size, pygame.FULLSCREEN)
pygame.display.set_caption('Wizardry Quest Game')
background = pygame.transform.scale(pygame.image.load("images/background.png"), screenrect.size)
screen.blit(background, (0, 0))

Player.images = [
    pygame.transform.flip(pygame.transform.scale(pygame.image.load("images/wizard.png").convert_alpha(), (63, 100)), 1,
                          0), pygame.transform.scale(pygame.image.load("images/wizard.png").convert_alpha(), (63, 100))]
Block.image = pygame.transform.scale(pygame.image.load("images/block.png").convert_alpha(), (40, 17))
Sphere.images = [pygame.transform.scale(pygame.image.load("images/fire.png").convert_alpha(), (50, 50)),
                 pygame.transform.scale(pygame.image.load("images/water.png").convert_alpha(), (50, 50)),
                 pygame.transform.scale(pygame.image.load("images/lightning.png").convert_alpha(), (50, 50))]
Waterball.images = [pygame.transform.scale(pygame.image.load("images/waterball.png").convert_alpha(), (48, 38)),
                    pygame.transform.flip(
                        pygame.transform.scale(pygame.image.load("images/waterball.png").convert_alpha(), (48, 38)), 1,
                        0)]
Cloud.image = pygame.transform.scale(pygame.image.load("images/cloud.png").convert_alpha(), (50, 30))
BadWizard.images = [pygame.transform.scale(pygame.image.load("images/badwizard.png").convert_alpha(), (50, 100)),
                    pygame.transform.scale(
                        pygame.transform.flip(pygame.image.load("images/badwizard.png").convert_alpha(), 1, 0),
                        (50, 100))]
Fireball.image = pygame.transform.scale(pygame.image.load("images/fireball.png").convert_alpha(), (45, 45))
Miniskeleton.images = [pygame.transform.scale(pygame.image.load("images/miniskeleton.png").convert_alpha(), (40, 50)),
                       pygame.transform.flip(
                           pygame.transform.scale(pygame.image.load("images/miniskeleton.png").convert_alpha(),
                                                  (40, 50)), 1, 0)]
Heart.image = pygame.transform.scale(pygame.image.load("images/heart.png").convert_alpha(), (40, 40))
Upgradesphere.images = [pygame.transform.scale(pygame.image.load("images/fireup.png"), (100, 100)),
                        pygame.transform.scale(pygame.image.load("images/waterup.png"), (100, 100)),
                        pygame.transform.scale(pygame.image.load("images/lightningup.png"), (100, 100))]
Healheart.image = pygame.transform.scale(pygame.image.load("images/heart.png").convert_alpha(), (50, 50))
Tomeofknoledge.image = pygame.transform.scale(pygame.image.load("images/tomeofknoledge.gif").convert_alpha(), (50, 50))
Skeletonboss.images = [pygame.transform.scale(pygame.image.load("images/skeletonboss.png").convert_alpha(), (200, 250)),
                       pygame.transform.flip(
                           pygame.transform.scale(pygame.image.load("images/skeletonboss.png").convert_alpha(),
                                                  (200, 250)), 1, 0)]
Healthbar.image = pygame.transform.scale(pygame.image.load("images/redline.png").convert_alpha(), (50, 50))
Shield.image = pygame.transform.scale(pygame.image.load("images/shield.png").convert_alpha(), (50, 50))
Rainbow.image = pygame.transform.scale(pygame.image.load("images/rainbow.png").convert_alpha(), (135, 230))

second = pygame.sprite.RenderUpdates()
mainall = pygame.sprite.RenderUpdates()
blocks = pygame.sprite.Group()
npss = pygame.sprite.Group()
momental = pygame.sprite.Group()
upgrades = pygame.sprite.RenderUpdates()
editupdate = pygame.sprite.RenderUpdates()
items = pygame.sprite.Group()
healthbars = pygame.sprite.Group()

Player.containers = mainall, editupdate
Block.containers = blocks, second, editupdate
Sphere.containers = mainall, editupdate
Waterball.containers = mainall
Cloud.containers = mainall
Shield.containers = mainall
BadWizard.containers = npss, second, editupdate
Fireball.containers = mainall, editupdate
Miniskeleton.containers = second, npss, editupdate
Heart.containers = mainall, momental
Upgradesphere.containers = upgrades
Healheart.containers = mainall, items
Tomeofknoledge.containers = mainall, items
Skeletonboss.containers = second, npss
Healthbar.containers = mainall
Rainbow.containers = mainall


def rules():
    background = pygame.transform.scale(pygame.image.load("images/background.png"), screenrect.size)
    screen.blit(background, (0, 0))
    pygame.display.flip()
    introText = ["Правила игры:", "",
                 "Ваш герой - маг, попавший в подземелье. Вы можете передвигать его,",
                 "нажимая на <- и ->, следите за тем, чтобы маг не упал! Клавиша Q ",
                 "создаёт сферу огня, W - сферу воды, E - сферу молнии. Три последнии",
                 "наколдованные Вами сферы отображены в левом нижнем углу экрана.",
                 "При нажатии на SPACE маг будет колдовать способность,",
                 "комбинируемую отображаемыми сферами. На каждом уровне игры будут",
                 "находиться монстры, которых Вы должны убить для перехода на",
                 "следующий уровень (над ними отображено колличество их жизней). Они",
                 "также могут убить Вас (следите за своим колличество жизней в правом",
                 "верхнем углу экрана). Удачи!"]
    font = pygame.font.Font(None, 40)
    textCoord = 15
    for line in introText:
        stringRendered = font.render(line, 1, pygame.Color('grey'))
        introRect = stringRendered.get_rect()
        textCoord += 10
        introRect.top = textCoord
        introRect.x = 15
        textCoord += introRect.height
        screen.blit(stringRendered, introRect)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if pygame.key.get_pressed()[pygame.K_ESCAPE]:
                screen.blit(background, (0, 0))
                pygame.display.flip()
                running = False
                time.sleep(0.5)
                menu()
        pygame.display.flip()
        pygame.time.Clock().tick(40)


def levelediting():
    spisok = ['Block(0, 578)', 'Block(40, 578)']
    Player(3, 5, 5, 5)
    Sphere((45, -20))
    Sphere((115, -20))
    Sphere((185, -20))
    Block(0, 578)
    Block(40, 578)
    backspacecd = 0
    edit = None
    numedit = None
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif pygame.key.get_pressed()[pygame.K_ESCAPE]:
                spisok = []
                screen.blit(background, (0, 0))
                pygame.display.flip()
                running = False
                for obj in list(second):
                    obj.kill()
                for obj in list(mainall):
                    obj.kill()
                time.sleep(0.5)
                menu()
            elif pygame.key.get_pressed()[pygame.K_1] and edit == None:
                edit = Block(pygame.mouse.get_pos()[0] // 40 * 40, pygame.mouse.get_pos()[1] // 17 * 17)
                numedit = 1
            elif pygame.key.get_pressed()[pygame.K_2] and edit == None:
                edit = BadWizard((pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1] // 17 * 17 + 1), 0, None)
                numedit = 2
            elif pygame.key.get_pressed()[pygame.K_3] and edit == None:
                edit = BadWizard((pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1] // 17 * 17 + 1), 1, None)
                numedit = 3
            elif pygame.key.get_pressed()[pygame.K_4] and edit == None:
                edit = Miniskeleton((pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]), 0, None)
                numedit = 4
            elif pygame.key.get_pressed()[pygame.K_5] and edit == None:
                edit = Miniskeleton((pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]), 1, None)
                numedit = 5
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and edit != None:
                if numedit == 1:
                    spisok.append('Block(' + str(edit.rect.left) + ', ' + str(edit.rect.top) + ')')
                elif numedit == 2:
                    spisok.append('BadWizard((' + str(edit.rect.centerx) + ', ' + str(
                        edit.rect.centery) + '), ' + '0' + ', ' + 'player' + ')')
                elif numedit == 3:
                    spisok.append('BadWizard((' + str(edit.rect.centerx) + ', ' + str(
                        edit.rect.centery) + '), ' + '1' + ', ' + 'player' + ')')
                elif numedit == 4:
                    spisok.append('Miniskeleton((' + str(edit.rect.centerx) + ', ' + str(
                        edit.rect.centery) + '), ' + '0' + ', ' + 'player' + ')')
                elif numedit == 5:
                    spisok.append('Miniskeleton((' + str(edit.rect.centerx) + ', ' + str(
                        edit.rect.centery) + '), ' + '1' + ', ' + 'player' + ')')
                edit = None
            elif pygame.key.get_pressed()[pygame.K_BACKSPACE] and edit == None and backspacecd == 0 and len(spisok) > 2:
                spisok.pop(-1)
                list(editupdate)[-1].kill()
                backspacecd = 3
            elif pygame.key.get_pressed()[pygame.K_SPACE]:
                fin = open('newlevel.txt', 'w')
                fin.write(('\n').join(spisok))
                fin.close()
                print('level saved to "nextlevel.txt"')
        if edit != None:
            if numedit == 1:
                edit.rect.move_ip(pygame.mouse.get_pos()[0] // 40 * 40 - edit.rect.left,
                                  pygame.mouse.get_pos()[1] // 17 * 17 - edit.rect.top)
            elif numedit == 2 or numedit == 3:
                edit.rect.move_ip(pygame.mouse.get_pos()[0] - edit.rect.centerx,
                                  pygame.mouse.get_pos()[1] // 17 * 17 + 1 - edit.rect.centery)
            elif numedit == 4 or numedit == 5:
                edit.rect.move_ip(pygame.mouse.get_pos()[0] - edit.rect.centerx,
                                  pygame.mouse.get_pos()[1] - edit.rect.centery)
        if backspacecd > 0:
            backspacecd -= 1
        editupdate.clear(screen, background)
        pygame.display.update(editupdate.draw(screen))
        pygame.time.Clock().tick(30)


def terminate():
    pygame.quit()
    exit(0)


def pause():
    running = True
    pygame.draw.rect(screen, (255, 255, 255), (550, 300, 40, 130))
    pygame.draw.rect(screen, (255, 255, 255), (490, 300, 40, 130))
    pygame.display.flip()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN and pygame.key.get_pressed()[pygame.K_p]:
                running = False
            elif pygame.key.get_pressed()[pygame.K_ESCAPE]:
                screen.blit(background, (0, 0))
                pygame.display.flip()
                running = False
                for obj in list(second):
                    obj.kill()
                for obj in list(mainall):
                    obj.kill()
                pygame.mouse.set_visible(1)
                time.sleep(0.5)
                menu()


def upgrade(player):
    pygame.mouse.set_visible(1)
    screen.blit(background, (0, 0))
    running = True
    uf = Upgradesphere((340, 315), 0)
    uw = Upgradesphere((490, 315), 1)
    ul = Upgradesphere((640, 315), 2)
    pygame.display.flip()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif pygame.key.get_pressed()[pygame.K_ESCAPE]:
                screen.blit(background, (0, 0))
                pygame.display.flip()
                running = False
                for obj in list(second):
                    obj.kill()
                for obj in list(mainall):
                    obj.kill()
                pygame.mouse.set_visible(1)
                time.sleep(0.5)
                menu()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if uf.rect.collidepoint(event.pos) and player.firelevel < 5:
                    player.firelevel += 1
                    running = False
                elif uw.rect.collidepoint(event.pos) and player.waterlevel < 5:
                    player.waterlevel += 1
                    running = False
                elif ul.rect.collidepoint(event.pos) and player.lightlevel < 5:
                    player.lightlevel += 1
                    running = False
        upgrades.update()
        pygame.display.update(upgrades.draw(screen))
    for up in list(upgrades):
        up.kill()
    screen.blit(background, (0, 0))
    pygame.display.flip()
    pygame.mouse.set_visible(0)


def image(imagetext):
    running = 300
    while running > 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if pygame.key.get_pressed()[pygame.K_ESCAPE]:
                screen.blit(background, (0, 0))
                pygame.display.flip()
                running = False
                for obj in list(second):
                    obj.kill()
                for obj in list(mainall):
                    obj.kill()
                pygame.mouse.set_visible(1)
                time.sleep(0.5)
                menu()
        screen.fill((0, 0, 0))
        font = pygame.font.Font(None, 50)
        text = font.render("" + str(imagetext), 1, (100, 255, 100))
        text_x = screenrect.size[0] // 2 - text.get_width() // 2
        text_y = screenrect.size[1] // 2 - text.get_height() // 2
        text_w = text.get_width()
        text_h = text.get_height()
        screen.blit(text, (text_x, text_y))
        pygame.draw.rect(screen, (0, 255, 0), (text_x - 10, text_y - 10, text_w + 20, text_h + 20), 1)
        running -= 1
        pygame.display.flip()
    screen.blit(background, (0, 0))
    pygame.display.flip()


def level(functions, playerh, firelevel, waterlevel, lightlevel):
    pygame.mouse.set_visible(0)
    player = Player(playerh, firelevel, waterlevel, lightlevel)
    sphere1 = Sphere((45, -20))
    sphere2 = Sphere((115, -20))
    sphere3 = Sphere((185, -20))
    timeforpause = 0
    fpssphere = 0
    for func in functions:
        eval(func)
    while player.alive():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if pygame.key.get_pressed()[pygame.K_ESCAPE]:
                screen.blit(background, (0, 0))
                pygame.display.flip()
                for obj in list(second):
                    obj.kill()
                for obj in list(mainall):
                    obj.kill()
                pygame.mouse.set_visible(1)
                time.sleep(0.5)
                menu()
            if pygame.key.get_pressed()[pygame.K_p] and timeforpause == 0:
                pause()
                screen.blit(background, (0, 0))
                pygame.display.flip()
                timeforpause = 30
            if pygame.key.get_pressed()[pygame.K_q] and fpssphere == 0:
                sphere1.change(sphere2.imgback())
                sphere2.change(sphere3.imgback())
                sphere3.change(0)
                fpssphere = 2
            if pygame.key.get_pressed()[pygame.K_w] and fpssphere == 0:
                sphere1.change(sphere2.imgback())
                sphere2.change(sphere3.imgback())
                sphere3.change(1)
                fpssphere = 2
            if pygame.key.get_pressed()[pygame.K_e] and fpssphere == 0:
                sphere1.change(sphere2.imgback())
                sphere2.change(sphere3.imgback())
                sphere3.change(2)
                fpssphere = 2
            if pygame.key.get_pressed()[pygame.K_SPACE]:
                player.cast(sphere1, sphere2, sphere3)
            if pygame.key.get_pressed()[pygame.K_g]:
                Tomeofknoledge((540, 250), player)
            if pygame.key.get_pressed()[pygame.K_t]:
                Healheart((540, 250), player)
        if player.reloadwaterball > 0:
            player.reloadwaterball -= 1
        if player.reloadcloud > 0:
            player.reloadcloud -= 1
        if player.reloadfireball > 0:
            player.reloadfireball -= 1
        if timeforpause > 0:
            timeforpause -= 1
        if player.cdupgrade > 0:
            player.cdupgrade -= 1
        if player.reloadshield > 0:
            player.reloadshield -= 1
        if player.reloadrainbow > 0:
            player.reloadrainbow -= 1
        if player.unkillable > 0:
            player.unkillable -= 1
        if fpssphere > 0:
            fpssphere -= 1
        for moment in list(momental):
            moment.kill()
        for q in range(player.healths):
            Heart((30 + q * 40, 30))
        direction = pygame.key.get_pressed()[pygame.K_RIGHT] - pygame.key.get_pressed()[pygame.K_LEFT]
        player.move(direction)
        second.clear(screen, background)
        mainall.clear(screen, background)
        second.update()
        mainall.update()
        pygame.display.update(second.draw(screen))
        pygame.display.update(mainall.draw(screen))
        pygame.time.Clock().tick(40)
        for item in list(items):
            if item.rect.centery >= screenrect.bottom - 4:
                item.kill()
        if len(list(npss)) == 0 and len(list(items)) == 0:
            break
    pygame.mouse.set_visible(1)
    second.clear(screen, background)
    mainall.clear(screen, background)
    if player.alive():
        for obj in list(mainall):
            obj.kill()
        for obj in list(second):
            obj.kill()
        return True, player.healths, player.firelevel, player.waterlevel, player.lightlevel
    else:
        for obj in list(second):
            obj.kill()
        for obj in list(mainall):
            obj.kill()
        return False, player.healths, player.firelevel, player.waterlevel, player.lightlevel


def menu():
    class Button():
        def __init__(self, rect, text, function):
            self.rect = pygame.Rect(rect)
            self.text = text
            self.bgcolor = pygame.Color('navy')
            self.font_color = pygame.Color('grey')
            self.font = pygame.font.Font(None, self.rect.height - 4)
            self.rendered_text = None
            self.rendered_rect = None
            self.pressed = False
            self.function = function

        def render(self, surface):
            surface.fill(self.bgcolor, self.rect)
            self.rendered_text = self.font.render(self.text, 1, self.font_color)
            self.rendered_rect = self.rendered_text.get_rect(centerx=self.rect.centerx, centery=self.rect.centery)
            pygame.draw.rect(surface, pygame.Color("grey"), self.rect, 3)
            surface.blit(self.rendered_text, self.rendered_rect)

    class GUI:
        def __init__(self):
            self.elements = []

        def add_element(self, element):
            self.elements.append(element)

        def render(self, surface):
            for element in self.elements:
                render = getattr(element, "render", None)
                if callable(render):
                    element.render(surface)

        def update(self):
            for element in self.elements:
                update = getattr(element, "update", None)
                if callable(update):
                    element.update()

    gui = GUI()
    gui.add_element(Button((350, 170, 440, 70), "Начать игру", 'startgame()'))
    gui.add_element(Button((350, 260, 440, 70), "Создание уровней", 'levelediting()'))
    gui.add_element(Button((350, 350, 440, 70), "Правила", 'rules()'))
    gui.add_element(Button((350, 440, 440, 70), "Выход", 'terminate()'))
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_ESCAPE]:
                terminate()
            for element in gui.elements:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and element.rect.collidepoint(event.pos):
                    element.pressed = True
                    screen.blit(background, (0, 0))
                    pygame.display.flip()
                    eval(element.function)
        gui.render(screen)
        gui.update()
        pygame.display.flip()


def startgame():
    fin = open('levels.txt')
    running = True
    playerh = 3
    firelevel = 1
    waterlevel = 1
    lightlevel = 1
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
        spisok = []
        line = fin.readline().rstrip()
        if line == 'end.':
            fin.close()
            running = False
            image('You win!')
            menu()
        else:
            while line != '*****':
                spisok.append(line)
                line = fin.readline().rstrip()
            result, playerh, firelevel, waterlevel, lightlevel = level(spisok, playerh, firelevel, waterlevel,
                                                                       lightlevel)
            if result:
                pass
            else:
                running = False
                image('Game over...')
                menu()
        pygame.display.flip()


image('Wizardry Quest')
menu()
pygame.quit()
