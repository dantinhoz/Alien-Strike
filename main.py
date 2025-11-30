import pgzrun
from pygame import Rect
import math
from pygame.transform import scale

# CONFIGURAÇÕES
WIDTH, HEIGHT = 1300, 600
TITLE = "Alien Strike"
MENU, PLAYING, PAUSED, CREDITS, VICTORY, GAME_OVER = 0, 1, 2, 3, 4, 5
game_state = MENU
sound_on = True
music_playing = False

# PLATAFORMAS E OBEJTIVO
platforms = [
    Rect(0, HEIGHT-40, WIDTH, 40),      # ground
    Rect(200, 460, 220, 20),            # low left
    Rect(480, 390, 180, 20),            # mid left
    Rect(320, 300, 140, 20),            # center lower
    Rect(700, 340, 160, 20),            # center higher
    Rect(980, 260, 180, 20),            # path to right
    Rect(880, 150, 160, 20),            # top area
    Rect(560, 220, 140, 20),            # connector
]
objective_x, objective_y = 1370, 400

# ANIMAÇÃO
class SpriteAnimator:
    def __init__(self, names, speed=0.15):
        self.names, self.speed, self.frame = names, speed, 0
        self.images = [getattr(images, n, None) for n in names]
    def update(self):
        self.frame = (self.frame + self.speed) % max(1, len(self.images))
    def get_image(self):
        return self.images[int(self.frame)]

# ALIEN
class Alien:
    def __init__(self):
        self.x = 100
        self.y = HEIGHT - 120
        self.vx = 0
        self.vy = 0
        self.width = 24
        self.height = 24
        self.on_ground = False
        self.facing_right = False
        self.state = 'idle'
        
        # ANIMAÇÕES ALIEN
        self.idle_anim = SpriteAnimator(['tile_0000', 'tile_0000'], 0.12)
        self.run_anim = SpriteAnimator(['tile_0000', 'tile_0001'], 0.2)
        self.jump_anim = SpriteAnimator(['tile_0000'], 0.1)

    def update(self):
        keys = keyboard
        
        # ALIEN MOVE HORIZONTAL
        if keys.left:
            self.vx = -4
            self.facing_right = True
            self.state = 'run'
        elif keys.right:
            self.vx = 4
            self.facing_right = False
            self.state = 'run'
        else:
            self.vx *= 0.8  # Atrito
            self.state = 'idle' if abs(self.vx) < 0.5 else 'run'
        
        # ALIEN JUMP
        if keys.up and self.on_ground:
            self.vy = -12
            self.state = 'jump'
            if sound_on:
                try:
                    sounds.jump.play()
                except:
                    pass
        
        # ALIEN GRAVIDADE
        self.vy += 0.6
        
        # ATUALIZAR POSIÇÃO
        self.x += self.vx
        self.y += self.vy
        
        # ALIEN COLISÃO
        self.check_platform_collisions()
        self.x = max(0, min(WIDTH - self.width, self.x))
        self.y = max(0, min(HEIGHT - self.height, self.y))
        
        # ATUALIZAR ANIMAÇÃO
        self.idle_anim.update()
        self.run_anim.update()

    # FUNÇÃO COLISÃO
    def check_platform_collisions(self):
        self.on_ground = False
        alien_rect = Rect(self.x, self.y + self.height - 5, self.width, 5)
        
        for plat in platforms:
            if alien_rect.colliderect(plat):
                if self.vy > 0:
                    self.y = plat.top - self.height
                    self.vy = 0
                    self.on_ground = True
                    self.vx *= 0.7
                break

    # DRAW ALIEN
    def draw(self):
        anim = self.idle_anim if self.state == 'idle' else self.run_anim
        img = anim.get_image()
        try:
            screen.blit(img, (self.x, self.y))
        except Exception:
            screen.draw.filled_rect(Rect(self.x, self.y, self.width, self.height), (0,255,0))
            screen.draw.text("SPRITE OK", (self.x, self.y+10), color="black")


