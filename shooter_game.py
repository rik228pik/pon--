

from pygame import *
from random import randint
font.init()

WIDTH,HEIGHT = 700, 525  
FPS = 60

lost = 0
points = 0

#mixer.init()
#mixer.music.load('space.ogg')
#mixer.music.set_volume(0.0)
#mixer.music.play()


window = display.set_mode((WIDTH, HEIGHT))
display.set_caption("Aboba")

class GameSprite(sprite.Sprite):
    def __init__(self,sprite_image, x, y, width, height):
        super().__init__()
        self.image = transform.scale(image.load(sprite_image), (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.mask = mask.from_surface(self.image)
        self.hp = 1

    def draw(self):
        window.blit(self.image, self.rect)


class Player(GameSprite):
    def update(self):
       
        pressed = key.get_pressed()
        if pressed[K_LEFT] and self.rect.x > 0:
            self.rect.x -= 3
        if pressed[K_RIGHT] and self.rect.x < WIDTH - 70:            
            self.rect.x += 3

        if pressed[K_UP] and self.rect.y > 0:            
            self.rect.y -= 3

        if pressed[K_DOWN] and self.rect.y < HEIGHT - 70:            
            self.rect.y += 3

    def fire(self):
        """Постріл кулею"""
        new_bullet = Bullet(self.rect.centerx, self.rect.y)
        bullets.add(new_bullet)


class Asteroid(GameSprite):
    def __init__(self, x, y, speed):
        super().__init__("pngegg копія.png", x, y, 60, 60)
        self.speed = speed

    def update(self):
        """рух астероїда"""
        self.rect.y += self.speed
        if self.rect.y > HEIGHT:
            self.rect.x = randint(0, WIDTH -80)
            self.rect.y = randint(-500, -150)
            self.speed = randint(3,4)
class Bonus(GameSprite):
    def __init__(self, x, y, speed):
        super().__init__("bonus.png", x, y, 50, 50)
        self.speed = speed


    def update(self):
        """рух ворога"""
        
        self.rect.y += self.speed
        if self.rect.y > HEIGHT:
            self.kill()

asteroids = sprite.Group()
for i in range(2):
    new = Asteroid(x=randint(0, WIDTH - 80),
                     y = randint(-500, -150),speed = randint(3,6))
    asteroids.add(new)



class Enemy(GameSprite):
    def __init__(self, x, y, speed):
        super().__init__("alien1.png", x, y, 80, 60)
        self.speed = speed


    def update(self):
        """рух ворога"""
        global lost, lost_text
        self.rect.y += self.speed
        if self.rect.y > HEIGHT:
            lost += 1
            lost_text = font1.render("Пропущено:" + str(lost), True,(255,255,255))
            self.rect.x = randint(0, WIDTH -80)
            self.rect.y = randint(-500, -150)
            self.speed = randint(3,6)


class Bullet(GameSprite):
    def __init__(self, x, y):
        super().__init__("beams2.png", x, y, 30,35)
        self.speed = 4

    def update(self):
        """рух кулі"""
        self.rect.y -= self.speed
        if self.rect.y < -30:
            self.kill()


player = Player("pngegg.png",x=WIDTH/2-50, y=HEIGHT-200, width=100, height =100)
bg = transform.scale(image.load("space.png"), (WIDTH, HEIGHT))
bg2 = transform.scale(image.load("space.png"), (WIDTH, HEIGHT))
bg_y1, bg_y2 = 0,-HEIGHT

bullets = sprite.Group()
monsters = sprite.Group()
bonus = sprite.Group()
for i in range(5):
    new_enemy = Enemy(x=randint(0, WIDTH - 80),
                     y = randint(-500, -150),speed = randint(3,6))
    monsters.add(new_enemy)

font1 = font.SysFont("Arial", 25)
lost_text = font1.render("Пропущено" + str(lost), True,(255,255,255))
points_text = font1.render("Рахунок" + str(points), True,(255,255,255))

font2 = font.SysFont("Arial", 50)
result_text = font2.render("БОТ!",True,(230, 145, 12))
restart_text = font2.render("РЕСТАРТ!",True,(230, 145, 12))
restart_btn = restart_text.get_rect()

run = True
finish = False
clock = time.Clock()

while run:
    for e in event.get():
        if e.type == QUIT:
            run = False

        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                player.fire()

        if e.type == MOUSEBUTTONDOWN and finish:
            x, y = mouse.get_pos()
            restart_btn.x, restart_btn.y = 320, 350
            if restart_btn.collidepoint(x,y):
                finish = False
                lost = 0
                points = 0
                lost_text = font1.render("Пропущено" + str(lost), True,(255,255,255))
                points_text = font1.render("Рахунок" + str(points), True,(255,255,255))

    if not finish:
        window.blit(bg, (0,bg_y1))
        window.blit(bg, (0,bg_y2))
        bg_y1 += 2
        bg_y2 += 2
        if bg_y1 > HEIGHT:
            bg_y1 = -HEIGHT
        if bg_y2 > HEIGHT:
            bg_y2  = -HEIGHT
        player.draw()
        player.update()
        monsters.draw(window)
        monsters.update()
        bullets.draw(window)
        bullets.update()
        asteroids.draw(window)
        asteroids.update()
        bonus.draw(window)
        bonus.update()
        window.blit(lost_text, (20,20))
        window.blit(points_text, (20,50))

        sprite_list = sprite.spritecollide(player, monsters, True, sprite.collide_mask)
        for colide in sprite_list:
            if player.hp > 0:
           # finish = True

        sprite_list = sprite.spritecollide(player, bonus, True, sprite.collide_mask)
        for colide in sprite_list:
            player.hp += 1


        sprite_list = sprite.spritecollide(player, asteroids, True, sprite.collide_mask)
        for colide in sprite_list:
            if player.hp < 0:
            finish = True

        collide_list = sprite.groupcollide(bullets, monsters, True, True, sprite.collide_mask)
        for collide in collide_list:
            points += 1
            points_text = font1.render("Рахунок: " + str(points), True,(255,255,255))
            collide.rect.x = randint(0, WIDTH -80)
            collide.rect.y = randint(-500, -150)
            collide.speed = randint(3,6)
            namm = randint(1,3)
            if namm == 1:
                bonus.add(Bonus ( randint(0, WIDTH -80), randint(-500, -150), randint(3,6)))
        if points > 10:

            finish = True
            result_text = font2.render("ПРЕМОГА!",True,(230, 145, 12))
    else:
        window.blit(result_text, (300, 250))
        window.blit(restart_text, (300, 350))
    display.update()
    clock.tick(FPS)