from objects import glib as gl
from objects.all_import import *
from pygame import freetype

pygame.freetype.init()

theme =[
#   [font, normal_text, background color, pressed button color, special text(not used)]
    ["mainfont.ttf", "white", "black", "ivory3", "azure4"], # dimgrey
    ["mainfont1.ttf", "white", "black", "ivory3", "azure4"] # dimgrey
]


colors = pygame.color.THECOLORS # all colors ( maybe ) in rgb shortcut
def rep(**args):
    global loop
    loop = False
def rep_setting(**args):
    global loop_setting
    loop_setting = False
    print(args)
    if args["done"] == 0:
        return
    if args["done"] == 1:
        pickle.dump(args["data"], open(args["save_main"].database, "wb" ))
        return
    if args["done"] == 2:
        pickle.dump(pickle.load(open(args["save_main"].default, "rb")), open(args["save_main"].database, "wb" ))
        return

def control_sound(save):
  pygame.mixer.music.set_volume(save.volume)
  if save.sound:
    pygame.mixer.music.unpause()
  else:
    pygame.mixer.music.pause()

def control(save_main):
  save = save_main.load()
  control_sound(save)

def settings(**args): # must to contain {"save":save, "save_main":save_main, "menu": bool, "back":surface, "theme_index":int, "fdir":string}
    global loop_setting
    save_main = args["save_main"]
    save = args["save"]
    from_menu = args["menu"]
    theme_choice = theme[args["theme_index"]]
    screen = pygame.display.set_mode(pygame.display.get_window_size())
    back = pygame.transform.scale(args["back"], screen.get_size())
    FONT_BIG = pygame.freetype.Font(args["fdir"]+theme_choice[0], 32)
    FONT = pygame.freetype.Font(args["fdir"]+theme_choice[0], 32)
    FONT_SMALL = pygame.freetype.Font(args["fdir"]+theme_choice[0], 24)
    center = (screen.get_width() // 2, screen.get_height() // 2 )
    loop_setting = True
    sound_text, rect_sound = FONT.render("Sound: ", theme_choice[3])
    volume_text, rect_volume = FONT.render("Volume: ", theme_choice[3])
    rect_sound.center = (center[0]/2, rect_volume.h*2)
    rect_volume.center = (center[0]/2, rect_volume.h*4)
    spinboxes = [
    [spinBox((rect_volume.right, rect_volume.centery), FONT, lenght=2, centered=True, state=pygame.mixer.music.get_volume(), step=0.01), pygame.mixer.music.set_volume],
    ]
    enable_sound = enableButton(rect_sound.right+20, rect_sound.centery, centered=True, state=save.sound)
    canc = ["cancel", rep_setting, {"save_main":save_main, "done":0}]
    save_button = ["save", rep_setting, {"save_main":save_main, "done":1, "data":save}]
    restore = ["restore default", rep_setting, {"save_main":save_main, "done":2}]
    while loop_setting:
        screen.blit(back, (0, 0))
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    rep_setting(**{"done":0})
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for sBox in spinboxes:
                    sBox[0](pygame.mouse.get_pos(), func=sBox[1])
                    sBox[0].draw(screen, theme_choice)
        save.sound = enable_sound.get_state()
        save.volume = spinboxes[0][0].state
        if not enable_sound.get_state():
            pygame.mixer.music.pause()
        if enable_sound.get_state():
            pygame.mixer.music.unpause()
        screen.blit(sound_text, rect_sound)
        screen.blit(volume_text, rect_volume)
        for sBox in spinboxes:
            sBox[0].draw(screen, theme_choice)
        enable_sound.draw(screen, theme_choice)
        button(screen, canc[0], center[0]/2, screen.get_height()-50, FONT, theme_choice, canc[2], func=canc[1], centered=True)
        button(screen, restore[0], center[0], screen.get_height()-140, FONT, theme_choice, restore[2], func=restore[1], centered=True)
        button(screen, save_button[0], center[0]*1.5, screen.get_height()-50, FONT, theme_choice, save_button[2], func=save_button[1], centered=True)
        pygame.display.flip()
        save_button = ["save", rep_setting, {"save_main":save_main, "done":1, "data":save.__dict__}]
    control(save_main)
    return
avail = True
def pause(screen, **args):# must to contain {"save":save, "save_main":save_main, "flags": python.locals, "theme_index":int, "fdir":string}
    global loop
    import cv2
    globals().update(args)
    control(save_main)
    pygame.display.flip()
    pygame.image.save(screen, "temp.jpeg")
    img = cv2.imread('temp.jpeg')
    blur = cv2.blur(img,(5,5))
    cv2.imwrite("temp.jpeg", blur)
    theme_choice = theme[theme_index]
    screen = pygame.display.set_mode(pygame.display.get_window_size())
    FONT_BIG = pygame.freetype.Font(fdir+theme_choice[0], 32)
    FONT = pygame.freetype.Font(fdir+theme_choice[0], 32)
    FONT_SMALL = pygame.freetype.Font(fdir+theme_choice[0], 24)
    center = (screen.get_width() // 2, screen.get_height() // 2 )
    back = pygame.transform.scale(pygame.image.load("temp.jpeg"), screen.get_size())
    menu_title, rect_menu = FONT.render("MENU", theme_choice[1])
    rect_menu.center = (screen.get_width()/2, rect_menu.h*2)
    avail = False
    loop = True
     
    butt = [
        ["Resume", rep, {}],
        ["Settings", settings, {"save":save, "save_main":save_main, "menu": False, "back":back, "theme_index":theme_index, "fdir":fdir}],
        ["Main Menu", restart, {}],
        ["quit", exit, {}],
    ]
    while loop:
        screen.blit(back, (0, 0))
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE and avail:
                    rep()
            if event.type == KEYUP:
                if event.key == K_ESCAPE and not avail:
                    avail = True
        for i in range(0, len(butt)):
            button(screen, butt[i][0], rect_menu.x-(rect_menu.w/4), rect_menu.h*((i+1)*4), FONT, theme_choice, butt[i][2], func=butt[i][1])
        screen.blit(menu_title, rect_menu)
        pygame.display.flip()
    del cv2
    pygame.display.set_mode(pygame.display.get_window_size(), flags)
    os.remove("temp.jpeg")
    return

def menu(**args): # must to contain {"img_DIR": python.locals, "theme_index":int, "fdir":string}
    global real_menu
    globals().update(args)
    control(save_main)
    theme_choice = theme[theme_index]

    screen = pygame.display.set_mode(pygame.display.get_window_size())

    FONT_BIG = pygame.freetype.Font(fdir+theme_choice[0], 32)
    FONT = pygame.freetype.Font(fdir+theme_choice[0], 32)
    FONT_SMALL = pygame.freetype.Font(fdir+theme_choice[0], 24)
    positions = [[32, 64], [32, 128], [32, 192]]
    if img_DIR:
        img = pygame.transform.scale(pygame.image.load(img_DIR+"splash.jpg"), (screen.get_width(), screen.get_height()))

        arrow_d = pygame.transform.scale(pygame.image.load(img_DIR+"arrow_d.png"), (140, 80))

        lines = ["Hello there!", "Welcome to the most pumped up game", "EVER!!!!"]
    
        first = True

        splash_init = False

        while splash_init:
            screen_dim = (screen.get_width(), screen.get_height())
            for event in pygame.event.get():
                if event.type == QUIT:
                    exit()
                if event.type == KEYDOWN and not first:
                    splash_init = False
            
            screen.blit(img, (0, 0))
            for line, pos in zip(lines, positions):
                text, rect = FONT.render(line, theme_choice[1])
                rect.topleft = pos
                screen.blit(text, rect)
                if first:
                    pygame.display.flip()
                    time.sleep(1)
            if first:
                arrd, rect_d = FONT_SMALL.render("press any key to continue...", theme_choice[1])
                rect_d.topleft = (positions[-1][0], (positions[-1][1]+64))
                pygame.display.flip()
            
            
            screen.blit(arrd, rect_d)
            screen.blit(arrow_d, (screen.get_width()-150, screen.get_height()-90))
            # screen.blit(img, (0, 0))
            first = False
            pygame.display.flip()
    text, rect = FONT_BIG.render("GAME START", colors[theme_choice[1]])
    rect.centerx = screen.get_width()/2
    buttons = [
        ["play!", run, {}],
        ["settings", settings, {"save":save, "save_main":save_main, "menu": True, "back":pygame.Surface((0, 0)), "theme_index":theme_index, "fdir":fdir}],
        ["info", None, {}],
        ["quit...", exit, {}]   
    ]
    real_menu = True
    while real_menu:
        screen.fill(colors[theme_choice[2]])
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
        screen.blit(text, rect)
        for i in range(0, len(buttons)): button(screen, buttons[i][0], 32, 128+(i*64), FONT, theme_choice, buttons[i][2], func=buttons[i][1])
        pygame.display.flip() # ivory3
    return 0
def button(screen, text, x, y, font, theme_choice, arg, radius=18, line=3, space=20, func=None, centered=False):
    global avail
    text, rect = font.render(text, theme_choice[1])
    rect_button = pygame.Rect(x, y, rect.w+space, rect.h+space)
    if centered:
        rect_button.center = (x, y) 
    rect.center = rect_button.center
    if not pygame.mouse.get_pressed()[0] and not avail:
        avail = True
    if rect_button.collidepoint(pygame.mouse.get_pos()):
        gl.draw.rrect(screen, colors[theme_choice[3]], rect_button, radius)
        if pygame.mouse.get_pressed()[0] and avail:
            print(arg)
            try:
                func(**arg)
            except TypeError:
                traceback.print_exc()
            avail = False
    
    else:
        gl.draw.rrect(screen, colors[theme_choice[3]], rect_button, radius, line)
    screen.blit(text, rect)

def run(**args):
    global real_menu
    real_menu = False
    return 
class enableButton:
    def __init__(self, x, y, width=50, height=20, centered=False, state=False):
        self.state = state
        self.rect = pygame.Rect(x, y, width, height)
        if centered:
            self.rect.center = (x, y)
        self.state = state
        self.avail = False
        
    def get_state(self):
        return self.state
    def draw(self, screen, theme_choice, radius=2, normal_width=4, func=None):
        if not pygame.mouse.get_pressed()[0] and not self.avail:
            self.avail = True
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            if pygame.mouse.get_pressed()[0] and self.avail:
                self.state = not self.state
                self.avail = False
        if not self.state:
            gl.draw.rrect(screen, (55,155,255), self.rect, radius, normal_width)
        if self.state:
            gl.draw.rrect(screen, colors[theme_choice[3]], self.rect, radius)

class spinBox:
    
    def __init__(self, position, font, limit=(0.0, 1.0), centered=False, state=0, step=1, lenght=1, scale_len=15):
        self.lenght = lenght
        self.scale_len = scale_len
        self.rect = pygame.Rect(position, (85+(self.lenght*self.scale_len), 60))
        if centered:
            self.rect.center = position
            self.rect.left = position[0]
        self.image = pygame.Surface(self.rect.size, SRCALPHA).convert_alpha()
        self.image.fill((0,0,0,0))

        self.buttonRects = [pygame.Rect(50+(self.lenght*self.scale_len),5,30,20),
                             pygame.Rect(50+(self.lenght*self.scale_len),35,30,20)]
        self.limit = limit
        self.state = state
        self.step = step
        self.state = round(self.state, self.lenght)
        self.font = font
    def draw(self, surface, theme):
        #Draw SpinBox onto surface
        textline = self.font.render(str(self.state), theme[1])

        self.image.fill((0,0,0,0))

        #increment button
        pygame.draw.rect(self.image, theme[3], self.buttonRects[0], 3)
        pygame.draw.polygon(self.image, (55,155,255), [(55+(self.lenght*self.scale_len),20), (65+(self.lenght*self.scale_len),8), (75+(self.lenght*self.scale_len),20)])
        #decrement button
        pygame.draw.rect(self.image, theme[3], self.buttonRects[1], 3)
        pygame.draw.polygon(self.image, (55+(self.lenght*10),155,255), [(55+(self.lenght*self.scale_len),40), (65+(self.lenght*self.scale_len),52), (75+(self.lenght*self.scale_len),40)])

        self.image.blit(textline[0], (5, (self.rect.height - textline[0].get_height()) // 2))

        surface.blit(self.image, self.rect)

    def increment(self):
        if self.limit[1]-self.step >= self.state: self.state += self.step
        self.state = round(self.state, self.lenght)

    def decrement(self):
        if self.limit[0]+self.step <= self.state: self.state -= self.step
        self.state = round(self.state, self.lenght)

    def __call__(self, position, func=None):
        #enumerate through all button rects
        for idx, btnR in enumerate(self.buttonRects):
            #create a new pygame rect with absolute screen position
            btnRect = pygame.Rect((btnR.topleft[0] + self.rect.topleft[0],
                                   btnR.topleft[1] + self.rect.topleft[1]), btnR.size)

            if btnRect.collidepoint(position):
                if idx == 0:
                    self.increment()
                else:
                    self.decrement()
                if func:
                    func(self.state)