from project import Capybara, Object, Total, Button
from project import generate, move, check_contact, read_records
import pytest, pygame, random

choice = random.choice
OBJECT_MAX = 3
FOOD_CHANCE = 1
OBSTACLE_CHANCE = 1
"""Possible positions of the capybara"""
swamp = [40, 190]
field = [40, 390]
orchard = [40, 600]
"""Initialization of obstacles/food"""
rock = []
kajman = []
trunk = []
apple = []
branch = []
hay = []
grass = []
hiacynth = []
for _ in range(OBJECT_MAX):
    rock.append(Object("Obstacles/bigrock.png", field, "obstacle"))
    kajman.append(Object("Obstacles/kajman.png", swamp, "obstacle"))
    trunk.append(Object("Obstacles/trunk.png", orchard, "obstacle"))
    apple.append(Object("Food/apple.png", orchard, "food"))
    branch.append(Object("Food/branch.png", orchard, "food"))
    hay.append(Object("Food/hay.png", field, "food"))
    grass.append(Object("Food/grass.png", field, "food"))
    hiacynth.append(Object("Food/hiacynth.png", swamp, "food"))
objects = [kajman, rock, trunk, apple, branch, hay, grass, hiacynth]


def test_Capybara():
    capybaras = []
    for _ in range(5):
        capybaras.append(Capybara())
    for capy in capybaras:
        assert capy.width == 96
        assert capy.height == 64

def test_Object():
    objects = []
    addresses = ["Food/apple.png", "Food/branch.png", "Obstacles/trunk.png"]
    places = [[700, 900], [700,300], [700,600]]
    types = ["obstacle", "food"]

    """testing initialization"""
    for _ in range(5):
        objects.append(Object(choice(addresses), choice(places), choice(types)))
    for object in objects:
        assert object.address in addresses
        assert object.position[1] in [places[0][1],places[1][1],places[2][1]]
        assert object.position[0] == 1500
        assert object.ismoving == False
        assert object.type in types

        """testing start method"""
        object.start()
        assert object.position[0] == 1400
        assert object.ismoving == True

        """testing move method"""
        for _ in range(100):
            object.move()
        assert object.position[0] == 400
        assert object.ismoving == True

        """testing stop method"""
        object.stop()
        assert object.position[0] == 1500
        assert object.ismoving == False

def test_Total():
    """testing initialization"""
    records = []
    for _ in range(5):
        records.append(Total())
    for record in records:
        assert record.movement == 0
        assert record.food_points == 0

        """testing add movement method"""
        for _ in range(3):
            record.add_movement()
        assert record.movement == 3
        assert record.food_points == 0

        """testing add food points method"""
        for _ in range(3):
            record.add_food_points()
        assert record.movement == 3
        assert record.food_points == 30

        """testing __str__ method"""
        assert str(record) == "33"

        """testing accessing the limit of the game"""
        for _ in range(9999):
            record.add_food_points()
        assert str(record) == "99999"

def test_Button():
    button = Button("exit.png", [100, 200], [300, 400])

    """testing display of properties"""
    assert button.width == 100
    assert button.height == 200
    assert button.position == [300, 400]
    assert button.rect == [(300, 400), (300, 600), (400, 600), (400, 400)]

    """testing check of mouse pointing"""
    assert button.pointed([350, 500]) == True
    assert button.pointed([400, 600]) == True
    assert button.pointed([200, 500]) == False
    assert button.pointed([375, 700]) == False

def test_generate():
    """generating the first object"""
    rock[0].start()
    rock_started = rock[0]
    rock[0].stop()
    assert generate(rock,objects)[0] == rock_started

    """not generating - object too close on the row"""
    for _ in range(10):
        rock[0].move()
    assert generate(rock,objects) == rock

    """generating the second object"""
    for _ in range(40):
        rock[0].move()
    rock[1].start()
    rock_started = rock[1]
    rock[1].stop()
    assert generate(rock,objects)[1] == rock_started

    """generating the third object"""
    for _ in range(50):
        rock[0].move()
        rock[1].move()
    rock[2].start()
    rock_started = rock[2]
    rock[2].stop()
    assert generate(rock,objects)[2] == rock_started

    for i in range(OBJECT_MAX):
        rock[i].stop

    """not generating - other object in column"""
    generate(rock,objects)
    generate(trunk,objects)
    assert generate(kajman, objects) == kajman

    """generating - object in other column moved"""
    for _ in range(30):
        rock[0].move()
    kajman[0].start()
    kajman_started = kajman[0]
    kajman[0].stop()
    assert generate(kajman, objects)[0] == kajman_started
    for object in objects:
        for i in range(OBJECT_MAX):
            object[i].stop()

def test_move():
    """testing non-moving object"""
    assert move(rock) == rock

    """testing moving object"""
    rock[0].start()
    rock[0].move()
    rock_moved = rock[0]
    rock[0].stop()
    rock_stopped = rock[0]
    rock[0].start()
    assert move(rock)[0] == rock_moved

    """testing stopping the object"""
    for _ in range(140):
        rock[0].move()
    assert move(rock)[0] == rock_stopped
    for object in objects:
        for i in range(OBJECT_MAX):
            object[i].stop()

def test_check_contact():
    capybara = Capybara()
    track = swamp

    """object on a different track"""
    assert check_contact(capybara, hay, track) == [False, -1]

    """object on the same track but not touching"""
    assert check_contact(capybara, hiacynth, track) == [False, -1]

    """object on the same track and touching"""
    hiacynth[0].start()
    for _ in range(127):
        hiacynth[0].move()
    assert check_contact(capybara, hiacynth, track) == [True, 0]

def test_read_records():
    """list of records < 10"""
    reader = [
        {"date":"0","dist_points":0,"food_points":0,"total_points":0},
    ]
    for i in range(6):
        reader.append({"date":str(int(reader[i]["date"])+1),
                       "dist_points":reader[i]["dist_points"]+1,
                       "food_points":reader[i]["food_points"]+1,
                       "total_points":reader[i]["total_points"]+1,
                       })
    assert read_records(reader) == reader[1:]

    """list of records > 10"""
    reader = [
        {"date":0,"dist_points":0,"food_points":0,"total_points":0},
    ]
    for i in range(13):
        reader.append({"date":str(int(reader[i]["date"])+1),
                       "dist_points":reader[i]["dist_points"]+1,
                       "food_points":reader[i]["food_points"]+1,
                       "total_points":reader[i]["total_points"]+1,
                       })
    assert read_records(reader) == reader[-10:]
