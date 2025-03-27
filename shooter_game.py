from pygame import *
from random import randint
from time import time as time1

win_width = 700
win_height = 500
clock = time.Clock()
FPS = 60
window = display.set_mode((win_width, win_height))
display.set_caption('Space')
background = transform.scale(image.load('galaxy.jpg'), (win_width, win_height))
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
font.init()
font1 = font.SysFont('Arial', 36)
font2 = font.SysFont('Arial', 50)
font3 = font.SysFont('Arial', 25)
lost = 0
score = 0
lifes = 3
num_fire = 0
bullets = sprite.Group()

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, player_width, player_height):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (player_width, player_height))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys_pressed[K_RIGHT] and self.rect.x < 630:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.x + 25, self.rect.y, 10, 20, 30)
        bullets.add(bullet)
class Enemy(GameSprite):
    def update(self):
        global lost 
        self.rect.y += self.speed
        if self.rect.y > win_height or self.rect.y == win_height:
            self.rect.y = 0
            self.rect.x = randint(50, win_width - 50)
            lost += 1
class Asteroid(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > win_height or self.rect.y == win_height:
            self.rect.y = 0
            self.rect.x = randint(50, win_width - 50)
class Bullet (GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0 :
            self.kill()





    

asteroids = sprite.Group()
asteroid1 = Asteroid('asteroid.png', randint(0, 630), 0, 1, 50, 50)
asteroid2 = Asteroid('asteroid.png', randint(0, 630), 0, 2, 50, 50)
asteroid3 = Asteroid('asteroid.png', randint(0, 630), 0, 1, 50, 50)
asteroids.add(asteroid1)
asteroids.add(asteroid2)
asteroids.add(asteroid3)







monsters = sprite.Group()
monster1 = Enemy('ufo.png', randint(0, 630), 0, 2, 50, 30)
monster2 = Enemy('ufo.png', randint(0, 630), 0, 1, 50, 30)
monster3 = Enemy('ufo.png', randint(0, 630), 0, 1, 50, 30)
monster4 = Enemy('ufo.png', randint(0, 630), 0, 1, 50, 30)
monster5 = Enemy('ufo.png', randint(0, 630), 0, 2, 50, 30)
monsters.add(monster1)
monsters.add(monster2)
monsters.add(monster3)
monsters.add(monster4)
monsters.add(monster5)
player = Player('rocket.png', 300, 435, 7, 65, 65)

rel_time = False
game = True
finish = False
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
           if e.key == K_SPACE:
                if num_fire < 5 and rel_time == False:
                    player.fire()
                    mixer.music.load('fire.ogg')
                    mixer.music.play()
                    num_fire += 1
                if num_fire >= 5 and rel_time == False:
                    rel_time = True
                    start_time = time1()
                
                
                



               
    text_lifes = font1.render('Жизни : ' + str(lifes), 1, (238, 255, 255))
    text_score = font1.render('Счет : ' + str(score), 1, (238, 255, 255))
    text_lose = font1.render('Пропущено : ' + str(lost), 1, (238, 255, 255))
    if finish != True:
        window.blit(background, (0, 0))
        player.reset()
        player.update()
        monsters.draw(window)
        monsters.update()
        asteroids.draw(window)
        asteroids.update()
        window.blit(text_score, (5, 5))
        window.blit(text_lose, (5, 40))
        window.blit(text_lifes, (5, 75))
        bullets.draw(window)
        bullets.update()


        if score > 5 or score == 5:
            finish = True
            text_win = font2.render('YOU WIN!', 1, (110, 197, 87))
            window.blit(text_win, (250, 220))
        if lost > 3 or sprite.spritecollide(player, monsters, False) or lifes == 0:
            finish = True
            text_lose = font2.render('YOU LOSE!', 1, (226, 46, 55))
            window.blit(text_lose, (250, 220))

        collides = sprite.groupcollide(monsters, bullets, True, True)
        for collide in collides:
            score += 1
            monster = Enemy('ufo.png', randint(0, 630), 0, 2, 50, 30)
            monsters.add(monster)

        if sprite.spritecollide(player, asteroids, True):
            lifes -= 1
            asteroid = Asteroid('asteroid.png', randint(0, 630), 0, 1, 50, 50)
            asteroids.add(asteroid)
        if rel_time == True:
            finish_time = time1()
            if finish_time - start_time < 3:
                text_rel_time = font3.render('Wait, reload...', 1, (147, 0, 0))
                window.blit(text_rel_time, (250, 480))
            else:
                num_fire = 0
                rel_time = False
        

    display.update()
    clock.tick(FPS)
