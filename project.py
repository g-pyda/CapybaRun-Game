"""CAPYBARUN - the game"""

import sys, pygame, random, csv, datetime
"""Environmental variables"""
BLACK = 0, 0, 0
WHITE = 255, 255, 255
OBJECT_MAX = 3
WIDTH = 1500
HEIGHT = 750
SCORE_LEN = 5
FOOD_CHANCE = 20
OBSTACLE_CHANCE = 5
BUTTON_SIZE = [300, 75]
BUTTON_BORDER_WIDTH = 5

RECORD_FIELDS = ["date","dist_points","food_points","total_points"]
RECORDS_ADDRESS = "./Records/records.csv"
RECORDS_FILE_READ = open(RECORDS_ADDRESS)
RECORDS_FILE_APPEND = open("./Records/records.csv", "a", newline="\n")

pygame.font.init()
FONT = pygame.font.Font("./Fonts/Minecraft.ttf", size=24)
FONT_BIG = pygame.font.Font("./Fonts/Minecraft.ttf", size=48)

class Capybara:
    def __init__(self):
        self._width = 96
        self._height = 64
        try:
            self._pic1 = pygame.image.load("./Pictures/Capybara/capybara1.png")
        except FileNotFoundError:
            sys.exit("\"capybara1.png\" from Capybara not found!")
        try:
            self._pic2 = pygame.image.load("./Pictures/Capybara/capybara2.png")
        except FileNotFoundError:
            sys.exit("\"capybara2.png\" from Capybara not found!")
        try:
            self._pic3 = pygame.image.load("./Pictures/Capybara/capybara3.png")
        except FileNotFoundError:
            sys.exit("\"capybara3.png\" from Capybara not found!")

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    @property
    def pic1(self):
        return self._pic1

    @property
    def pic2(self):
        return self._pic2
    
    @property
    def pic3(self):
        return self._pic3

class Object:
    def __init__(self, address, place, type):
        self._width = 64
        self._height = 64
        try:
            self._pic = pygame.image.load(f"./Pictures/{address}")
        except FileNotFoundError:
            sys.exit(f"\"{address}\" from Obstacles/Food not found!")
        if type == "food" or type == "obstacle":
            self._type = type
        self._place = place
        self._position = [1500, place[1]]
        self._ismoving = False
        self._address = address

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    @property
    def place(self):
        return self._place

    @property
    def pic(self):
        return self._pic

    @property
    def address(self):
        return self._address

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, list):
        if -100 < list[0] < 1600 and -100 < list[1] < 1600:
            self._position = [list[0], list[1]]
        else: raise ValueError

    @property
    def type(self):
        return self._type

    @property
    def ismoving(self):
        return self._ismoving

    def start(self):
        self.position = [1400, self.position[1]]
        self._ismoving = True

    def stop(self):
        self.position = [1500, self.position[1]]
        self._ismoving = False

    def move(self):
        if self.ismoving:
            self.position = [self.position[0] - 10, self.position[1]]

class Total:
    def __init__(self):
        self._movement = 0
        self._food_points = 0

    @property
    def movement(self):
        return self._movement

    def add_movement(self):
        self._movement += 1

    @property
    def food_points(self):
        return self._food_points

    def add_food_points(self):
        self._food_points += 10

    def __str__(self):
        total = self.movement + self.food_points
        if total >= 99999: total = 99999
        return str(total)

class Button:
    def __init__(self, address, size, position):
        try:
            self._pic = pygame.image.load(f"./Pictures/Buttons/{address}")
        except FileNotFoundError:
            sys.exit(f"\"{address}\" from Buttons not found!")
        self._position = position
        self._size = size
        self._picname = address

    @property
    def width(self):
        return self._size[0]

    @property
    def height(self):
        return self._size[1]
    
    @property
    def picname(self):
        return self._picname

    @property
    def rect(self):
        leftTop = (self.position[0],self.position[1])
        leftBot = (self.position[0],self.position[1] + self.height)
        rightTop = (self.position[0] + self.width ,self.position[1])
        rightBot = (self.position[0] + self.width, self.position[1] + self.height)
        return [leftTop, leftBot, rightBot, rightTop]

    @property
    def pic(self):
        return self._pic

    @property
    def position(self):
        return self._position

    def border(self, screen):
        pygame.draw.lines(screen, WHITE, True, self.rect, width=BUTTON_BORDER_WIDTH)

    def pointed(self, mouse):
        if self.position[0] <= mouse[0] <= self.position[0] + self.width:
            if self.position[1] <= mouse[1] <= self.position[1] + self.height:
                return True
            else: return False
        else: return False

