from prettytable import PrettyTable
import ctypes

kernel32 = ctypes.windll.kernel32
kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)

# ANSI Escape Sequences (https://gist.github.com/fnky/458719343aabd01cfb17a3a4f7296797)

PLAYER_WHITE = 0
PLAYER_BLACK = 1

CHECKER_WHITE = " ◯ "
CHECKER_BLACK = " ● "
CHECKER_WHITE_ACTIVE = " ⚪ "
CHECKER_BLACK_ACTIVE = " ⚫ "
DOUBLE_DICE = "🎲🎲"

def disable_utf():
    global CHECKER_WHITE
    global CHECKER_BLACK
    global CHECKER_WHITE_ACTIVE
    global CHECKER_BLACK_ACTIVE
    global DOUBLE_DICE

    CHECKER_WHITE = "\033[37m o \033[0;30;43m"
    CHECKER_BLACK = " o "
    CHECKER_WHITE_ACTIVE = "\033[37m o \033[0;30;43m"
    CHECKER_BLACK_ACTIVE = " o "
    DOUBLE_DICE = "Kostka"

# ⚪⚫◯

class Text:
    def bold(self, text):
        return "\033[1;33;43m"+text+"\033[0;30;43m"
    
    def highlight(self, text):
        return "\033[2;33;43m"+text+"\033[0;30;43m"
    
    def error(self, text):
        return "\033[2;31;43m"+text+"\033[0;30;43m"
    
    def info(self, text):
        return "\033[2;36;43m"+text+"\033[0;30;43m"
    
    def blue(self, text):
        return "\033[2;34;43m"+text+"\033[0;30;43m"
    

class Display():
    def __init__(self) -> None:
        self.table = PrettyTable()
        self.table.header = False
        self.table.title = "Herní deska"
        self.dice = PrettyTable()
        self.dice.header = False
        self.dice.title = DOUBLE_DICE
        self.bar = PrettyTable()
        self.bar.header = False
        self.init_colors()

    def title(self) -> None:
        print(Text().highlight("Vrchcáby"))

    def clear(self):
        print('\033[2J')
    
    def set_error(self, message: str) -> None:
        self.table.title = Text().error(message)

    def set_message(self, message: str) -> None:
        self.table.title = Text().info(message)    

    def reset_message(self) -> None:
        self.table.title = "Herní deska"

    def game_board(self, keys, data, now_plaing, selected:list):
        height = 0
        for key in keys:
            if data[key].count_checkers() > height:
                height = data[key].count_checkers()
        
        difference = 1
        for key in range(11, -1, -1):
            checkers = []
            checkers.append(str(key+1))
            if data[keys[key]].get_color() == PLAYER_WHITE:
                if now_plaing == PLAYER_WHITE:
                    checker = CHECKER_WHITE_ACTIVE
                else:
                    checker = CHECKER_WHITE
            else:
                if now_plaing == PLAYER_BLACK:
                    checker = CHECKER_BLACK_ACTIVE
                else:
                    checker = CHECKER_BLACK

            if data[keys[key+difference]].get_color() == PLAYER_WHITE:
                if now_plaing == PLAYER_WHITE:
                    checker_opposite = CHECKER_WHITE_ACTIVE
                else:
                    checker_opposite = CHECKER_WHITE
            else:
                if now_plaing == PLAYER_BLACK:
                    checker_opposite = CHECKER_BLACK_ACTIVE
                else:
                    checker_opposite = CHECKER_BLACK

            for i in range(data[keys[key]].count_checkers()):
                if key+1 in selected:
                    checkers.append((f"\033[41m{checker}\033[0;30;43m"))
                else:
                    checkers.append(checker)

            if data[keys[key]].count_checkers() < height:
                for i in range(data[keys[key]].count_checkers(), height):
                    if key+1 in selected:
                        if data[keys[key]].count_checkers() == 0:
                            checkers.append(("\033[41m \033[0;30;43m"))
                        else:
                            checkers.append(" ")
                    else:
                        checkers.append(" ")

            checkers.append("-")

            if data[keys[key+difference]].count_checkers() < height:
                for i in range(data[keys[key+difference]].count_checkers(), height):
                    if key+difference+1 in selected:
                        if data[keys[key+difference]].count_checkers() == 0:
                            checkers.append(("\033[41m \033[0;30;43m"))
                        else:
                            checkers.append(" ")
                    else:
                        checkers.append(" ")

            for i in range(data[keys[key+difference]].count_checkers()):
                if key+difference+1 in selected:
                    checkers.append((f"\033[41m{checker_opposite}\033[0;30;43m"))
                else:
                    checkers.append(checker_opposite)

            
            checkers.append(str(key+difference+1))

            self.table.add_column(keys[key], checkers)

            difference = difference + 2
        
        print(self.table)
        self.table.clear()
        self.dice.clear()

    def bar_refactor(self, checkers):
        refactored = []
        for item in checkers:
            if item.color == PLAYER_WHITE:
                refactored.append(CHECKER_WHITE_ACTIVE)
            else:
                refactored.append(CHECKER_BLACK_ACTIVE)
        return refactored

    def author(self):
        self.clear()
        print("Autor: Jakub Jelínek\n2023")

    def reset_console(self):
        print('\033[2J')
        print("\033[0m")

    def init_colors(self):
        self.clear()
        print("\033[0;30;43m")

    def welcome(self):
        self.clear()
        print("Vrchcáby\n\n")
        print(f"1: {Text().blue('Nová hra')}\n2: {Text().blue('Načíst poslední uloženou hru')}\n3: {Text().blue('Autor')}\n4: {Text().blue('Ukončit')}")

    def graphics_mode(self):
        self.clear()
        print("Vrchcáby\n\n")
        print("Zobrazují se vám všechny znaky níže správně?")
        print(f"{CHECKER_WHITE} {CHECKER_BLACK} {CHECKER_WHITE_ACTIVE} {CHECKER_BLACK_ACTIVE} {DOUBLE_DICE}\n\n")
        print(f"1: {Text().blue('ANO (spustí hru s pokročilou znakovou sadou)')}\n2: {Text().error('NE (spustí hru se základní znakovou sadou)')}")
        print(f"\n{Text().highlight('Pokud se vám nezobrazují znaky správně, a přesto chcete používat pokročilou grafiku ve vaší konzoli, spusťte hru v konzoli podporující znaky UNICODE. Windows 11 - nativně, Windows 10: https://apps.microsoft.com/store/detail/windows-terminal/9N0DX20HK701')}")

    def double_dice(self, numbers):
        self.dice.add_row(numbers)

        print(self.dice)

    def bars(self, bars):
        if bars[0].has_any or bars[1].has_any:
            self.bar.add_row(["Bar"] + self.bar_refactor(bars[0].checkers) + self.bar_refactor(bars[1].checkers))
            print(self.bar)
            self.bar.clear()

    def render(self, game, dice, selected=[]):
        self.clear()
        self.title()
        self.game_board(game.keys.primary, game.points, game.now_playing, selected)
        self.bars(game.bars)
        self.double_dice(dice)

        self.reset_message()