# BANDEIRA
class Flag:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.anim = SpriteAnimator(['tile_0111','tile_0112'], 0.18)
    def update(self): self.anim.update()
    def draw(self):
        img = self.anim.get_image();
        try: screen.blit(img, (self.x, self.y))
        except: screen.draw.text('F', (self.x, self.y), fontsize=20, color='yellow')


# INIMIGO
class Enemy:
    def __init__(self, x, y, patrol_left, patrol_right):
        self.x = x
        self.y = y
        self.patrol_left = patrol_left
        self.patrol_right = patrol_right
        self.vx = 1.2
        self.width = 28
        self.height = 28
        self.idle_anim = SpriteAnimator(['tile_0011'], 0.1)
        self.run_anim = SpriteAnimator(['tile_0011', 'tile_0012'], 0.18)

    def update(self):
        self.x += self.vx
        # LOGICA ANDAR INIMIGO/PATRULHA
        if self.x <= self.patrol_left or self.x >= self.patrol_right:
            self.vx *= -1
        # ANIMAÇÕES
        self.idle_anim.update()
        self.run_anim.update()

    # DRAW INIMIGO
    def draw(self):
        img = self.run_anim.get_image()
        try:
            screen.blit(img, (self.x, self.y))
        except Exception:
            screen.draw.filled_rect(Rect(self.x, self.y, self.width, self.height), (255,0,0))


# INIMIGO VOADOR
class FlyingEnemy:
    def __init__(self, x, y, amp=40, speed=0.08, vx=1.0):
        self.x = x
        self.base_y = y
        self.amp = amp
        self.phase = 0
        self.phase_speed = speed
        self.vx = vx
        self.width = 28
        self.height = 28
        self.anim = SpriteAnimator(['tile_0024','tile_0025','tile_0026'], 0.18)

    # LOGICA MOVIMENTO
    def update(self):
        self.x += self.vx
        self.phase += self.phase_speed
        self.y = self.base_y + math.sin(self.phase) * self.amp
        if self.x < 0 or self.x > WIDTH - self.width:
            self.vx *= -1
        self.anim.update()

    # DRAW INIMIGO VOADOR
    def draw(self):
        img = self.anim.get_image()
        try:
            screen.blit(img, (self.x, self.y))
        except Exception:
            screen.draw.filled_rect(Rect(self.x, self.y, self.width, self.height), (200,50,50))


# POSIÇÕES INICIAIS
alien = None
enemies = []
flag = None
lives = 2
def init_game():
    global alien, enemies, flag, objective_x, objective_y, lives
    alien = Alien()
    enemies = [
        Enemy(200, HEIGHT-40 - 28, 150, 350),
        Enemy(500, HEIGHT-40 - 28, 450, 650),
        Enemy(240, 460 - 28, 210, 380),
        Enemy(1000, 260 - 28, 980, 1160),
    ]
    highest = min(platforms, key=lambda r: r.top)
    objective_x = highest.centerx
    objective_y = highest.top
    flag = Flag(objective_x - 16, objective_y - 32)
    enemies.append(FlyingEnemy(640, 200, amp=40, speed=0.08, vx=1.0))
    lives = 2


