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



# Hra (Herní deska)
class Game:
    def __init__(self) -> None:
        self.points = dict()
        for i in range(1,25):
            self.points[i] = Point()
    def display(self) -> None:
        print("\n\n\n------------- Stav hry -------------")
        for key in self.points:
            print(f"{key}. pole -> kamenů: {self.points[key].count_checkers()}, barva: {self.points[key].owner}")
            if key in [6,12,18]:
                print()

    def move(self, from_point: int, to_point: int) -> None:
        checker = self.points[from_point].remove_checker()
        if checker:
            if not self.points[to_point].add_checker(checker):
                self.points[from_point].add_checker(checker)
        else:
            print('Přesun neproběhl.')



# Herní kámen (s pamětí, kde se postupně nacházel)
class Checker:
    def __init__(self, owner, checker_id: int) -> None:
        self.next_checker = None
        self.id = checker_id
        self.owner = owner
        pass

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

    def remove_checker(self) -> Checker:
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

# Bar (továrna na herní kameny, s řízenou produkcí)
class Bar:
    def __init__(self) -> None:
        pass

# Hráč
class Player:
    def __init__(self) -> None:
        pass

class ConsolePlayer(Player):
    pass

class AIPlayer(Player):
    pass

game = Game()

game.points[1].add_checker(Checker("bílý", 1))
game.points[1].add_checker(Checker("bílý", 2))
game.points[1].add_checker(Checker("bílý", 2))
game.points[1].add_checker(Checker("bílý", 2))
game.points[2].add_checker(Checker("černý", 2))
game.display()
game.move(1,3)
game.move(1,3)
game.move(1,3)
game.move(1,3)
game.move(2,3)
game.display()