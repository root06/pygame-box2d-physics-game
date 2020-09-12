from objects.all_import import *

class Player(object):
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.width = w
        self.height = h
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.size = (self.width, self.height)
        self.x_change = 0
        self.y_change = 0
        self.ultimate_change = (self.x_change, self.y_change)
        self.respawn = (self.x, self.y)
        self.jump_avail = True
    def update(self, hei):
        self.box.linearVelocity += (self.x_change/self.meter, -(self.y_change/self.meter))
        # self.box.position -= (0, 1/self.meter)
        #self.x += self.x_change
        #self.y += self.y_change
        vert = self.box.position
        self.x = vert[0]*self.meter-self.width/2
        self.y = hei-(vert[1])*self.meter-self.height/2
        self.rect = pygame.Rect(self.x, self.y+1, self.width, self.height)# pygame.Rect(self.x, self.y, self.width, self.height)
        if self.y > hei:
            self.x = self.respawn[0]
            self.y = self.respawn[1]
            self.def_box2d_pos(hei)
        if self.box.contacts:
            self.jump_avail = True
        return self.rect
    def set_phis(self, body, meter):
        self.box = body
        self.meter = meter
    def move(self, x_change, y_change):
        self.x_change += x_change
        self.y_change += y_change
        self.ultimate_change = [self.x_change, self.y_change]

    def stop(self):
        self.x_change = 0
        self.y_change = 0

    def get_rect(self):
        return self.rect

    def resize(self, w, h):
        self.width = w
        self.height = h
        self.size = (self.width, self.height)

    def def_box2d_pos(self, hei):
        self.box.position = (self.x/self.meter+((self.width/2)/self.meter), (self.y/self.meter)+(hei/self.meter)-((self.height/2)/self.meter)-0.1)
    def jump(self, force=8):
        if self.jump_avail:
            self.jump_avail = False
            self.box.linearVelocity += (0, force)
        
        # print(dir(self.box))
