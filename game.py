""" Stručný popis zadání:
Vytvořte implementaci hry vrhcáby, která podporuje hru dvou hráčů či hru proti jednoduché umělé inteligenci.

povinně implementovaná funkčnost:
generování hodu kostkami
výpis všech možných tahů hráče
jednoduchá umělá inteligence, která náhodně volí jeden z platných tahů
trasování chodu každého jednotlivého kamene (od vstupu z baru po vyhození/vyvedení), herní pole se chovají jako zásobník
uložení a obnova stavu hry (s návrhem vlastního JSON formátu pro uložení)

co musí zobrazovat displej (výpis na standardním vstupu)
výsledky hodů kostkami
pozice všech kamenů na desce (včetně těch "na baru")
stručný komentář toho, co se ve hře událo a nemusí být zřejmé ze zobrazení na desce (kámen vstoupil do hry, byl "vyhozen", opustil hru, hráč nemůže hrát tj. ani házet, pod.)
počet vyvedených kamenů
po výhře typ výhry
po ukončení se zobrazí statistika o všech kamenech ve hře (zvlášť pro bílého a černého), například:
počet kamenů vyhozených, vyvedených a opuštěných
průměrná životnost kamene v tazích """


import random
PLAYER_BLACK = 0
PLAYER_WHITE = 1




# Hra (Herní deska)
class Game:
    def __init__(self) -> None:
        self.points = dict()
        self.players = dict()
        for i in range(1,25):
            self.points[i] = Point()

    def set_player(self, player) -> bool:
        if not player.player_color in self.players.keys():
            self.players[player.player_color] = player
            return True
        return False

    def display(self) -> None:
        print("\n\n\n------------- Stav hry -------------")
        for key in self.points:
            print(f"{key}. pole -> kamenů: {self.points[key].count_checkers()}, barva: {self.points[key].owner}")
            if key in [6,12,18]:
                print()

    def init_points(self) -> None:
        self.points[1].add_checker(Checker(PLAYER_BLACK, 1))
        self.points[1].add_checker(Checker(PLAYER_BLACK, 2))

        self.points[6].add_checker(Checker(PLAYER_WHITE, 3))
        self.points[6].add_checker(Checker(PLAYER_WHITE, 4))
        self.points[6].add_checker(Checker(PLAYER_WHITE, 5))
        self.points[6].add_checker(Checker(PLAYER_WHITE, 6))
        self.points[6].add_checker(Checker(PLAYER_WHITE, 7))

        self.points[8].add_checker(Checker(PLAYER_WHITE, 8))
        self.points[8].add_checker(Checker(PLAYER_WHITE, 9))
        self.points[8].add_checker(Checker(PLAYER_WHITE, 10))

        self.points[12].add_checker(Checker(PLAYER_BLACK, 11))
        self.points[12].add_checker(Checker(PLAYER_BLACK, 12))
        self.points[12].add_checker(Checker(PLAYER_BLACK, 13))
        self.points[12].add_checker(Checker(PLAYER_BLACK, 14))
        self.points[12].add_checker(Checker(PLAYER_BLACK, 15))

        self.points[13].add_checker(Checker(PLAYER_WHITE, 16))
        self.points[13].add_checker(Checker(PLAYER_WHITE, 17))
        self.points[13].add_checker(Checker(PLAYER_WHITE, 18))
        self.points[13].add_checker(Checker(PLAYER_WHITE, 19))
        self.points[13].add_checker(Checker(PLAYER_WHITE, 20))

        self.points[17].add_checker(Checker(PLAYER_BLACK, 21))
        self.points[17].add_checker(Checker(PLAYER_BLACK, 22))
        self.points[17].add_checker(Checker(PLAYER_BLACK, 23))

        self.points[19].add_checker(Checker(PLAYER_BLACK, 24))
        self.points[19].add_checker(Checker(PLAYER_BLACK, 25))
        self.points[19].add_checker(Checker(PLAYER_BLACK, 26))
        self.points[19].add_checker(Checker(PLAYER_BLACK, 27))
        self.points[19].add_checker(Checker(PLAYER_BLACK, 28))

        self.points[24].add_checker(Checker(PLAYER_WHITE, 29))
        self.points[24].add_checker(Checker(PLAYER_WHITE, 30))

    def bear_off_ready(self, player):
        if isinstance(player, Player):
            last_key = None
            for key in self.points:
                if player.player_color == PLAYER_BLACK:
                    if self.points[key].owner == player.player_color:
                        if key < 19:
                            return 0
                        else:
                            return 25 - key
                elif player.player_color == PLAYER_WHITE:
                    if self.points[key].owner == player.player_color:
                        if key > 6:
                            return 0
                        else:
                            last_key = key
            return last_key
        else:
            return 0

    def toggle_bear_off(self, player_color) -> None:
        if self.bear_off_ready(self.players[player_color]):
            self.players[player_color].bear_off_available = True
            print("Vyvádění kamenů aktivní")
        else:
            self.players[player_color].bear_off_available = False
            print("Vyvádění kamenů neaktivní")

    def move(self, from_point: int, to_point: int) -> None:
        checker = self.points[from_point].remove_checker()
        if checker:
            if not self.points[to_point].add_checker(checker):
                self.points[from_point].add_checker(checker)
            else:
                self.toggle_bear_off(self.points[to_point].owner)
        else:
            print('Přesun neproběhl.')

    def find_available_points(self, owner: int, dice_numbers: list) -> list:
        available_points = []
        # Vyvádění kamenů
        if self.bear_off_ready(self.players[owner]):
            pass
        else:
            for key in self.points:
                # Všechna dostupná pole hráče
                if self.points[key].owner == owner:
                    # Pokud DvojKostka hodila 2 čísla
                    if len(dice_numbers) == 2:
                        for dice_number in dice_numbers:
                            if owner == PLAYER_BLACK:
                                if key + dice_number <= 24:
                                    if (self.points[key + dice_number].owner == owner) or (self.points[key + dice_number].count_checkers() <= 1):
                                        available_points.append(key)
                            elif owner == PLAYER_WHITE:
                                if key - dice_number > 0:
                                    if (self.points[key - dice_number].owner == owner) or (self.points[key - dice_number].count_checkers() <= 1):
                                        available_points.append(key)
                    # Pokud DvojKostka hodila 4 čísla
                    elif len(dice_numbers) == 4:
                        if owner == PLAYER_BLACK:
                            if key + dice_numbers[0] <= 24:
                                if (self.points[key + dice_numbers[0]].owner == owner) or (self.points[key + dice_numbers[0]].count_checkers() <= 1):
                                    available_points.append(key)
                        elif owner == PLAYER_WHITE:
                            if key - dice_numbers[0] > 0:
                                if (self.points[key - dice_numbers[0]].owner == owner) or (self.points[key - dice_numbers[0]].count_checkers() <= 1):
                                    available_points.append(key)
        return list(set(available_points))
    

