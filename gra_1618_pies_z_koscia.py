import turtle
import random
import math
import time
import os

WORLD_SIZE = 300


class World:
    def __init__(self, size):
        self._size = size
        self._elements = []

    def add_element(self, element):
        self._elements.append(element)

    def get_size(self):
        return self._size

    def is_inside(self, x, y):
        if abs(x) > self._size // 2:
            return False
        if abs(y) > self._size // 2:
            return False
        return True

    def get_elements(self):
        return self._elements


class WorldElement:
    def __init__(self, name):
        self._name = name

    def get_name(self):
        return self._name


class Mud(WorldElement):
    def __init__(self):
        WorldElement.__init__(self, "Bloto")

    def activate(self, dog):
        dog.add_fatigue(15)
        dog.add_event("Pies wpadl w glebokie bloto (+15 zmeczenia)")
        print("[ELEMENT SWIATA] Pies wpadl w glebokie bloto.")
        print("Zmeczenie wzrasta o 15.")


class WaterPuddle(WorldElement):
    def __init__(self):
        WorldElement.__init__(self, "Kaluza")

    def activate(self, dog):
        dog.add_fatigue(-20)
        dog.add_item("woda")
        dog.add_event("Znaleziono kaluze z czysta woda")
        print("[ELEMENT SWIATA] Pies znalazl kaluze czystej wody.")
        print("Zmeczenie spada o 20 i otrzymujesz wode.")


class TreatBush(WorldElement):
    def __init__(self):
        WorldElement.__init__(self, "Krzak")

    def activate(self, dog):
        dog.add_fatigue(-10)
        dog.add_item("smaczki")
        dog.add_event("Znaleziono krzak pelen smaczkow")
        print("[ELEMENT SWIATA] Krzak byl pelen przysmakow.")
        print("Otrzymujesz smaczka i odzyskujesz 10 energii.")


class RestPlace(WorldElement):
    def __init__(self):
        WorldElement.__init__(self, "Odpoczynek")

    def activate(self, dog):
        dog.add_fatigue(-25)
        dog.add_event("Odpoczynek pod drzewem")
        print("[ELEMENT SWIATA] Pies odpoczal pod drzewem.")
        print("Zmeczenie spada o 25.")