class Background:
    def __init__(self, address):
        try:
            self._pic = pygame.image.load(f"./Pictures/Backgrounds/{address}")
        except FileNotFoundError:
            sys.exit(f"\"{address}\" from Backgrounds not found!")
        self._picname = address

    @property
    def picname(self):
        return self._picname
    @property
    def pic(self):
        return self._pic

def main():
    """Initializing the game and it's parameters"""
    pygame.init()
    pygame.font.init()

    size = WIDTH, HEIGHT
    screen = pygame.display.set_mode(size)

    pygame.mouse.set_cursor(*pygame.cursors.arrow)
    main_menu(screen)

def main_menu(screen):
    """Initializing buttons and the background"""
    start_but = Button("start.png", BUTTON_SIZE, (750, 350))
    records_but = Button("records.png", BUTTON_SIZE, (750, 475))
    exit_but = Button("exit.png", BUTTON_SIZE, (750, 600))
    main_back = Background("main.png")

    while True:

        """Quitting the game"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit("Thank you for using the game!")
        """Displaying the page"""
        screen.fill(BLACK)
        screen.blit(main_back.pic,(0, 0))
        for button in [start_but, records_but, exit_but]:
            screen.blit(button.pic, button.position)

        position = pygame.mouse.get_pos()
        """Pointing the buttons and action"""
        if start_but.pointed(position): #start button pointed
            start_but.border(screen)
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    game(screen)
        elif records_but.pointed(position): #records button pointed
            records_but.border(screen)
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    records(screen)
        elif exit_but.pointed(position): #exit button pointed
            exit_but.border(screen)
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    sys.exit("Thank you for using the game!")
        pygame.display.flip()

def game(screen):
    """Possible positions of the capybara"""
    swamp = [40, 190]
    field = [40, 390]
    orchard = [40, 600]
    track = field
    """Initializing the score, speed (time of change in frames)"""
    distance = 0
    points = Total()
    """Initializing the background and the capybara"""
    game_back = Background("game.png")
    capybara = Capybara()
    """Initialization of obstacles/food"""
    rock = []
    kajman = []
    trunk = []
    apple = []
    branch = []
    hay = []
    grass = []
    hiacynth = []
    try:
        for _ in range(OBJECT_MAX):
            rock.append(Object("Obstacles/bigrock.png", field, "obstacle"))
            kajman.append(Object("Obstacles/kajman.png", swamp, "obstacle"))
            trunk.append(Object("Obstacles/trunk.png", orchard, "obstacle"))
            apple.append(Object("Food/apple.png", orchard, "food"))
            branch.append(Object("Food/branch.png", orchard, "food"))
            hay.append(Object("Food/hay.png", field, "food"))
            grass.append(Object("Food/grass.png", field, "food"))
            hiacynth.append(Object("Food/hiacynth.png", swamp, "food"))
    except FileNotFoundError:
        sys.exit("At least one of the object (obstacle/food) files is missing!")

    while True:
        """Quitting the game"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit("Thank you for using the game!")
        """Entering the menu"""
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            menu(screen, capybara, [kajman, rock, trunk, apple, branch, hay, grass, hiacynth], distance, track)

        """Displaying the page"""
        screen.fill(BLACK)
        screen.blit(game_back.pic,(0, 0))
        pygame.font.init()
        points_text = str(points)
        if SCORE_LEN - len(points_text) == 4:
            points_text = "0000"+ points_text
        elif SCORE_LEN - len(points_text) == 3:
            points_text = "000"+ points_text
        elif SCORE_LEN - len(points_text) == 2:
            points_text = "00"+ points_text
        elif SCORE_LEN - len(points_text) == 1:
            points_text = "0"+ points_text
        score_text = FONT_BIG.render(points_text, True, WHITE, None)
        screen.blit(score_text, [1250, 30])

        """Generating the obstacles and food"""
        for object in [kajman, rock, trunk, apple, branch, hay, grass, hiacynth]:
            if distance%5 == 0:
                object = generate(object, [kajman, rock, trunk, apple, branch, hay, grass, hiacynth])
                object = move(object)
            for i in range(OBJECT_MAX):
                screen.blit(object[i].pic,object[i].position)

        """Movement of the capybara and display"""
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                if track == orchard: track = field
                elif track == field: track = swamp
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                if track == swamp: track = field
                elif track == field: track = orchard
        if distance%40 < 10:
            screen.blit(capybara.pic1,track)
        elif distance%40 < 20:
            screen.blit(capybara.pic3,track)
        elif distance%40 < 30:
            screen.blit(capybara.pic2,track)
        else:
            screen.blit(capybara.pic3,track)

        """Actualisation of the surface"""
        pygame.display.flip()

        """Checking of the contact with the obstacles and food"""
        for object in [kajman, rock, trunk, apple, branch, hay, grass, hiacynth]:
            yummy = [False, -1]
            over = [False, -1]
            if object[0].type == "obstacle": over = check_contact(capybara, object, track)
            elif object[0].type == "food": yummy = check_contact(capybara, object, track)
            if over[0] == True or int(str(points)) >= 99999:
                with open(RECORDS_ADDRESS, "a") as records:
                    writer = csv.DictWriter(records, fieldnames=RECORD_FIELDS)
                    save_record(writer, points)
                game_over(screen, capybara, [kajman, rock, trunk, apple, branch, hay, grass, hiacynth], distance, track, score_text)
            if yummy[0] == True:
                points.add_food_points()
                object[yummy[1]].stop()

        """Actualization of the score"""
        distance += 1
        if distance%10 == 0 and distance != 0: points.add_movement()