# Herní kámen (s pamětí, kde se postupně nacházel)
class Checker:
    def __init__(self, owner, checker_id: int) -> None:
        self.next_checker = None
        self.id = checker_id
        self.owner = owner


# HerníPole (modifikovaný zásobník, lze vkládat jen kameny stejných barev)
class Point:
    def __init__(self) -> None:
        self.first_checker = None
        self.owner = None

    def add_checker(self, checker: Checker) -> bool:
        # Pokud se na poli nevyskytuje žádný kámen
        if self.first_checker is None:
            self.first_checker = checker
            self.owner = checker.owner
            return True
        # Pokud se již na poli nějaký kámen nachází
        else:
            # Pokud je kámen stejného hráče
            if checker.owner == self.first_checker.owner:
                checker.next_checker = self.first_checker
                self.first_checker = checker
                return True
            # Pokud patří jinému hráči
            else:
                print('Nelze přidat, pole patří jinému hráči')
                return False

    def remove_checker(self):
        if self.first_checker is not None:
            checker = self.first_checker
            if checker.next_checker == None:
                self.owner = None
                self.first_checker = None
            else:
                self.first_checker = checker.next_checker
                checker.next_checker = None
            return checker
        else:
            print('Nelze odebrat kámen, který neexistuje')

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


# Dvojkostka (vrací seznam možných dvojic či čtveřic)
class DoubleDice:
    def __init__(self) -> None:
        pass

    def roll(self):
        number1 = random.randint(1,6)
        number2 = random.randint(1,6)
        numbers = [number1, number2]
        if number1 == number2:
            numbers.append(number1)
            numbers.append(number2)
        return numbers


# Bar (továrna na herní kameny, s řízenou produkcí)
class Bar:
    def __init__(self) -> None:
        pass


# Hráč
class Player:
    def __init__(self, player_color: int) -> None:
        self.player_color = player_color
        self.bear_off_available = False
        self.bear_off_needed = None


class ConsolePlayer(Player):
    pass


class AIPlayer(Player):
    pass

game = Game()
player = Player(PLAYER_BLACK)
game.set_player(player)
game.init_points()
game.display()
print(game.find_available_points(player.player_color, [5,6]))
#dice = DoubleDice()
#print(dice.roll())