class Bone:
    def __init__(self, world_size):
        self._x = random.randint(-world_size // 2 + 20, world_size // 2 - 20)
        self._y = random.randint(-world_size // 2 + 20, world_size // 2 - 20)

    def get_x(self):
        return self._x

    def get_y(self):
        return self._y


class Dog:
    def __init__(
            self,
            name,
            breed,
            start_x,
            start_y,
            fatigue,
            max_fatigue
    ):
        self._name = name
        self._breed = breed
        self._x = start_x
        self._y = start_y
        self._fatigue = fatigue
        self._max_fatigue = max_fatigue

        self._distance = 0
        self._history = []

        self._inventory = {
            "kosci": 0,
            "smaczki": 0,
            "woda": 0
        }

        self._turtle = turtle.Turtle()
        self._turtle.shape("turtle")
        self._turtle.color("brown")
        self._turtle.penup()
        self._turtle.goto(self._x, self._y)
        self._turtle.pendown()

    def add_event(self, event):
        self._history.append(event)

    def get_history(self):
        return self._history

    def get_name(self):
        return self._name

    def get_breed(self):
        return self._breed

    def get_x(self):
        return self._x

    def get_y(self):
        return self._y

    def get_fatigue(self):
        return self._fatigue

    def get_max_fatigue(self):
        return self._max_fatigue

    def get_distance(self):
        return self._distance

    def get_inventory(self):
        return self._inventory

    def move(self, azimuth, steps):
        angle_rad = math.radians(90 - azimuth)

        x_change = math.cos(angle_rad)
        y_change = math.sin(angle_rad)

        self._turtle.setheading(azimuth)

        for _ in range(steps):
            self._x += x_change
            self._y += y_change
            self._distance += 1

            self._turtle.goto(self._x, self._y)

            turtle.Screen().update()
            time.sleep(0.005)

    def add_fatigue(self, value):
        self._fatigue += value

        if self._fatigue < 0:
            self._fatigue = 0

        if self._fatigue > self._max_fatigue:
            self._fatigue = self._max_fatigue

    def add_item(self, item):
        if item in self._inventory:
            self._inventory[item] += 1

    def use_item(self, item):
        if item not in self._inventory:
            return False

        if self._inventory[item] <= 0:
            return False

        self._inventory[item] -= 1

        if item == "smaczki":
            self.add_fatigue(-10)
            self.add_event("Zuzyto smaczka")

        if item == "woda":
            self.add_fatigue(-15)
            self.add_event("Wypito wode")

        return True

    def clear(self):
        self._turtle.clear()
        self._turtle.hideturtle()


class GameVisualizer:
    def __init__(self):
        self._drawer = turtle.Turtle()

        self._drawer.hideturtle()
        self._drawer.speed(0)

        self._hud = turtle.Turtle()

        self._hud.hideturtle()
        self._hud.penup()

    def draw_world(self):
        self._drawer.clear()

        self._drawer.penup()
        self._drawer.goto(
            -WORLD_SIZE / 2,
            -WORLD_SIZE / 2
        )

        self._drawer.pendown()
        self._drawer.color("red")

        for _ in range(4):
            self._drawer.forward(WORLD_SIZE)
            self._drawer.left(90)

    def draw_house(self, x, y):
        marker = turtle.Turtle()

        marker.hideturtle()
        marker.speed(0)

        marker.penup()
        marker.goto(x - 8, y - 8)

        marker.pendown()

        marker.begin_fill()

        for _ in range(4):
            marker.forward(16)
            marker.left(90)

        marker.end_fill()

        marker.penup()
        marker.goto(x - 10, y + 8)

        marker.pendown()

        marker.begin_fill()

        for _ in range(3):
            marker.forward(20)
            marker.left(120)

        marker.end_fill()

        return marker

    def draw_marker(self, x, y, color, shape):
        marker = turtle.Turtle()

        marker.shape(shape)
        marker.color(color)

        marker.penup()
        marker.goto(x, y)

        return marker

    def update_hud(self, dog):
        self._hud.clear()

        self._hud.goto(
            -WORLD_SIZE // 2 - 120,
            WORLD_SIZE // 2 - 40
        )

        inventory = dog.get_inventory()

        self._hud.write(
            f"Pies: {dog.get_name()} ({dog.get_breed()})\n"
            f"X: {round(dog.get_x())}\n"
            f"Y: {round(dog.get_y())}\n"
            f"Zmeczenie: {dog.get_fatigue()}/{dog.get_max_fatigue()}\n"
            f"Smaczki: {inventory['smaczki']}\n"
            f"Woda: {inventory['woda']}",
            font=("Courier", 10, "bold")
        )


def get_input(prompt, cast_type, default, validator=None):
    turtle.getcanvas().winfo_toplevel().update()

    while True:
        user_input = input(prompt).strip()

        if user_input == "":
            print(f"Przyjeto wartosc domyslna: {default}")
            return default

        try:
            value = cast_type(user_input)

            if validator is not None:
                if not validator(value):
                    print("Wartosc poza zakresem.")
                    continue

            return value

        except ValueError:
            print("Niepoprawna wartosc.")


def random_world_element(dog):
    chance = random.randint(1, 100)

    if chance <= 15:
        Mud().activate(dog)

    elif chance <= 30:
        WaterPuddle().activate(dog)

    elif chance <= 45:
        TreatBush().activate(dog)

    elif chance <= 55:
        RestPlace().activate(dog)


def random_event(dog):
    chance = random.randint(1, 100)

    if chance <= 10:
        move_x = random.randint(-15, 15)
        move_y = random.randint(-15, 15)

        dog._x += move_x
        dog._y += move_y

        dog.add_event("Silny wiatr zmienil pozycje psa")

        print("[ZDARZENIE LOSOWE]")
        print("Silny wiatr zepchnal psa z kursu.")
        print(f"Przesuniecie: ({move_x}, {move_y})")

    elif chance <= 20:
        dog.add_fatigue(10)

        dog.add_event("Szczekajacy pies zwiekszyl zmeczenie")

        print("[ZDARZENIE LOSOWE]")
        print("W oddali szczekal inny pies.")
        print("Zmeczenie wzrasta o 10.")

    elif chance <= 28:
        dog.add_item("smaczki")

        dog.add_event("Znaleziono porzuconego smaczka")

        print("[ZDARZENIE LOSOWE]")
        print("Na ziemi lezal porzucony smaczek.")
        print("Dodano smaczka do ekwipunku.")

    elif chance <= 35:
        dog.add_fatigue(-15)

        dog.add_event("Wlasciciel podal miske wody")

        print("[ZDARZENIE LOSOWE]")
        print("Wlasciciel podal miske wody.")
        print("Zmeczenie spada o 15.")


def choose_breed():
    print()
    print("Wybierz rase psa:")
    print("1 - Nova Scotia Duck Tolling Retriever")
    print("2 - Owczarek Belgijski")
    print("3 - Samoyed")
    print("4 - Chart")
    print()

    choice = get_input(
        "Numer rasy (1-4, domyslnie 3): ",
        int,
        3,
        lambda x: 1 <= x <= 4
    )

    breeds = {
        1: ("Nova Scotia Duck Tolling Retriever", 150),
        2: ("Owczarek Belgijski", 200),
        3: ("Samoyed", 100),
        4: ("Chart", 120)
    }

    return breeds[choice]


def choose_difficulty():
    print()
    print("Poziom trudności:")
    print("1 - Łatwy")
    print("2 - Normalny")
    print("3 - Trudny")
    print()

    difficulty = get_input(
        "Poziom (1-3, domyslnie 2): ",
        int,
        2,
        lambda x: 1 <= x <= 3
    )

    if difficulty == 1:
        return "Łatwy", 40

    if difficulty == 2:
        return "Normalny", 30

    return "Trudny", 20


def main_game():
    os.system("cls" if os.name == "nt" else "clear")

    print(f"""Witaj w grze!!!!
Celem twojej wyprawy jako psa jest znalezienie kości, lecz musisz się strzec przed trudnościami:
    - Nie zgub się (nie wyjdź poza świat, którego rozmiar to {WORLD_SIZE} na {WORLD_SIZE})
    - Pamiętaj o wskaźniku zmęczenia (możesz je zmniejszyć przez użycie elementów ekwipunku, lub poprzez znalezienie odpowiedniego miejsca)
W trakcie rundy możesz zdecydować się na różne akcje, wpisując:
    - eq (zobaczenie ekwipunku)
    - uzyj smaczek (zmniejsza zmęczenie)
    - uzyj woda (zmniejsza zmęczenie)
    - np. 90 50 (azymut i ilość kroków do przodu)
Przed grą będziesz musiał podać przy pytaniach:
    - imię swojego psa
    - rasę psa (odpowiadają im różne zmęczenia)
    - poziom trudności
    - współrzędne początkowe x i y
    - początkowe zmęczenie
Powodzenia!!!!""")


    world = World(WORLD_SIZE)

    visualizer = GameVisualizer()
    visualizer.draw_world()

    turtle.Screen().update()

    name = get_input(
        "Imie psa (domyślnie Azor): ",
        str,
        "Reksio"
    )

    breed_name, max_fatigue = choose_breed()

    difficulty_name, max_steps = choose_difficulty()

    start_x = get_input(
        f"Pozycja X ({-WORLD_SIZE//2} do {WORLD_SIZE//2}): ",
        int,
        0,
        lambda x: -WORLD_SIZE//2 <= x <= WORLD_SIZE//2
    )

    start_y = get_input(
        f"Pozycja Y ({-WORLD_SIZE//2} do {WORLD_SIZE//2}): ",
        int,
        0,
        lambda y: -WORLD_SIZE//2 <= y <= WORLD_SIZE//2
    )

    start_fatigue = get_input(
        "Poczatkowe zmeczenie (0 domyslnie, im mniej tym prościej ;0 ): ",
        int,
        0,
        lambda x: x >= 0
    )

    dog = Dog(
        name,
        breed_name,
        start_x,
        start_y,
        start_fatigue,
        max_fatigue
    )

    bone = Bone(WORLD_SIZE)

    house_marker = visualizer.draw_house(
        start_x,
        start_y
    )

    bone_marker = visualizer.draw_marker(
        bone.get_x(),
        bone.get_y(),
        "black",
        "circle"
    )

    visualizer.update_hud(dog)

    print()
    print("PODSUMOWANIE STARTU")
    print(f"Pies: {name}")
    print(f"Rasa: {breed_name}")
    print(f"Pozycja startowa: ({start_x}, {start_y})")
    print(f"Zmeczenie: {start_fatigue}/{max_fatigue}")
    print(f"Poziom trudnosci: {difficulty_name}")
    print(f"Limit etapow: {max_steps}")
    print(f"Granice swiata: {-WORLD_SIZE//2} do {WORLD_SIZE//2}")
    print("Warunek sukcesu: znalezienie kosci")

    step_counter = 0

    success = False

    end_reason = ""

    while True:
        turtle.Screen().update()
        turtle.getcanvas().winfo_toplevel().update()

        if step_counter >= max_steps:
            end_reason = "Przekroczono limit etapow"
            break

        command = input(
            f"\n[KROK {step_counter + 1}] Podaj polecenie: "
        ).strip().lower()

        if command == "eq":
            print("--- EKWIPUNEK ---")
            print(dog.get_inventory())
            continue

        if command == "uzyj smaczek":
            if dog.use_item("smaczki"):
                print("Pies zjadl smaczka.")
                print("Zmeczenie spadlo o 10.")
            else:
                print("Brak smaczkow.")
            visualizer.update_hud(dog)
            continue

        if command == "uzyj woda":
            if dog.use_item("woda"):
                print("Pies wypil wode.")
                print("Zmeczenie spadlo o 15.")
            else:
                print("Brak wody.")
            visualizer.update_hud(dog)
            continue

        try:
            azimuth, steps = map(int, command.split())

            if azimuth < 0 or azimuth > 359:
                print("Kat musi byc od 0 do 359.")
                continue

            if steps <= 0:
                print("Liczba krokow musi byc dodatnia.")
                continue

        except ValueError:
            print("Wpisz np. '90 30' albo 'eq'.")
            continue

        step_counter += 1

        old_x = dog.get_x()
        old_y = dog.get_y()

        old_fatigue = dog.get_fatigue()

        dog.move(azimuth, steps)

        fatigue_cost = max(1, steps // 4)

        dog.add_fatigue(fatigue_cost)

        random_world_element(dog)

        random_event(dog)

        visualizer.update_hud(dog)

        distance_to_bone = math.sqrt(
            (dog.get_x() - bone.get_x()) ** 2 +
            (dog.get_y() - bone.get_y()) ** 2
        )

        print()
        print(f"Ruch: kat {azimuth}, kroki {steps}")
        print(
            f"Pozycja przed: "
            f"({round(old_x)}, {round(old_y)})"
        )
        print(
            f"Pozycja po: "
            f"({round(dog.get_x())}, {round(dog.get_y())})"
        )

        print(
            f"Zmeczenie przed: "
            f"{old_fatigue}/{dog.get_max_fatigue()}"
        )

        print(
            f"Zmeczenie po: "
            f"{dog.get_fatigue()}/{dog.get_max_fatigue()}"
        )

        print(
            f"Koszt ruchu: +{fatigue_cost}"
        )

        print(
            f"Odleglosc od kosci: "
            f"{round(distance_to_bone, 1)}"
        )

        if not world.is_inside(
                dog.get_x(),
                dog.get_y()
        ):
            end_reason = "Pies opuscil granice swiata"
            break

        if dog.get_fatigue() >= dog.get_max_fatigue():
            end_reason = "Pies osiagnal maksymalne zmeczenie"
            break

        if distance_to_bone <= 15:
            dog.add_item("kosci")
            dog.add_event("Odnaleziono ukryta kosc")

            success = True

            end_reason = "Odnaleziono kosc"

            break

    end_marker = visualizer.draw_marker(
        dog.get_x(),
        dog.get_y(),
        "black",
        "triangle"
    )

    turtle.Screen().update()

    score = 5000

    score -= step_counter * 100

    score -= int(dog.get_distance())

    score += dog.get_inventory()["smaczki"] * 150

    score += dog.get_inventory()["woda"] * 100

    if success:
        score += 2000

    if difficulty_name == "Normalny":
        score += 500

    if difficulty_name == "Trudny":
        score += 1000

    if score < 0:
        score = 0

    print()
    print("RAPORT KONCOWY")
    print(
        f"Nazwa psa: "
        f"{dog.get_name()} ({dog.get_breed()})"
    )

    print(
        f"Parametry startowe: "
        f"({start_x}, {start_y}), "
    )

    print(
        f"Pozycja koncowa: "
        f"({round(dog.get_x())}, "
        f"{round(dog.get_y())})"
    )

    print(
        f"Liczba etapow: "
        f"{step_counter}"
    )

    print(
        f"Przebyty dystans: "
        f"{dog.get_distance()}"
    )

    print(
        f"Zmeczenie: "
        f"{dog.get_fatigue()}/"
        f"{dog.get_max_fatigue()}"
    )

    print(
        f"Ekwipunek: "
        f"{dog.get_inventory()}"
    )

    print()
    print("Najwazniejsze zdarzenia:")

    history = dog.get_history()

    if len(history) == 0:
        print("Brak zapisanych zdarzen.")
    else:
        for index, event in enumerate(history, start=1):
            print(index, "-", event)

    print()
    print(
        f"Przyczyna zakonczenia: "
        f"{end_reason}"
    )

    if success:
        print("Status wyprawy: SUKCES")
    else:
        print("Status wyprawy: PORAZKA")

    print(
        f"Wynik koncowy: "
        f"{score} pkt"
    )

    print("----------------------------------------------")

    choice = input(
        "\nUruchomic ponownie? (tak/nie): "
    ).strip().lower()

    if choice in ["tak", "t", "yes", "y"]:
        dog.clear()

        house_marker.clear()
        house_marker.hideturtle()

        bone_marker.clear()
        bone_marker.hideturtle()

        end_marker.clear()
        end_marker.hideturtle()

        visualizer._drawer.clear()
        visualizer._hud.clear()

        return True

    print("Koniec programu.")
    return False


if __name__ == "__main__":
    screen = turtle.Screen()

    screen.title("Symulator Wyprawy Psa")

    screen.setup(
        WORLD_SIZE + 250,
        WORLD_SIZE + 150,
        startx=900,
        starty=100
    )

    screen.tracer(0)

    running = True

    while running:
        running = main_game()

    screen.bye()

