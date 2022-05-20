#Создай собственный Шутер!

from pygame import *
from random import randint
from time import time as timer

lost = 0

window = display.set_mode((700, 500))
display.set_caption("Шутер")
background = transform.scale(image.load("galaxy.jpg"), (700, 500))

font.init()
font1 = font.SysFont('Arial', 35)
text_lose = font1.render('Пропущено: ' + str(lost), 1, (255, 255, 255))

font2 = font.SysFont('Arial', 35)
text_chet = font2.render('Счёт: ', 1, (255, 255, 255))

font3 = font.SysFont('Arial', 35)
text_win = font3.render('You Win!', 1, (255, 255, 255))

font4 = font.SysFont('Arial', 35)
text_losed = font4.render('You Lose!', 1, (255, 255, 255))
font5 = font.SysFont('Arial', 35)
text_reload = font5.render("Wait, reload", 1, (255, 0, 0))


class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, player_weidth, player_height):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (player_weidth, player_height))
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

    def Fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 7, 5, 15)
        bullets.add(bullet)  

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y >= 500:
            self.rect.y = 0
            self.rect.x = randint(0,635)
            global lost
            lost += 1

class Asteroid(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y >= 500:
            self.rect.y = 0
            self.rect.x = randint(0,635)
            global lost
            lost += 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y <= 0:
            self.kill()
    
FPS = 60
clock= time.Clock()

num_fire= 0
rel_time = False



asteroids = sprite.Group()
for i in range(2):
    asteroid = Asteroid('asteroid.png', randint(0, 635), 0, randint(2,5), 65, 45)
    asteroids.add(asteroid)

rocket = Player("rocket.png", 285, 425, 10, 55, 65)
bullets = sprite.Group()

monsters = sprite.Group()
for i in range (5):
    monster = Enemy('ufo.png', randint(0,635), 0, randint(2,5), 65, 45)
    monsters.add(monster)

score = 0
game = True
Finish = False
while game:
    if Finish != True:
        


        text_chet = font2.render('Счёт: '+ str(score), 1, (255, 255, 255))
        text_lose = font1.render('Пропущено: ' + str(lost), 1, (255, 255, 255))
        text_win = font3.render('You Win!', 1, (255, 162, 0))
        text_losed = font4.render('You Lose!', 1, (205, 0, 0)) 
        window.blit(background, (0,0))
        window.blit(text_chet, (0,25))
        window.blit(text_lose, (0,50))
        bullets.update()
        bullets.draw(window)
        rocket.update() 
        rocket.reset()
        monsters.update()
        monsters.draw(window)
        asteroids.update()
        asteroids.draw(window)
        sprites_list = sprite.spritecollide(rocket, monsters, False)
        sprites_list2 = sprite.groupcollide(monsters, bullets, True, True)
        sprites_list3 = sprite.spritecollide(rocket, asteroids, False)



        if len(sprites_list) > 0:
            window.blit(text_losed, (350, 250))
            Finish = True

        if len(sprites_list3) > 0:
            window.blit(text_losed, (350, 250))
            Finish = True

        if score > 41:
            window.blit(text_win, (350, 250))
            Finish = True
        
        if lost > 21:
            window.blit(text_losed, (350, 250))
            Finish = True

        for s in sprites_list2:
            score += 1
            monster = Enemy('ufo.png', randint(0,635), 0, randint(2,5), 65, 45)
            monsters.add(monster)

        if rel_time == True:
            new_time = timer()
            if new_time - old_time >= 3:
                num_fire = 0
                rel_time = False
            else:
                text_reload = font5.render("Wait, reload", 1, (255, 0, 0))
                window.blit(text_reload, (285, 450))
                
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 10 and rel_time == False:
                    rocket.Fire()
                    num_fire += 1
                else:
                    rel_time = True
                    old_time = timer()
            
        

    display.update()
    clock.tick(FPS)