def generate(to_generate, objects):
    object = to_generate
    """Looking for objects in the same row"""
    for other in objects:
        if other[0].position[1] == object[0].position[1]:
            for i in range(OBJECT_MAX):
                if 1200 <= other[i].position[0] < 1500: return object
    """Looking for objects in column (obstacles only) """
    if object[0].type == "obstacle":
        aligned = 0
        for other in objects:
            if other[0].type == "obstacle" and other[0].position[1] != object[0].position[1]:
                for i in range(OBJECT_MAX):
                    if 1000 < other[i].position[0] < 1500: aligned += 1
        if aligned > 1: return object
    """Generating the object"""
    if object[0].type == "food": chance = FOOD_CHANCE
    else: chance = OBSTACLE_CHANCE
    if object[0].ismoving == False:
        if (random.choice(range(100))%chance) == 0:
            object[0].start()
    elif object[0].ismoving == True and object[1].ismoving == False:
        if (random.choice(range(100))%chance) == 0:
            object[1].start()
    elif object[0].ismoving == True and object[1].ismoving == True and object[2].ismoving == False:
        if (random.choice(range(100))%chance) == 0:
            object[2].start()

    return object

def move(object):
    for i in range(OBJECT_MAX):
        if -70 < object[i].position[0] < 1500 and object[i].ismoving == True :
            object[i].move()
        if -70 >= object[i].position[0]:
             object[i].stop()
    return object

def check_contact(capybara, object, track):
    if object[0].position[1] != track[1]: return [False,-1]
    for i in range(OBJECT_MAX):
        if 40 - object[i].width <= object[i].position[0] <= 40 + capybara.width: return [True,i]
    return [False, -1]

