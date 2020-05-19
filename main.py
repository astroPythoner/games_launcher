import sys
import os
import json
import pygame
from joystickpins import joystickpins

width = 1000 # opening screen size
height = 750
background_color = (70, 70, 70)  # background color
font = pygame.font.match_font("arial") # choose font
scroll = [5,4]  # change between [5,4] and [4,5] to switch srolling direction
LIST_VIEW = "list view"
SIDE_VIEW = "side view"
ansicht = SIDE_VIEW

text_groessen = [30,20,15]
game_folder_path = os.path.dirname(os.path.realpath(__file__))

class Game:
    name = "Unnamed"
    description = ""
    type = "Game"
    players = "unknown"
    playable_with = ["unknown"]
    title_image = None
    trailer = None
    readme = {}
    folder = None

    def __init__(self,game_path):
        self.folder = game_path
        if os.path.isfile(os.path.join(game_path, "info.json")):
            with open(os.path.join(game_path, "info.json")) as f:
                data = json.load(f)
                if "name" in data: self.name = data["name"]
                if "description" in data: self.description = data["description"]
                if "type" in data: self.type = data["type"]
                if "players" in data: self.players = data["players"]
                if "playable with" in data: self.playable_with = data["playable with"]
        if os.path.isfile(os.path.join(game_path, "title_image.png")):
            self.title_image = pygame.image.load(os.path.join(game_path, "title_image.png"))
        if os.path.isfile(os.path.join(game_path, "trailer.MPG")):
            self.trailer = pygame.movie.Movie(os.path.join(game_path, "trailer.MPG"))
        if os.path.isfile(os.path.join(game_path, "README.md")):
            self.readme = {}
            with open(os.path.join(game_path, "README.md"),"r") as file:
                for line in file:
                    line = line.rstrip()
                    ueberschrift_num = 0
                    if line.startswith("#### "):
                        line = line[5:]
                        ueberschrift_num = 3
                    elif line.startswith("####"):
                        line = line[4:]
                        ueberschrift_num = 3
                    if line.startswith("### "):
                        line = line[4:]
                        ueberschrift_num = 3
                    elif line.startswith("###"):
                        line = line[3:]
                        ueberschrift_num = 3
                    if line.startswith("## "):
                        line = line[3:]
                        ueberschrift_num = 2
                    elif line.startswith("##"):
                        line = line[2:]
                        ueberschrift_num = 2
                    if line.startswith("# "):
                        line = line[2:]
                        ueberschrift_num = 1
                    elif line.startswith("#"):
                        line = line[1:]
                        ueberschrift_num = 1
                    if not line == "```" and not line == "***" and not line.startswith("![") and not "](" in line:
                        self.readme[line] = ueberschrift_num
                file.close()

    def __str__(self):
        return self.name+"\n"+self.description+"\n"+self.type+"\n"+self.players+"\n"+str(self.playable_with)+"\n"+self.folder+"\n"+str(self.readme)

def calculate_fit_size(width,height,max_width_faktor, max_height_faktor):
    # caltulate size so it fits to WIDTH and HEIGHT
    size = max_width_faktor * width
    if size / height > max_height_faktor:
        size = max_height_faktor * height
    return int(size)
def update_text_sizes(width,height):
    # Textgroessen
    text_groessen[0] = int(calculate_fit_size(width,height,0.041, 0.0625))
    text_groessen[1] = int(calculate_fit_size(width,height,0.027, 0.040625))
    text_groessen[2] = int(calculate_fit_size(width,height,0.02,  0.03125))
def draw_text(surf, text, x, y, size=text_groessen[1], font_name=font, color=(0,0,0), rect_place="oben_mitte"):
    font = pygame.font.Font(font_name, int(size))
    text_surface = font.render(str(text), True, color)
    text_rect = text_surface.get_rect()
    if rect_place == "oben_mitte":
        text_rect.midtop = (x, y)
    elif rect_place == "oben_links":
        text_rect.topleft = (x, y)
    elif rect_place == "oben_rechts":
        text_rect.topright = (x, y)
    elif rect_place == "mitte_rechts":
        text_rect.midright = (x, y)
    elif rect_place == "mitte_links":
        text_rect.midleft = (x, y)
    elif rect_place == "mitte":
        text_rect.center = (x, y)
    elif rect_place == "unten_mitte":
        text_rect.midbottom = (x, y)
    elif rect_place == "unten_rechts":
        text_rect.bottomright = (x, y)
    elif rect_place == "unten_links":
        text_rect.bottomleft = (x, y)
    else:
        print("rect_pos given to draw_text is not known")
    surf.blit(text_surface, text_rect)
    return text_rect