# DRAW PRINCIPAL
def draw():
    global alien
    if alien is None: init_game()
    screen.clear()
    if game_state == MENU: draw_menu(); return
    if game_state == PLAYING: draw_game(); return
    if game_state == PAUSED:
        draw_game();
        screen.draw.filled_rect(Rect(0,0,WIDTH,HEIGHT),(0,0,0,128))
        screen.draw.text("PAUSED", center=(WIDTH//2,HEIGHT//2), fontname='kenney_pixel', fontsize=72, color='white')
        screen.draw.text("press ESC to resume", center=(WIDTH//2,350), fontname='kenney_pixel', fontsize=36, color='white')
        btn_img = getattr(images, return_button['img'], None)
        if btn_img:
            try:
                # Aumentar sprite 1.5x usando scale
                scaled_img = scale(btn_img, (int(btn_img.get_width() * 1.5), int(btn_img.get_height() * 1.5)))
                screen.blit(scaled_img, return_button['rect'].topleft)
            except:
                screen.draw.filled_rect(return_button['rect'], (180,60,60))
        else:
            screen.draw.filled_rect(return_button['rect'], (180,60,60))
        return
    if game_state == CREDITS: draw_credits(); return
    if game_state == VICTORY: draw_victory(); return
    if game_state == GAME_OVER: draw_game_over(); return


# MENU
menu_buttons = [
    {"text": "START", "rect": Rect(500, 220, 300, 60), "action": "start"},
    {"text": "SOUND " + ("ON" if sound_on else "OFF"), "rect": Rect(500, 300, 300, 60), "action": "sound"},
    {"text": "CREDITS", "rect": Rect(500, 380, 300, 60), "action": "credits"},
    {"text": "EXIT", "rect": Rect(500, 460, 300, 60), "action": "exit"}
]
# DRAW MENU
def draw_menu():
    screen.fill((16,125,79))
    screen.draw.text("ALIEN STRIKE", center=(WIDTH//2,120), fontname='kenney_pixel', fontsize=48, color='white')
    screen.draw.text("Use ARROWS to play", center=(WIDTH//2,180), fontname='kenney_pixel', fontsize=24, color=(75,192,97))
    for b in menu_buttons: screen.draw.filled_rect(b['rect'],(75,192,97)); screen.draw.text(b['text'], center=b['rect'].center, fontname='kenney_pixel', fontsize=28, color='white')


# CREDITS
credits_text = [
    "'ALIEN STRIKE'",
    "",
    "DEVELOPMENT",
    "Game Design & Programming  - Dante Lopes",
    "",
    "ASSETS",
    "Sprites & Sound - Kenney",
    "Soundtrack Music - Viacheslav 'original_soundtrack' Starostin"
]
return_button = {"img": 'tile_0576', "rect": Rect(20, 20, 64, 64), "action": "menu"}
# DRAW CREDITS
def draw_credits():
    screen.fill((16,125,79)); screen.draw.text("CREDITS", center=(WIDTH//2,40), fontname='kenney_pixel', fontsize=48, color='white')
    y=100
    for line in credits_text:
        if not line: y+=20; continue
        sz=32 if line.startswith(('DEVELOPMENT','ASSETS')) else 24
        col=(255,215,0) if sz==32 else (75,192,97)
        screen.draw.text(line, center=(WIDTH//2,y), fontname='kenney_pixel', fontsize=sz, color=col); y+=40 if sz==32 else 30
    btn_img = getattr(images, return_button['img'], None)
    if btn_img:
        try:
            scaled_img = scale(btn_img, (int(btn_img.get_width() * 1.5), int(btn_img.get_height() * 1.5)))
            screen.blit(scaled_img, return_button['rect'].topleft)
        except:
            screen.draw.filled_rect(return_button['rect'], (180,60,60))


# DRAW VICTORY
def draw_victory():
    screen.fill((16,125,79)); screen.draw.text("CONGRATULATIONS!", center=(WIDTH//2, 150), fontname='kenney_pixel', fontsize=48, color=(255,215,0))
    screen.draw.text("YOU WON!", center=(WIDTH//2, 230), fontname='kenney_pixel', fontsize=56, color='white')
    screen.draw.text("Press SPACE to return to menu", center=(WIDTH//2,400), fontname='kenney_pixel', fontsize=20, color=(75,192,97))


# DRAW GAME OVER
def draw_game_over():
    screen.fill((40,20,20))
    screen.draw.text("GAME OVER", center=(WIDTH//2,150), fontname='kenney_pixel', fontsize=64, color=(255,80,80))
    screen.draw.text("You Died", center=(WIDTH//2,230), fontname='kenney_pixel', fontsize=36, color='white')
    screen.draw.text("Press SPACE to return to menu", center=(WIDTH//2,360), fontname='kenney_pixel', fontsize=20, color=(200,200,200))


# DRAW GAME
def draw_game():
    screen.fill((40,100,160))
    for p in platforms: screen.draw.filled_rect(p,(80,160,60)); screen.draw.rect(p,(120,200,100))
    if flag: flag.draw()
    else: screen.draw.filled_rect(Rect(objective_x-15,objective_y-15,30,30),(255,215,0)); screen.draw.text('?',(objective_x-6,objective_y-12),fontsize=24,color='white')
    alien.draw(); [e.draw() for e in enemies]
    screen.draw.text(f"Sound: {'ON' if sound_on else 'OFF'}", (10,10), fontsize=24, fontname='kenney_pixel', color='white')
    screen.draw.text(f"State: {alien.state}", (10,40), fontsize=20, fontname='kenney_pixel', color='white')
    # HUD
    full = getattr(images, 'tile_0044', None)
    empty = getattr(images, 'tile_0046', None)
    start_x = WIDTH - 120
    for i in range(2):
        img = full if i < lives else empty
        x = start_x + i * 60
        if img:
            try:
                scaled_img = scale(img, (int(img.get_width() * 1.5), int(img.get_height() * 1.5)))
                screen.blit(scaled_img, (x, 5))
            except:
                screen.draw.filled_rect(Rect(x, 5, 50, 50), (200,0,0))
        else:
            screen.draw.filled_rect(Rect(x, 5, 50, 50), (200,0,0))


# UPDATE STATES
def update():
    global game_state, sound_on, music_playing, alien, lives
    if alien is None: init_game()

    # MUSICA
    if game_state in [MENU, PLAYING, CREDITS, VICTORY]:
        if sound_on and not music_playing:
            try:
                music.play('retro_arcade')
                music.set_volume(0.15)
                music_playing = True
            except Exception as e:
                music_playing = True
        elif sound_on and music_playing:
            try:
                music.unpause()
            except:
                pass
        elif not sound_on and music_playing:
            try:
                music.pause()
            except:
                pass
    elif game_state in [GAME_OVER, PAUSED]:
        if music_playing:
            try:
                music.pause()
            except:
                pass
    
    if game_state != PLAYING: return
    alien.update(); [e.update() for e in enemies]
    if flag: flag.update()

    # COLISÕES
    a = Rect(alien.x, alien.y, alien.width, alien.height)
    for e in enemies:
        if a.colliderect(Rect(e.x, e.y, e.width, e.height)):
            if lives > 1:
                lives_left = lives - 1
                alien.x = 100; alien.y = HEIGHT - 120; alien.vx = alien.vy = 0
                globals()['lives'] = lives_left
                return
            else:
                game_state = GAME_OVER
                return
    if a.colliderect(Rect(objective_x-15,objective_y-15,30,30)):
        game_state = VICTORY

# CLICKS
def on_mouse_down(pos):
    global game_state, sound_on
    if game_state==MENU:
        for b in menu_buttons:
            if b['rect'].collidepoint(pos):
                if b['action']=='start':
                    init_game()
                    game_state=PLAYING
                elif b['action']=='sound':
                    sound_on=not sound_on; [x.update() for x in menu_buttons if x['action']=='sound'];
                    for x in menu_buttons:
                        if x['action']=='sound': x['text']='SOUND '+('ON' if sound_on else 'OFF'); break
                elif b['action']=='credits': game_state=CREDITS
                elif b['action']=='exit': exit()
    elif game_state==CREDITS and return_button['rect'].collidepoint(pos): game_state=MENU
    elif game_state==PAUSED:
        if return_button['rect'].collidepoint(pos):
            game_state = MENU
        else:
            game_state = PLAYING
            try:
                music.unpause()
            except:
                pass

def on_key_down(key):
    global game_state, music_playing
    if key==keys.ESCAPE:
        if game_state == PLAYING:
            game_state = PAUSED
            try:
                music.pause()
            except:
                pass
        elif game_state == PAUSED:
            game_state = PLAYING
            try:
                music.unpause()
            except:
                pass
    elif key==keys.SPACE and game_state==VICTORY:
        alien.x=100; alien.y=HEIGHT-120; alien.vx=alien.vy=0; game_state=MENU
    elif key==keys.SPACE and game_state==GAME_OVER:
        game_state=MENU

pgzrun.go()