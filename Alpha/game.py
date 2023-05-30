import json

PLAYER_WHITE = 0
PLAYER_BLACK = 1

# Klíče
class Keys:
    def __init__(self) -> None:
        self.primary = list(range(1,25))
        self.secondary = list(range(24, 0, -1))

# Bar
class Bar:
    def __init__(self) -> None:
        self.checkers = []
        self.has_any = False

    def add_checker(self, checker):
        self.checkers.append(checker)
        self.has_any = True

    def remove_checker(self):
        if len(self.checkers) == 1:
            self.has_any = False
        return self.checkers.pop()



# Hra
class Game:
    # Inicializace hry
    def __init__(self) -> None:
        self.keys = Keys()
        self.now_playing = PLAYER_WHITE
        self.points = dict()
        self.init_points()
        self.bars = {
            0: Bar(),
            1: Bar()
        }
        self.PLAYER_WHITE = 0
        self.PLAYER_BLACK = 1

    # Inicializace polí
    def init_points(self) -> None:
        for i in range(1,25):
            self.points[i] = Point()

        self.points[1].add_checker(Checker(PLAYER_WHITE, 1))
        self.points[1].add_checker(Checker(PLAYER_WHITE, 2))

        self.points[6].add_checker(Checker(PLAYER_BLACK, 3))
        self.points[6].add_checker(Checker(PLAYER_BLACK, 4))
        self.points[6].add_checker(Checker(PLAYER_BLACK, 5))
        self.points[6].add_checker(Checker(PLAYER_BLACK, 6))
        self.points[6].add_checker(Checker(PLAYER_BLACK, 7))
        self.points[8].add_checker(Checker(PLAYER_BLACK, 8))
        self.points[8].add_checker(Checker(PLAYER_BLACK, 9))
        self.points[8].add_checker(Checker(PLAYER_BLACK, 10))

        self.points[12].add_checker(Checker(PLAYER_WHITE, 11))
        self.points[12].add_checker(Checker(PLAYER_WHITE, 12))
        self.points[12].add_checker(Checker(PLAYER_WHITE, 13))
        self.points[12].add_checker(Checker(PLAYER_WHITE, 14))
        self.points[12].add_checker(Checker(PLAYER_WHITE, 15))

        self.points[13].add_checker(Checker(PLAYER_BLACK, 16))
        self.points[13].add_checker(Checker(PLAYER_BLACK, 17))
        self.points[13].add_checker(Checker(PLAYER_BLACK, 18))
        self.points[13].add_checker(Checker(PLAYER_BLACK, 19))
        self.points[13].add_checker(Checker(PLAYER_BLACK, 20))

        self.points[17].add_checker(Checker(PLAYER_WHITE, 21))
        self.points[17].add_checker(Checker(PLAYER_WHITE, 22))
        self.points[17].add_checker(Checker(PLAYER_WHITE, 23))
        self.points[19].add_checker(Checker(PLAYER_WHITE, 24))
        self.points[19].add_checker(Checker(PLAYER_WHITE, 25))
        self.points[19].add_checker(Checker(PLAYER_WHITE, 26))
        self.points[19].add_checker(Checker(PLAYER_WHITE, 27))
        self.points[19].add_checker(Checker(PLAYER_WHITE, 28))

        self.points[24].add_checker(Checker(PLAYER_BLACK, 29))
        self.points[24].add_checker(Checker(PLAYER_BLACK, 30))

    # Je hráč v režimu vyvádění?
    def is_bearing_off(self):
        if self.now_playing == PLAYER_WHITE:
            for key in self.keys.primary:
                if key < 19 and self.points[key].get_color() == PLAYER_WHITE:
                    return False
        elif self.now_playing == PLAYER_BLACK:
            for key in self.keys.secondary:
                if key > 6 and self.points[key].get_color() == PLAYER_BLACK:
                    return False
        return True
    
    # Ukončení hry
    def quit_game(self):
        if input("Opravdu chcete ukončit hru? y/n: ") == "y":
            exit(0)
        return False

    # Zobraz hru (textový mód)
    def display(self) -> None:
        print("------------- Stav hry -------------")
        for key in self.points:
            print(f"{key}. pole -> kamenů: {self.points[key].count_checkers()}, barva: {None if self.points[key].first_checker == None else self.points[key].first_checker.color}")
            if key in [6,12,18]:
                print()

    # Aktuální klíče
    def current_keys(self) -> list:
        if self.now_playing == PLAYER_WHITE:
            keys = self.keys.primary
        else:
            keys = self.keys.secondary
        return keys

    # Přesun kamene z jednoho pole na jiné pole
    def move(self, from_point: int, to_point: int) -> int:
        keys = self.keys.primary

        if from_point < 0 or from_point > 23:
            checker = self.bars[self.now_playing].remove_checker()
        else:
            checker = self.points[keys[from_point]].remove_checker()
        # Pokud byl odebrán kámen
        if checker:
            if self.points[keys[to_point]].first_checker:
                if not self.points[keys[to_point]].first_checker.color == checker.color:
                    self.points[keys[to_point]].first_checker.point_history.append("bar")
                    self.bars[self.points[keys[to_point]].first_checker.color].add_checker(self.points[keys[to_point]].first_checker)
            if checker.point_history == []:
                checker.point_history.append(from_point+1)
            checker.point_history.append(to_point+1)
            self.points[keys[to_point]].add_checker(checker)
            return abs(from_point - to_point)
        
        return 0
    
    # Ulož hru (zatím nefunkční)
    def save(self):
        with open('result.json', 'w') as fp:
            data = dict()
            data["points"] = self.points
            data["bars"] = self.bars
            data["now_playing"] = self.now_playing
            data_json = json.dumps(data, default=vars, indent=4)
            fp.write(data_json)

    def load(self):
        with open('result.json', 'r') as fp:
            self.points = json.load(fp)

    # Přepínač hráčů
    def switch_players(self) -> None:
        if self.now_playing == PLAYER_BLACK:
            self.now_playing = PLAYER_WHITE
        else:
            self.now_playing = PLAYER_BLACK
    
    # Platný tah
    def valid_move(self, point_key, dice_number):
        keys = self.current_keys()
        if keys == self.keys.primary:
            changed_key = point_key + dice_number
        else:
             changed_key = point_key - dice_number
        if changed_key in keys:
            if not self.points[changed_key].first_checker:
                return changed_key
            elif self.points[changed_key].first_checker.color == self.now_playing:
                return changed_key
            elif not self.points[changed_key].first_checker.next_checker:
                return changed_key
            
        return None

    # Platné tahy
    def valid_moves(self, point_key, dice_numbers):
        moves = []
        for dice_number in dice_numbers:
            valid_move = self.valid_move(point_key, dice_number)
            if valid_move:
                moves.append(valid_move)
        return list(set(moves))
    
    # Platné tahy během vyvádění kamenů
    def valid_move_bear_off(self, point_key):
        if self.is_bearing_off():
            pass

    # Platné tahy během vyvádění kamenů
    def valid_moves_bear_off(self, point_key):
        if self.is_bearing_off():
            pass

    # Platné tahy během vyvádění kamenů
    def valid_points_bear_off(self, dice_numbers):
        if self.is_bearing_off():
            pass

    # Možná pole
    def valid_points(self, dice_numbers):
        points = []
        keys = self.keys.primary
        
        for key in keys:
            #print(key, self.points[key].get_color(), self.now_playing)
            if self.points[key].first_checker and self.points[key].get_color() == self.now_playing:
                if self.valid_moves(key, dice_numbers):
                    points.append(key)
        
        return points


