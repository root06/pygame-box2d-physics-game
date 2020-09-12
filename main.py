import pygame
from pygame.locals import *
from objects.camera import *
from objects.player import *
from objects.splash_menu import *
from objects.box2d import *
from objects.save import *
from multi_key_dict import multi_key_dict
import os, sys, random

# Box2D.b2 maps Box2D.b2Vec2 to vec2 (and so on)
THEME = 0
occluders = []
# occluders.append(occluder.Occluder([[256,256],[256,300],[300,300]]))
#occluders.append(occluder.Occluder([[156,156],[156,200],[200,200]]))
DATA_DIR = os.path.join('data/')
# MUSIC_DIR = os.path.join(DATA_DIR+'music/') there was music but it weighed too much
IMG_DIR = os.path.join(DATA_DIR+'img/')
FONTS_DIR = os.path.join(DATA_DIR+'fonts/')
SAVE_DIR = os.path.join(DATA_DIR+'save/')
DATABASE = os.path.join(SAVE_DIR+'database.p')
DEFAULT = os.path.join(SAVE_DIR+'default.p')

save_main = Save(DATABASE, DEFAULT)
save = save_main.load()

pygame.init()

control(save_main)

# so define a conversion factor:
PPM = 20.0  # pixels per meter
TARGET_FPS = 80
TIME_STEP = 1.0 / TARGET_FPS

COLORS = pygame.color.THECOLORS # all colors ( maybe ) in rgb shortcut

DISPLAY = [640, 480]
FLAGS = RESIZABLE
screen = pygame.display.set_mode(DISPLAY, FLAGS)

world = Camera(DISPLAY[0], DISPLAY[1], 0, 0)
world.set_fill(COLORS["white"])
player = Player(100, 1, 15, 34)
world.load_shadow(IMG_DIR+"light_falloff100.png", occluders)
phis = Game(TARGET_FPS, PPM)

# pygame.mixer.music.load(MUSIC_DIR+'test.wav')
# pygame.mixer.music.play(-1)

def add_body(typ, pos, box, density=1, friction=0.3, mass=1):
  phis.add_body(typ, pos, box, density=density, friction=friction, mass=mass)
  return world.add_box()
id_S = [
  add_body("p", ((player.x/phis.meter), player.y/phis.meter), (player.width/(phis.meter*2), player.height/(phis.meter*2)), density=10, friction=0.8, mass=500),
  add_body("s", (0, 0), (50, 0.5)),
  add_body("s", (0, 0), (0.5, 50)),
  add_body("s", (20, 10), (5, 0.5))
]

for _ in range(0, 10):
  id_S.append(add_body("d", (random.randint(5, 35), 45), (2, 2)))
# del random
part = world.add_emitter(angle=[360, 360], life=[1, 3], colors=[COLORS["aliceblue"], COLORS["cadetblue1"], COLORS["darkslategray2"], COLORS["lightblue2"]])
#  add_body("d", (21, 45), (2, 1)),
#  add_body("d", (23, 45), (2, 1)),
#  add_body("d", (28, 45), (2, 1)),
player.set_phis(phis.player_body[0][0], phis.meter)
player.def_box2d_pos(world.height)
player_id = world.add_rect(player.get_rect(), COLORS["red"])
# phis.add_body("s", (0, 0), (50, 1), world.boxes)
# id2 = world.add_box()

KEY = multi_key_dict()
KEY[K_RIGHT, K_d] = (4, 0)
KEY[K_LEFT, K_a] = (-4, 0)
KEY[K_DOWN, K_s] = (0, 4)

menu(**{"img_DIR":IMG_DIR+"menu/", "fdir":FONTS_DIR, "theme_index":THEME, "save":save, "save_main":save_main})

clock = pygame.time.Clock()

# Let's play with extending the shape classes to draw for us.
def draw_polygon(polygon, body, ids, player=False):
  world.draw_box2d(polygon, body, phis, ids[0], ids[1], player=player)
  # for i in world.occluders: print(i.points)
  # world.draw_box2d(polygon, body, phis, 1, 3)
  # print(world.occluders[id2[1]].points)
  #pygame.draw.polygon(screen, colors[body.type], vertices)

polygonShape.draw = draw_polygon



screen = pygame.display.set_mode(pygame.display.get_window_size(), FLAGS)

# Game loop.
while True:
  
  mouse_position = pygame.mouse.get_pos()
  for event in pygame.event.get():
    if event.type == QUIT:
      exit()
    elif event.type == VIDEORESIZE:
      #world.set_scale(event.w, event.h)
      pygame.display.update()
    elif event.type == VIDEOEXPOSE:
      
      #world.set_scale(event.w, event.h)
      pygame.display.update()
      world.set_scale(screen.get_width(), screen.get_height(), reload=True, new_light=False)
    if event.type == KEYDOWN:
      # if event.key == K_ESCAPE:
      #  exit()
      if KEY.has_key(event.key):
        player.move(KEY[event.key][0], KEY[event.key][1])
      if event.key == K_SPACE:
        player.jump()
      if event.key == K_q:
        id_S.append(add_body("d", (random.randint(5, 35), 45), (2, 2)))
      if event.key == K_ESCAPE:
        pause(screen,**{"save":save, "save_main":save_main, "fdir":FONTS_DIR, "flags":FLAGS, "theme_index":THEME})
        
    if event.type == KEYUP:
      if KEY.has_key(event.key):
        player.move(-KEY[event.key][0], -KEY[event.key][1])
  # world.emitters[part].set_position(mouse_position)
  world.shad.set_light_position(player.rect.center)#(int(player.x+player.width/2), int(player.y+player.height/2)))
  world.update_rect(player_id, player.update(world.height))
  # player.update(world.world, world.height)
  world.draw(screen, phis, id_S, 0, draw_part=False, debug=clock)
  pygame.display.flip()
  clock.tick(TARGET_FPS)


