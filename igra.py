#Создай собственный Шутер!

from pygame import *
from random import randint

mixer.init()
mixer.music.load('listen.ogg')
mixer.music.play()
fire_sound = mixer.Sound('listen.ogg')
img_bullet='banana.png'
img_hero='monkey.png'
img_enemy='spider.png'

font.init()
font1=font.Font(None,80)
win=font1.render('YOU WIN', True, (255,255,255))
lose=font1.render('YOU lOSE',True, (180,0,0))

font2=font.Font(None, 36)

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x,player_y, size_x, size_y, player_speed):
        super().__init__()
        self.image=transform.scale(image.load(player_image), (size_x, size_y))
        self.speed=player_speed
        self.rect=self.image.get_rect()
        self.rect.x=player_x
        self.rect.y=player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x-=self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
    def fire(self):
        bullet=Bullet(img_bullet, self.rect.centerx, self.rect.top, 15,20, -15)
        bullets.add(bullet)
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x=randint(80, win_width-80)
            self.rect.y=0
            lost=lost+1
class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

score = 0 
goal = 15 
lost = 0 
max_lost = 1

win_width =700
win_height=500
display.set_caption('Shooter')
window=display.set_mode((win_width, win_height))
background=transform.scale(image.load('jungle.jpg'), (win_width, win_height))
game=True
finish=False
daun=Player('monkey.png', 5, win_height - 100, 80, 100, 10)
monsters=sprite.Group()
for i in range(1,6):
    monster=Enemy('spider.png',randint(80,win_width-80),-40,80,50,randint(1,5))
    monsters.add(monster)
bullets=sprite.Group()
while game:
    for e in event.get():
        if e.type == QUIT:
            game=False
        elif e.type==KEYDOWN:
            if e.key==K_SPACE:
                fire_sound.play()
                daun.fire()
            
    if not finish:
        window.blit(background,(0,0))
        # пишем текст на экране
        text = font2.render("Счет: " + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))

        text_lose = font2.render("Пропущено: " + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))

        
        daun.update()
        monsters.update()
        bullets.update()
        daun.reset()
        monsters.draw(window)
        bullets.draw(window)
        # проверка столкновения пули и монстров (и монстр, и пуля при касании исчезают)
        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            # этот цикл повторится столько раз, сколько монстров подбито
            score = score + 1
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)

        # возможный проигрыш: пропустили слишком много или герой столкнулся с врагом
        if sprite.spritecollide(daun, monsters, False) or lost >= max_lost:
            finish = True # проиграли, ставим фон и больше не управляем спрайтами.
            window.blit(lose, (200, 200))

        # проверка выигрыша: сколько очков набрали?
        if score >= goal:
            finish = True
            window.blit(win, (200, 200))



    display.update()
    time.delay(50)