def game_over(screen, capybara, objects, distance, track, score_text):
    """Initializing buttons and the background"""
    game_back = Background("game.png")
    try_but = Button("try_again.png", BUTTON_SIZE, [600, 325])
    main_but = Button("main_menu.png", BUTTON_SIZE, [600, 425])
    records_but = Button("records.png", BUTTON_SIZE, [600, 525])
    exit_but = Button("exit.png", BUTTON_SIZE, [600, 625])
    over_back = Background("game_over.png")

    while True:

        """Quitting the game"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit("Thank you for using the game!")
        """Displaying the page"""
        screen.fill(BLACK)
        screen.blit(game_back.pic,(0, 0))
        for object in objects:
            for i in range(OBJECT_MAX):
                screen.blit(object[i].pic,object[i].position)
        if distance%20 < 10:
            screen.blit(capybara.pic1,track)
        else:
            screen.blit(capybara.pic2,track)
        screen.blit(over_back.pic,(0, 0))
        for button in [try_but,records_but,main_but,exit_but]:
            screen.blit(button.pic, button.position)
        screen.blit(score_text, [780, 240])
        position = pygame.mouse.get_pos()
        """Pointing the buttons and action"""
        if try_but.pointed(position): #try_again button pointed
            try_but.border(screen)
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    game(screen)
        elif main_but.pointed(position): #main button pointed
            main_but.border(screen)
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    main_menu(screen)
        elif records_but.pointed(position): #records button pointed
            records_but.border(screen)
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    records(screen)
        elif exit_but.pointed(position): #exit button pointed
            exit_but.border(screen)
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    sys.exit("Thank you for using the game!")
        pygame.display.flip()

def records(screen):
    """Initializing the background and the buttons"""
    records_back = Background("records.png")
    exit_but = Button("exit.png", BUTTON_SIZE, [300, 650])
    main_but = Button("main_menu.png", BUTTON_SIZE, [900, 650])

    """Opening records file"""
    with open(RECORDS_ADDRESS) as records:
        reader = csv.DictReader(records, fieldnames=RECORD_FIELDS)
        record_list = read_records(reader)

        while True:

            """Quitting the game"""
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    records.close()
                    sys.exit("Thank you for using the game!")
            """Displaying the page"""
            screen.fill(BLACK)
            screen.blit(records_back.pic,(0, 0))
            for button in [main_but, exit_but]:
                screen.blit(button.pic, button.position)

            position = pygame.mouse.get_pos()
            """Pointing the buttons and action"""
            if main_but.pointed(position): #main button pointed
                main_but.border(screen)
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        records.close()
                        main_menu(screen)
            elif exit_but.pointed(position): #exit button pointed
                exit_but.border(screen)
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        records.close()
                        sys.exit("Thank you for using the game!")

            """Displaying the score (the last 10 games)"""
            pygame.font.init()
            headers = ["DATE:", "DISTANCE POINTS:", "FOOD POINTS:", "TOTAL:"]
            for i in range(len(RECORD_FIELDS)):
                Header = FONT.render(headers[i], True, (39, 39, 54), None)
                position = [80 + i*350, 220]
                screen.blit(Header, position)
            i = 0
            for record in record_list:
                a = 0
                for field in RECORD_FIELDS:
                    Record = FONT.render(record[field], True, (39, 39, 54), None)
                    position = [90 + a*350, 285 + i*30]
                    screen.blit(Record, position)
                    a += 1
                i += 1
            pygame.display.flip()

def menu(screen, capybara, objects, distance, track):
    """Initializing buttons and the background"""
    game_back = Background("game.png")
    resume_but = Button("resume.png", BUTTON_SIZE, [600, 250])
    main_but = Button("main_menu.png", BUTTON_SIZE, [600, 350])
    records_but = Button("records.png", BUTTON_SIZE, [600, 450])
    exit_but = Button("exit.png", BUTTON_SIZE, [600, 550])
    menu_back = Background("menu.png")

    while True:

        """Quitting the game"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit("Thank you for using the game!")
        """Displaying the page"""
        screen.fill(BLACK)
        screen.blit(game_back.pic,(0, 0))
        for object in objects:
            for i in range(OBJECT_MAX):
                screen.blit(object[i].pic,object[i].position)
        if distance%20 < 10:
            screen.blit(capybara.pic1,track)
        else:
            screen.blit(capybara.pic2,track)
        screen.blit(menu_back.pic,(0, 0))
        for button in [resume_but, records_but, main_but, exit_but]:
            screen.blit(button.pic, button.position)

        position = pygame.mouse.get_pos()
        """Entering thr menu"""
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            return None
        """Pointing the buttons and action"""
        if resume_but.pointed(position): #resume button pointed
            resume_but.border(screen)
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    return None
        elif main_but.pointed(position): #main button pointed
            main_but.border(screen)
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    main_menu(screen)
        elif records_but.pointed(position): #records button pointed
            records_but.border(screen)
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    records(screen)
        elif exit_but.pointed(position): #exit button pointed
            exit_but.border(screen)
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    sys.exit("Thank you for using the game!")
        pygame.display.flip()

def save_record(records, points):
    date = datetime.datetime.now()
    records.writerow({"date": date, "dist_points":points.movement, "food_points":points.food_points, "total_points":str(points)})

def read_records(reader):
    last_10 = []
    reader_list = list(reader)
    i = len(reader_list)
    if 0 <= i <= 11:
        for row in reader_list[1:]:
            last_10.append({
                "date":(row["date"])[:19],
                "dist_points":row["dist_points"],
                "food_points":row["food_points"],
                "total_points":row["total_points"]
                })
    else:
        for row in reader_list[-10:]:
            last_10.append({
                "date":(row["date"])[:19],
                "dist_points":row["dist_points"],
                "food_points":row["food_points"],
                "total_points":row["total_points"]})
    return last_10

if __name__ == "__main__":
    main()