def draw_text_fitting_line_width(surf,text,width, x, y, size=text_groessen[1], font_name=font, color=(0,0,0)):
    # draws text but only into given width, if text is to big it breaks the line
    # return y pos of end of text
    # carful if with smaller than one letter this function is an endless loop
    unterkante = y
    rest_text = text
    font = pygame.font.Font(font_name, int(size))
    while rest_text != "":
        written_text = rest_text
        while True:
            text_surface = font.render(str(written_text), True, color)
            text_rect = text_surface.get_rect()
            if text_rect.width <= width:
                rect = draw_text(surf,written_text,x,unterkante+size/4,size,font_name,color,"oben_links")
                unterkante = rect.y+size
                rest_text = rest_text[len(written_text)+1:]
                break
            else:
                words = written_text.split(" ")
                if len(words) >= 1:
                    written_text = ""
                    for word in words[0:-1]:
                        written_text += word+" "
                written_text = written_text[:-1]
    return unterkante
def draw_readme(surf,text,width,x,y,size1=None,size2=None,size3=None,normal_size=None,font_name=font,color1=(0,0,0),color2=(0,0,0),color3=(0,0,0),normal_color=(0,0,0),line_color=(0,0,0)):
    if size1 is None:
        size1 = text_groessen[1]+(text_groessen[0]-text_groessen[1])*3/4
    if size2 is None:
        size2 = text_groessen[1]+(text_groessen[0]-text_groessen[1])*2/4
    if size3 is None:
        size3 = text_groessen[1]+(text_groessen[0]-text_groessen[1])*1/4
    if normal_size is None:
        normal_size = text_groessen[1]
    for line in text:
        if line == "***":
            pygame.draw.line(surf, line_color, (x, y + 5), (x + width, y + 5))
            y += 10
        else:
            y = draw_text_fitting_line_width(surf,line,width,x,y,[normal_size,size1,size2,size3][text[line]],font_name,[normal_color,color1,color2,color3][text[line]]) + normal_size/2
    if text == {} or text is None:
        y = draw_text_fitting_line_width(surf,"nicht vorhanden",width,x,y,normal_size,font_name,normal_color) + normal_size/2
    return y
def draw_game_info_on_surface(surface,game,y_scroll):
    y = y_scroll
    # infos aus info.json datei, die in der Game Klasse gespeichert sind
    y = draw_text_fitting_line_width(surface, game.name,                                        surface.get_width() - 20, 10, y, text_groessen[0], color=(250, 250, 250)) + text_groessen[0] / 2
    y = draw_text_fitting_line_width(surface, game.description,                                 surface.get_width() - 20, 10, y, text_groessen[1], color=(200, 200, 200)) + text_groessen[0]
    y = draw_text_fitting_line_width(surface, "Typ: " + game.type,                              surface.get_width() - 20, 10, y, text_groessen[1], color=(200, 200, 200)) + text_groessen[0] / 4
    y = draw_text_fitting_line_width(surface, "Spieler: " + game.players.replace("to", "bis"),  surface.get_width() - 20, 10, y, text_groessen[1], color=(200, 200, 200)) + text_groessen[0] / 4
    y = draw_text_fitting_line_width(surface, "Spielen mit: " +  ", ".join(game.playable_with), surface.get_width() - 20, 10, y, text_groessen[1], color=(200, 200, 200)) + text_groessen[0] / 4
    # Linie
    pygame.draw.line(surface, (200, 200, 200), (0, y+5), (surface.get_width(), y+5))
    y += 10 + text_groessen[1]
    # Readme
    y = draw_text_fitting_line_width(surface, "Readme:",                                        surface.get_width() - 20, 10, y, text_groessen[0], color=(250, 250, 250)) + text_groessen[0] / 2
    y = draw_readme(surface, game.readme, surface.get_width() - 20, 10, y, color1=(250, 225, 225), color2=(225, 200, 200), color3=(200, 175, 175), normal_color=(150, 150, 150), line_color=(200, 200, 200))
    return y - y_scroll - surface.get_height() + text_groessen[0]

def find_games(game_folder_path):
    games = []
    for folder in os.listdir(game_folder_path):
        game_path = os.path.join(game_folder_path, folder)
        if os.path.isfile(os.path.join(game_path, "main.py")):
            games.append(Game(game_path))
    return games
