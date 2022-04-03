from pygame import *
from random import *
from time import time as timer 
font.init()
font1 = font.Font(None, 80)
lose = font1.render('You Lose', True, (180, 0 , 0))
win = font1.render('You win', True, (180, 0 , 0))
max_score = 120

class GameSprite(sprite.Sprite):
    def __init__(self,player_img, player_x, player_y, size_x, size_y, player_speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_img), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height :
            self.rect.x = randint(80, win_wigth - 80)
            self.rect.y = 0
            lost = lost + 1
            
class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys_pressed[K_RIGHT] and self.rect.x < win_wigth - 80:
            self.rect.x += self.speed
        if keys_pressed[K_UP] and self.rect.y < win_height - 80:
            self.rect.y -= self.speed     
        if keys_pressed[K_DOWN] and self.rect.y < win_height - 80:
            self.rect.y += self.speed         
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)







mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')
font.init()
font2 = font.Font(None, 36)
win_wigth = 700
win_height = 500
hero = Player('rocket.png',5, win_height - 100, 80, 100, 10)
monsters = sprite.Group()
for i in range(1, 6):
    ufo = Enemy('ufo.png', randint(80, win_wigth - 80), -40,80, 50, randint(1 , 6))
    monsters.add(ufo)
asteroinds = sprite.Group()
for i in range(1, 3):
    asteroind = Enemy('asteroid.png', randint(30, win_wigth - 30), -40, 80, 50, randint(1, 2))
    asteroinds.add(asteroind)

bullets = sprite.Group()    
score = 0
lost = 0
max_lost = 3
life = 3
window = display.set_mode((win_wigth,win_height))
display.set_caption('shooter')
background = transform.scale(image.load('galaxy.jpg'),(700,500))
game = True
finish = False
rel_time = False
num_fire = 0
clock = time.Clock()
FPS = 60
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False

        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and rel_time == False:
                    num_fire = num_fire + 1
                    hero.fire()

                if num_fire >= 5 and rel_time == False:
                    last_time = timer()
                    rel_time = True



    if not finish:


        window.blit(background, (0,0))
        monsters.update()
        hero.update()
        asteroinds.update()
        bullets.update()
        hero.reset()
        monsters.draw(window)
        bullets.draw(window)
        asteroinds.draw(window)


        if rel_time == True:
            now_time = timer()


            if now_time - last_time < 0.3:
                reload = font2.render('Wait, reload', 1,(150, 0, 0))
                window.blit(reload,(250, 460))
            else:
                num_fire = 0
                rel_time = False






        
        text = font2.render('Score: ' + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))
        text_lose = font2.render('Missed: ' + str(lost), 1 ,(255, 255, 255))
        window.blit(text_lose, (10, 50))

        if life == 3:
            life_color = (0, 150, 0)
        if life == 2:
            life_color = (150, 150, 0)
        if life == 1:
            life_color = (150, 0, 0)

        text_life = font1.render(str(life), 1, life_color)
        window.blit(text_life,(650, 10))



        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score = score + 1
            monster = Enemy('ufo.png', randint(80, win_wigth - 80), - 40, 80, 50, randint(1, 5))
            monsters.add(monster)


        if sprite.spritecollide(hero, monsters, False) or sprite.spritecollide(hero, asteroinds, False):
            sprite.spritecollide(hero,monsters, True)
            sprite.spritecollide(hero,asteroinds, True)
            life = life - 1

        if life == 0 or lost > max_lost:
            finish = True
            window.blit(lose,(200, 200))




        if sprite.spritecollide(hero, monsters, False) or lost >= max_lost:
            window.blit(lose,(200,200))
            finish = True
        if score >= max_score:
            window.blit(win,(200,200))
            finish = True
    else: 
        finish = False
        score = 0
        lost = 0
        life = 3
        for b in bullets:
            b.kill()
  
        for m in monsters:

            m.kill()
        time.delay(3000)
        for i in range(1, 6):
            monster = Enemy('ufo.png', randint(80, win_wigth - 80), - 40, 80, 50, randint(1, 5))
            monsters.add(monster)








    display.update()
    
    clock.tick(FPS)
