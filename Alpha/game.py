import json
import time
import glob
import os
import random
import dice
import graphics
import time

PLAYER_WHITE = 0
PLAYER_BLACK = 1

MAX_SAVES = 5

# Klíče
class Keys:
    # Inicializace klíčů
    def __init__(self) -> None:
        self.primary = list(range(1,25))
        self.secondary = list(range(24, 0, -1))

# Bar
class Bar:
    # Inicializace baru
    def __init__(self) -> None:
        self.checkers = []
        self.has_any = False

    # Přidá kámen
    def add_checker(self, checker):
        self.checkers.append(checker)
        self.has_any = True

    # Odstraní kámen
    def remove_checker(self):
        if len(self.checkers) == 1:
            self.has_any = False
        return self.checkers.pop()

class Home(Bar):
    # Inicializace domečku
    def __init__(self) -> None:
        super().__init__()

# Hra
class Game:
    # Inicializace hry
    def __init__(self) -> None:
        self.keys = Keys()
        self.now_playing = PLAYER_WHITE
        self.points = dict()
        self.init_points()
        self.rolled_history = []
        self.bars = {
            0: Bar(),
            1: Bar()
        }
        self.homes = {
            0: Home(),
            1: Home()
        }
        self.rounds_played = 0
        self.reset_active_saves()
        self.players = dict()

    # Inicializace polí
    def init_points(self) -> None:
        for i in range(1,25):
            self.points[i] = Point()

        self.points[1].add_checker(Checker(PLAYER_WHITE, 0))
        self.points[1].add_checker(Checker(PLAYER_WHITE, 2))

        self.points[6].add_checker(Checker(PLAYER_BLACK, 1))
        self.points[6].add_checker(Checker(PLAYER_BLACK, 3))
        self.points[6].add_checker(Checker(PLAYER_BLACK, 5))
        self.points[6].add_checker(Checker(PLAYER_BLACK, 7))
        self.points[6].add_checker(Checker(PLAYER_BLACK, 9))
        self.points[8].add_checker(Checker(PLAYER_BLACK, 11))
        self.points[8].add_checker(Checker(PLAYER_BLACK, 13))
        self.points[8].add_checker(Checker(PLAYER_BLACK, 15))

        self.points[12].add_checker(Checker(PLAYER_WHITE, 4))
        self.points[12].add_checker(Checker(PLAYER_WHITE, 6))
        self.points[12].add_checker(Checker(PLAYER_WHITE, 8))
        self.points[12].add_checker(Checker(PLAYER_WHITE, 10))
        self.points[12].add_checker(Checker(PLAYER_WHITE, 12))

        self.points[13].add_checker(Checker(PLAYER_BLACK, 17))
        self.points[13].add_checker(Checker(PLAYER_BLACK, 19))
        self.points[13].add_checker(Checker(PLAYER_BLACK, 21))
        self.points[13].add_checker(Checker(PLAYER_BLACK, 23))
        self.points[13].add_checker(Checker(PLAYER_BLACK, 25))

        self.points[17].add_checker(Checker(PLAYER_WHITE, 14))
        self.points[17].add_checker(Checker(PLAYER_WHITE, 16))
        self.points[17].add_checker(Checker(PLAYER_WHITE, 18))
        self.points[19].add_checker(Checker(PLAYER_WHITE, 20))
        self.points[19].add_checker(Checker(PLAYER_WHITE, 22))
        self.points[19].add_checker(Checker(PLAYER_WHITE, 24))
        self.points[19].add_checker(Checker(PLAYER_WHITE, 26))
        self.points[19].add_checker(Checker(PLAYER_WHITE, 28))

        self.points[24].add_checker(Checker(PLAYER_BLACK, 27))
        self.points[24].add_checker(Checker(PLAYER_BLACK, 29))

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
        result = input("Opravdu chcete ukončit hru? y/n: ")
        if result == "y":
            return True
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

        if to_point >= 24 or to_point <= -1:
            checker.point_history.append("home")
            self.homes[self.now_playing].add_checker(checker)
            return abs(from_point - to_point)
        
        
        # Pokud byl odebrán kámen
        if checker is not None:
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
    
    # Pole SAVEů
    def list_saves(self) -> list:
        return glob.glob("saves/????????-??????.json")
    
    # Z aktivní SAVŮ, které nejsou už aktivní udělá neaktivní
    def reset_active_saves(self):
        if os.path.isdir("saves"):
            for file in self.list_saves():
                with open(file, 'r') as fp:
                    data = json.load(fp)
                    data["now_running"] = False
                with open(file, 'w') as fp:
                    fp.write(json.dumps(data, default=vars, indent=4))

    # Pokud savy přesahují limit, nejstarší odstraní
    def clear_saves(self):
        saves = self.list_saves()
        if len(saves) >= MAX_SAVES:
            sorted_saves = sorted(saves, reverse=True)
            for save in sorted_saves[MAX_SAVES:]:
                os.remove(save)

    # Uložení hry
    def save(self):
        if not os.path.isdir("saves"):
            os.mkdir("saves")
            
        saves = self.list_saves()
        for file in saves:
            remove = False
            with open(file, 'r') as fp:
                data = json.load(fp)
                if data["now_running"] == True:
                    remove = True
            if remove:
                os.remove(file)

        timestr = time.strftime("%Y%m%d-%H%M%S")
        with open(f'saves/{timestr}.json', 'w+') as fp:
            data = dict()
            data["points"] = self.points
            data["bars"] = self.bars
            data["homes"] = self.homes
            data["players"] = [self.players[0].type, self.players[1].type]
            data["now_playing"] = self.now_playing
            data["rounds_played"] = self.rounds_played
            data["rolled_history"] = self.rolled_history
            data["now_running"] = True
            data_json = json.dumps(data, default=vars, indent=4)
            fp.write(data_json)

        self.clear_saves()

    # Načtení hry
    def load(self, save_path):
        with open(save_path, 'r') as fp:
            data = json.load(fp)

            self.rounds_played = data["rounds_played"]
            self.now_playing = data["now_playing"]
            self.rolled_history = data["rolled_history"]
            self.players[0] = Player().create_player(data["players"][0])
            self.players[1] = Player().create_player(data["players"][1])
            self.homes = dict()
            for i in data["homes"]:
                self.homes[int(i)] = Bar()
                for checker in data["homes"][i]["checkers"]:
                    self.homes[int(i)].add_checker(Checker(id=checker["id"], color=checker["color"], point_history=checker["point_history"]))
            
            self.bars = dict()
            for i in data["homes"]:
                self.bars[int(i)] = Bar()
                for checker in data["bars"][i]["checkers"]:
                    self.bars[int(i)].add_checker(Checker(id=checker["id"], color=checker["color"], point_history=checker["point_history"]))
            
            self.points = dict()
            for i, point in data["points"].items():
                self.points[int(i)] = Point()
                if point["first_checker"] == None:
                    self.points[int(i)].first_checker = None
                else:
                    first_checker = Checker(id=point["first_checker"]["id"], color=point["first_checker"]["color"], point_history=point["first_checker"]["point_history"])
                    checker = point["first_checker"]
                    checkers = [first_checker]
                    while checker["next_checker"] is not None:
                        checker = checker["next_checker"]
                        checkers.append(Checker(id=checker["id"], color=checker["color"], point_history=checker["point_history"]))
                    for j in range(len(checkers)-1,-1,-1):
                        self.points[int(i)].add_checker(checkers[j])
            
    # Přepínač hráčů
    def switch_players(self) -> None:
        if self.now_playing == PLAYER_BLACK:
            self.now_playing = PLAYER_WHITE
        else:
            self.now_playing = PLAYER_BLACK
        
        self.rounds_played += 0.5
    
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
            valid_move_bear_off = self.valid_move_bear_off(point_key, dice_number)
            print(valid_move, valid_move_bear_off)
            if valid_move is not None:
                moves.append(valid_move)
            if valid_move_bear_off is not None:
                moves.append(valid_move_bear_off)
        return list(set(moves))
    
    # Platné tahy během vyvádění kamenů
    def valid_move_bear_off(self, point_key, dice_number):
        if self.is_bearing_off():
            keys = self.current_keys()
            if keys == self.keys.primary:
                changed_key = point_key + dice_number
            else:
                changed_key = point_key - dice_number
            if changed_key == 0 or changed_key == 25:
                return changed_key
            
            first_key = None
            if self.now_playing == PLAYER_WHITE:
                for key in self.keys.primary:
                    if self.points[key].get_color() == PLAYER_WHITE:
                        first_key = key
                        break
            elif self.now_playing == PLAYER_BLACK:
                for key in self.keys.secondary:
                    if self.points[key].get_color() == PLAYER_BLACK:
                        first_key = key
                        break
            if first_key == point_key:
                if changed_key > 24:
                    
                    return changed_key
                elif changed_key < 1:
                    return changed_key

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

    # Má některý z hráčů všechny kameny v domečku?
    def finished(self):
        if len(self.homes[0].checkers) == 15 or len(self.homes[1].checkers) == 15:
            return True
        else:
            return False

    # Sebere všechny kameny ve hře a vrátí seznam
    def collect_checkers(self):
        all_checkers = dict()
        for i in self.bars:
            for checker in self.bars[i].checkers:
                all_checkers[checker.id] = checker
        for i in self.homes:
            for checker in self.homes[i].checkers:
                all_checkers[checker.id] = checker
        for key in self.keys.primary:
            first = self.points[key].first_checker
            if first is not None:
                all_checkers[first.id] = first
                while first.next_checker is not None:
                    first = first.next_checker
                    all_checkers[first.id] = first

        all_checkers = dict(sorted(all_checkers.items()))
        return all_checkers

    # Průměrná životnost v tazích    
    def get_average_lifespan(self):
        all_checkers = self.collect_checkers()
        checker_lifespan = dict()
        total_points = 0
        for key in all_checkers:
            total_points = len(all_checkers[key].point_history)
            if "bar" not in all_checkers[key].point_history:
                checker_lifespan[key] = total_points
            else:
                i = 0
                occurences = []
                for item in all_checkers[key].point_history:
                    i += 1
                    if item == "bar":
                        occurences.append(i)
                        i = 0
                checker_lifespan[key] = sum(occurences) / len(occurences)
        
        avg1 = 0
        avg2 = 0
        for key in checker_lifespan:
            if key % 2 == 0:
                avg1 += checker_lifespan[key]
            else:
                avg2 += checker_lifespan[key]
        
        avg1 = avg1 / 15
        avg2 = avg2 / 15

        return (avg1, avg2)

    # Vybere kdo začíná
    def choose_first(self):
        num1 = 0
        num2 = 0
        while num1 == num2:
            num1 = self.players[0].roll_single_dice()
            
            graphics.Display().double_dice([num1, ""])
            print("HRÁČ1, HRÁČ2")
            num2 = self.players[1].roll_single_dice()
            graphics.Display().double_dice([num1, num2])

            if num1 == num2:
                print("Hráči hodili stejná čísla, bude se házet znovu")
            print("\nPokračujte stisknutím ENTER")
            input("ENTER > ")
        if num2 > num1:
            self.players[0], self.players[1] = self.players[1], self.players[0]
        print("Hra může začít, stisknutím ENTER spustíte hru")
        input("ENTER > ")