def start_game(game_path):
    if os.path.isfile(os.path.join(game_path, "main.py")):
        sys.path.insert(1, game_path)
        exec("from " + os.path.basename(game_path) + " import main")

def draw_side_view(screen,width,height,height_anzeige_auswahl,games,selected_game, y_scroll):
    buttons_for_mouse_klick = {}
    # side view
    for game_num_add in [-3,3,-2,2,-1,1,0]:
        game_num = selected_game+game_num_add
        if game_num >= 0 and game_num < len(games):
            game = games[game_num]
            image_height = int(height*(2/5) / [1,1.2,1.45,1.7][abs(game_num-selected_game)])
            image_width = int(image_height * 1.5)
            image_x = width/2-image_width/2+[-width/2.5,-width/3.2,-width/5.7,0,width/5.7,width/3.2,width/2.5][(game_num-selected_game+3)]
            image_y = height*2/10-image_height/2+10+height_anzeige_auswahl
            color = [255, 230, 200, 170][abs(game_num - selected_game)]/2.25
            rect = pygame.Rect(image_x, image_y, image_width, image_height)
            buttons_for_mouse_klick[game_num] = rect
            if game.title_image != None:
                title_image = pygame.transform.scale(game.title_image, (image_width,image_height))
                screen.blit(title_image,(image_x,image_y))
            else:
                try:
                    surface = screen.subsurface(rect)
                    surface.fill((color, color, color))
                    draw_text(surface,game.name,image_width/2,image_height/2, text_groessen[0]*[1,0.88,0.7,0.6][abs(game_num-selected_game)],rect_place="mitte")
                except ValueError:
                    pass
    # linie
    pygame.draw.line(screen,(200,200,200),(0,height*(2/5)+height/30+height_anzeige_auswahl),(width,height*(2/5)+height/30+height_anzeige_auswahl),2)
    # info
    surface = screen.subsurface(pygame.Rect(0, height*(2/5)+height/30+height_anzeige_auswahl, width, height-height*(2/5)-height/30-height_anzeige_auswahl))
    y = draw_game_info_on_surface(surface,games[selected_game],y_scroll)
    return y, buttons_for_mouse_klick
def draw_list_view(screen,width,height,height_anzeige_auswahl,games,selected_game,y_scroll):
    buttons_for_mouse_klick = {}
    # list view
    y_size_per_game = (height - height_anzeige_auswahl) / len(games)
    width_games = 0
    for count,game in enumerate(games):
        rect = draw_text(screen,game.name,10,count*y_size_per_game+y_size_per_game/2+height_anzeige_auswahl,int(min([height/len(games)*(4/5),text_groessen[0]])),color=(250,250,250),rect_place="mitte_links")
        if rect.width+20 > width_games:
            width_games = rect.width+20
    for count,game in enumerate(games):
        rect = pygame.Rect(0, count*y_size_per_game+height_anzeige_auswahl,width_games, y_size_per_game)
        buttons_for_mouse_klick[count] = rect
        if count == selected_game:
            rect = pygame.Surface((width_games, y_size_per_game))
            rect.set_alpha(128)
            rect.fill((200, 200, 200))
            screen.blit(rect, (0, selected_game*y_size_per_game+height_anzeige_auswahl))
    for game in range(1,len(games)):
        pygame.draw.line(screen,(200,200,200),(0,game*y_size_per_game+height_anzeige_auswahl),(width_games,game*y_size_per_game+height_anzeige_auswahl))
    # linie
    pygame.draw.line(screen,(250,250,250),(width_games,height_anzeige_auswahl),(width_games,height),2)
    # bild
    if games[selected_game].title_image != None:
        image_width = int(width - width_games - 6)
        image_height = int(image_width / 1.5)
        if image_height > (height-height_anzeige_auswahl)*2/5:
            image_height = int((height-height_anzeige_auswahl)*2/5)
            image_width = int(image_height * 1.5)
        title_image = pygame.transform.scale(games[selected_game].title_image, (image_width, image_height))
        screen.blit(title_image, (int(width_games+(width-width_games-image_width)/2), height_anzeige_auswahl))
    # info
    if games[selected_game].title_image != None:
        surface = screen.subsurface(pygame.Rect(width_games, image_height+height_anzeige_auswahl, width-width_games, height-image_height-height_anzeige_auswahl))
    else:
        surface = screen.subsurface(pygame.Rect(width_games, height_anzeige_auswahl, width-width_games, height-height_anzeige_auswahl))
    y = draw_game_info_on_surface(surface, games[selected_game], y_scroll)
    return y,buttons_for_mouse_klick