# Kámen
class Checker:
    # Inicializace kamene
    def __init__(self, color, id) -> None:
        self.id = id
        self.color = color
        self.next_checker = None
        self.point_history = []

# Pole
class Point:
    # Inicializace pole
    def __init__(self) -> None:
        self.first_checker = None

    # Přidání kamene
    def add_checker(self, new_checker: Checker) -> None:
        # Pokud v poli není žádný kámen
        if self.first_checker is None:
            self.first_checker = new_checker
        # Pokud v poli již kámen je
        else:
            # Přidáváme stejnou barvu na stejnou barvu
            if self.first_checker.color == new_checker.color:
                new_checker.next_checker = self.first_checker # type: ignore
                self.first_checker = new_checker
            # Přidáváme jinou barvu
            else:
                if self.count_checkers() == 1:
                    self.first_checker = new_checker


    # Počet kamenů v poli
    def count_checkers(self) -> int:
        checker = self.first_checker
        if checker is None:
            return 0
        else:
            count = 1
            while checker.next_checker is not None:
                checker = checker.next_checker
                count += 1
            return count

    # Získání barvy pole
    def get_color(self):
        if self.first_checker == None:
            return None
        else:
            return self.first_checker.color

    # Odstranění kamene z pole
    def remove_checker(self):
        checker = self.first_checker
        if checker:
            if checker.next_checker is None:
                self.first_checker = None
            else:
                self.first_checker = checker.next_checker
                checker.next_checker = None
            return checker
        return None

