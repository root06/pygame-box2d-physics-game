import pygame
from pygame.locals import *
import traceback
from multi_key_dict import multi_key_dict
from Box2D.b2 import staticBody, dynamicBody, kinematicBody
import pickle
import os, time, sys


COLORS = pygame.color.THECOLORS # all colors ( maybe ) in rgb shortcut
COLORS[staticBody] = COLORS["grey"]
COLORS[dynamicBody] = COLORS["darkslategrey"]
COLORS[kinematicBody] = COLORS["red"]

def restart():
  os.execl(sys.executable, sys.executable, *sys.argv) 

def exit(code="tutto ok!"):
  pygame.mixer.quit()
  pygame.display.quit()
  pygame.quit()
  from pathlib import Path
  if Path("temp.jpeg").exists():
    os.remove("temp.jpeg")
  sys.exit(code)