def draw_anzeige_auswahl(surf,width,height):
    pygame.draw.line(surf,(230,100,100),(0,height),(width,height))
    draw_text(surf, "Listenansicht",width*(1/4),height/2,size=min([height*(5/8),text_groessen[0]]),color=(230,100,100),rect_place="mitte")
    draw_text(surf, "Seitenansicht",width*(3/4),height/2,size=min([height*(5/8),text_groessen[0]]),color=(230,100,100),rect_place="mitte")

if __name__ == '__main__':
    games = find_games(game_folder_path)

    selected_game = 0
    y_scroll = 0

    pygame.init()
    screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
    pygame.display.set_caption("Games with python and pygame")
    screen.fill((60,60,60))
    clock = pygame.time.Clock()

    all_joysticks = []
    for joy in range(pygame.joystick.get_count()):
        pygame_joystick = pygame.joystick.Joystick(joy)
        pygame_joystick.init()
        my_joystick = joystickpins.JoystickPins(pygame_joystick)
        print("adding joystick " + my_joystick.get_name())
        all_joysticks.append(my_joystick)

    while True:
        # draw
        screen.fill(background_color)
        height_anzeige_auswahl = height/20
        max_y_scroll = height
        mouse_buttons = {}
        if ansicht == SIDE_VIEW:
            max_y_scroll,mouse_buttons = draw_side_view(screen,width,height,height_anzeige_auswahl,games,selected_game,y_scroll)
        elif ansicht == LIST_VIEW:
            max_y_scroll,mouse_buttons = draw_list_view(screen,width,height,height_anzeige_auswahl,games,selected_game,y_scroll)
        draw_anzeige_auswahl(screen,width,height_anzeige_auswahl)
        pygame.display.flip()

        # events
        events = pygame.event.get()
        for event in events:
            # schließen
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                quit()
            # auswählen
            if event.type == pygame.KEYDOWN and (event.key == pygame.K_RIGHT or event.key == pygame.K_DOWN):
                y_scroll = 0
                selected_game += 1
                if selected_game >= len(games): selected_game = len(games)-1
            if event.type == pygame.KEYDOWN and (event.key == pygame.K_LEFT or event.key == pygame.K_UP):
                y_scroll = 0
                selected_game -= 1
                if selected_game < 0: selected_game = 0
            # scrollen oder klicken
            if event.type == pygame.MOUSEBUTTONDOWN:
                # klicken
                if event.button == 1:
                    pos = pygame.mouse.get_pos()
                    if pos[1] <= height_anzeige_auswahl:
                        if pos[0] <= width/2:
                            ansicht = LIST_VIEW
                        else:
                            ansicht = SIDE_VIEW
                    else:
                        for button in mouse_buttons:
                            if mouse_buttons[button].collidepoint(pos):
                                selected_game = button
                # scrollen
                elif event.button == scroll[0]:
                    y_scroll -= 50
                    if y_scroll < -max_y_scroll: y_scroll = -max_y_scroll
                elif event.button == scroll[1]:
                    y_scroll += 50
                    if y_scroll > 0: y_scroll = 0
            # starten
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                pygame.quit()
                start_game(games[selected_game].folder)
            # window resize
            if event.type == pygame.VIDEORESIZE:
                width = event.w
                height = event.h
                if width < 200: width=200
                if height < 150: height=150
                update_text_sizes(width,height)
                screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
        for joystick in all_joysticks:
            # schließen
            if joystick.get_start() and joystick.get_select():
                quit()
            # auswählen
            if joystick.get_axis_left():
                y_scroll = 0
                selected_game -= 1
                if selected_game < 0: selected_game = 0
            if joystick.get_axis_right():
                y_scroll = 0
                selected_game += 1
                if selected_game >= len(games): selected_game = len(games) - 1
            # ansicht wählen
            if joystick.get_shoulder_left():
                ansicht = LIST_VIEW
            if joystick.get_shoulder_right():
                ansicht = SIDE_VIEW
            # scrollen
            if joystick.get_axis_up():
                y_scroll -= 50
                if y_scroll < -max_y_scroll: y_scroll = -max_y_scroll
            if joystick.get_axis_down():
                y_scroll += 50
                if y_scroll > 0: y_scroll = 0
            # starten
            if joystick.get_B() or joystick.get_A():
                pygame.quit()
                start_game(games[selected_game].folder)