from objects.all_import import *

import objects.glib.occluder as occluder
import objects.glib.shadow as shadow
import objects.glib.particles as particles

img = pygame.image.load("data/img/box.png")
img = pygame.transform.scale(img, (80, 80))
class Camera(object):
    def __init__(self, width, height, x, y):
        self.width = width # save width
        self.height = height # save height
        self.size = (width, height) # create size tuple
        self.world = pygame.Surface(self.size) # Create Map Surface
        self.surfaces = [] # surfaces in the map
        self.rects =[] # rects in the map
        self.x = x # map x
        self.y = y # map y
        self.change_x = 0 # x increase
        self.change_y = 0 # y increase
        self.pos = (self.x, self.y) # map position
        self.fill = (0, 0, 0) # map background color
        self.map_world = '' # map tileset
        self.shad = None # shadow not initializated
        self.boxes = []
        self.emitters = []
        self.p_system = particles.ParticleSystem()
        self.font = pygame.font.SysFont("Arial", 12)

    def draw(self, screen, phis, ids, player_id, box2d=True, draw_part=True, debug = False):
        self.world.fill(self.fill)
        self.x += int(self.change_x)
        self.y += int(self.change_y)
        self.pos = (self.x, self.y)
        
        if not self.shad == None:
            self.create_shadow() 
        
        for i in range(0, len(self.surfaces)):
            self.world.blit(self.surfaces[i].obj, self.surfaces[i].pos)
        for i in range(0, len(self.rects)):
            pygame.draw.rect(self.world, self.rects[i][0], self.rects[i][1])
        for i in range(0, len(self.map_world)):
            self.world.blit(self.map_world[i][0], self.map_world[i][1])
        if debug:
            fps = "FPS: "+str(int(debug.get_fps()))
            fps_text = self.font.render(fps, 1, COLORS["white"])
            self.world.blit(fps_text, (0, 0))
        self.update_psys(phis.time_step)
        if draw_part:
            self.p_system.draw(self.world)
        if box2d:
            i=-1
            for body in phis.world.bodies:
                i+=1
                for fixture in body.fixtures:
                    if i == player_id:
                        fixture.shape.draw(body, ids[i], player=True)
                    else:
                        fixture.shape.draw(body, ids[i])
        phis.update()
        screen.blit(self.world, self.pos)
        
    def set_fill(self, new_fill):
        self.fill = new_fill
    def add_emitter(self, acc=[0.0,500.0], density=50, angle=[0, 45], speed=[700, 800], life=[2, 3], colors=[COLORS["red"]]):
        em = particles.Emitter()
        em.set_density(density)
        em.set_angle(angle[0],angle[1])
        em.set_speed(speed)
        em.set_life(life)
        em.set_colors(colors)
        self.emitters.append(em)
        self.p_system.add_emitter(em, "e"+str(len(self.emitters)))
        return len(self.emitters)-1
    def update_psys(self, dt):
        self.p_system.update(dt)

    def move(self, change_x, change_y):
        self.change_x += change_x
        self.change_y += change_y
        

    def get_coord(self):
        return self.pos
    
    def update_size(self, width, height):
        self.width = width
        self.height = height
        self.size = (width, height)

    def add_rect(self, rect, color):
        index = len(self.rects)
        self.rects.insert(index, [color, rect])
        return index

    def update_rect(self, index, new, new_color = "auto"):
        if new_color == "auto":
            self.rects[index] = [self.rects[index][0], new]
        else:
            self.rects[index] = [new_color, new]
        
    def add_surf(self, surf, pos, scale='auto'):
        index = len(self.surfaces)
        if scale == 'auto':
            self.surfaces.insert(index, Surf(surf, pos[0], pos[1], surf.get_size()))
        else:
            self.surfaces.insert(index, Surf(surf, pos[0], pos[1], scale))
        return index

    def update_surf(self, index, new, new_pos, scale = "auto"):
        if new_color == "auto":
            self.rects[index] = [self.rects[index][0], new]
        else:
            self.rects[index] = [new_color, new]

    def set_scale(self, width, height, reload=False, new_light=False, new_rect=False, new_scale = False):
        ex_size = self.size
        self.width = width # save width
        self.height = height # save height
        self.size = (width, height) # create size tuple
        self.world = pygame.transform.scale(self.world, self.size) # resize world
        if reload:
            try:
                new_size = (int((self.current_map[2][0]*self.size[0])/ex_size[0]), int((self.current_map[2][1]*self.size[1])/ex_size[1]))
                self.load_map(self.current_map[0], self.current_map[1], new_size)
            except:
                traceback.print_exc()
                pass
            try:
                self.shad_surf = pygame.Surface(self.size)
                new_occluder = []
                for i in self.occluders:
                    new_occluder.append(i.points)
                for i in range(0, len(new_occluder)):
                    for pos in range(0, len(new_occluder[i])):
                        ex_pos = new_occluder[i][pos]
                        new_x = (self.size[0]*ex_pos[0])/ex_size[0]
                        new_y = (self.size[1]*ex_pos[1])/ex_size[1]
                        new_occluder[i][pos] = (new_x, new_y)
                for i in range(0, len(self.occluders)):
                    self.occluders[i] = occluder.Occluder(new_occluder[i])
                if not new_light:
                    self.load_shadow(self.ldir, self.occluders, self.shad.radius)
                if new_light:
                    self.load_shadow(self.ldir, self.occluders, int((self.shad.radius*self.size[0])/ex_size[0]))
            except:
                traceback.print_exc()
                pass
    def load_map(self, string, rules, scale):
        self.current_map = [string, rules, scale]
        self.map_world = tiles(map_to_list(string), rules, scale)
        for i in range(0, len(self.map_world)-1):
            self.world.blit(self.map_world[i][0], self.map_world[i][1])
    
    def draw_box2d(self, polygon, body, phisi, index, allocate, player=False, occl = True, poly=True, lines=False, color="auto", outline=True): # polygon, screen, ppm, body, fixture, index, occl = True, poly=True, lines=False, color=(0, 0, 0)):
        global img
        if not player:
            vertices = [(body.transform * v) * phisi.meter for v in polygon.vertices]
            vertices = [(v[0], self.height - v[1]) for v in vertices]
            if color == "auto":
                color = COLORS[body.type]
            if body.position[1]*phisi.meter < -40:
                body.DestroyFixture(body.fixtures[0])
                self.boxes[index] = occluder.Occluder(([-1, -1], [-2, -2]))
                self.occluders[allocate] = self.boxes[index]
                self.update_occluders(self.occluders)    
                return 
        if player:
            vertices = [(body.transform * v) * phisi.meter for v in polygon.vertices]
            vertices = [(v[0], self.height - v[1]) for v in vertices]
            # occl = False
            # poly=False
            # lines=False
            body.angle=0
            return
            # color = COLORS["black"]
            # vertices = [(v[0], self.height - v[1]) for v in vertices]
        # mask_surf = pygame.Surface(get_size_from_rect(vertices))
        if occl:
            self.boxes[index] = occluder.Occluder(vertices)
            self.occluders[allocate] = self.boxes[index]
            self.update_occluders(self.occluders)            
        if poly:
            pygame.draw.polygon(self.world, color, vertices)
        if lines:
            pygame.draw.lines(self.world, color, True, vertices)
        if outline:
            pygame.draw.lines(self.world, (255, 255, 255), True, vertices)
    def load_shadow(self, falloff, occluders, radius=100):
        self.ldir = falloff
        falloff = pygame.image.load(falloff)
        self.shad = shadow.Shadow() # create shadow 
        self.surf_light = pygame.transform.scale(falloff, (radius*2, radius*2)).convert() # create light
        self.occluders = occluders # create umbra points
        self.shad.set_occluders(self.occluders) # update occluders
        self.shad.set_radius(radius) # set light radius
        self.shad_surf = pygame.Surface(self.size)
    
    def add_box(self, auto_occ=True):
        self.boxes.append(occluder.Occluder([[0, 0], [1, 1]]))
        if auto_occ:
            self.occluders.append(occluder.Occluder([[0, 0], [1, 1]]))
        return (len(self.boxes)-1, len(self.occluders)-1)

    def update_occluders(self, new_occluder):
        
        self.occluders = new_occluder # create umbra points
        for i in self.occluders: i.set_bounce(0.5)
        self.shad.set_occluders(self.occluders) # update occluders
        self.p_system.set_particle_occluders(self.occluders)

    def create_shadow(self, fill=[0, (0, 0, 0)], occluders_color=(0, 0, 0), ambient_light=(100, 100, 100), with_falloff=True, poly=False):
        mask,draw_pos = self.shad.get_mask_and_position(False)

        if with_falloff:
            mask.blit(self.surf_light,(0,0),special_flags=pygame.BLEND_MULT)

        self.shad_surf.fill(ambient_light)

        self.shad_surf.blit(mask,draw_pos,special_flags=pygame.BLEND_MAX)

        self.world.blit(self.shad_surf,(0,0),special_flags=pygame.BLEND_MULT)

        for occluder in self.occluders:
            #pygame.draw.lines(self.world,occluders_color,True,occluder.points)
            if poly:
                pygame.draw.polygon(self.world, fill[1], occluder.points, width=fill[0])

class Surf(object):
    def __init__(self, obj, x, y, scale):
        self.obj = obj
        self.x = x
        self.y = y
        self.scale = scale

def tiles(mapp, tile, scale):
    result = []
    for y, line in enumerate(mapp):
        for x, c in enumerate(line):
            try:
                resuld.append(tile[c])
            except:
                pass
    return result

def map_to_list(string):
    map1 = string.splitlines()
    map2 = []
    for n, line in enumerate(map1):
        map2.append(list(map1[n]))
    return map2

def get_size_from_rect(vert):
    w = calc_distance(vert[0], vert[1])
    h = calc_distance(vert[2], vert[3])
    return (w, h)
# I hope to be of help and to have understood the request
from math import sqrt # import square root from the math module
def calc_distance(p1, p2): # simple function, I hope you are more comfortable
  return sqrt((p1[0]-p2[0])**2+(p1[1]-p2[1])**2) # Pythagorean theorem