# Kámen
class Checker:
    # Inicializace kamene
    def __init__(self, color, id, point_history = []) -> None:
        self.id = id
        self.color = color
        self.next_checker = None
        if point_history == [] or point_history == None:
            self.point_history = []
        else:
            self.point_history = point_history


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

class Player:
    def create_player(self, type):
        if type == "console":
            return ConsolePlayer()
        if type == "ai":
            return AIPlayer()
    

class ConsolePlayer(Player):
    def __init__(self) -> None:
        self.type = "console"

    def play(self, options: list, text: str) -> str:
        result = input(text)
        return result
    
    def roll_single_dice(self) -> int:
        number = dice.Dice().roll()
        input("Stisknutím ENTER hodíte kostkou > ")
        return number

    def roll_double_dice(self) -> list:
        number = dice.DoubleDice().roll()
        input("Stisknutím ENTER hodíte dvojkostkou > ")
        return number


class AIPlayer(Player):
    def __init__(self) -> None:
        self.type = "ai"

    def play(self, options: list, text: str) -> str:
        result = random.choice(options)
        print("Prosím čekejte hráč hraje ... ")
        time.sleep(2.5)
        return result
    
    def roll_single_dice(self) -> int:
        number = dice.Dice().roll()
        print("Prosím čekejte hráč hází kostkou ... ")
        time.sleep(1.5)
        return number

    def roll_double_dice(self) -> list:
        number = dice.DoubleDice().roll()
        print("Prosím čekejte hráč hází dvojkostkou ... ")
        time.sleep(1.5)
        return number
    
    