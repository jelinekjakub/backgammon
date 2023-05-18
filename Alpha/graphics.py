from prettytable import PrettyTable
import ctypes

kernel32 = ctypes.windll.kernel32
kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)

# ANSI Escape Sequences (https://gist.github.com/fnky/458719343aabd01cfb17a3a4f7296797)

PLAYER_WHITE = 0
PLAYER_BLACK = 1
CHECKER_WHITE = "\033[39m●\033[0;30;43m"
CHECKER_BLACK = "●"
CHECKER_WHITE_ACTIVE = "\033[39m●\033[0;30;43m"
CHECKER_BLACK_ACTIVE = "●"

# ⚪⚫◯

class Text:
    def bold(self, text):
        return "\033[1;33;43m"+text+"\033[0;30;43m"
    
    def highlight(self, text):
        return "\033[2;33;43m"+text+"\033[0;30;43m"
    

class Display():
    def __init__(self) -> None:
        self.table = PrettyTable()
        self.table.header = False
        self.table.title = "Herní deska"
        self.dice = PrettyTable()
        self.dice.header = False
        self.dice.title = "Kostka"

    def title(self) -> None:
        print(Text().highlight("Vrchcáby"))

    def game_board(self, keys, data, now_plaing, selected:list):
        height = 0
        print("selected", selected)
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

    def double_dice(self, numbers):
        self.dice.add_row(numbers)

        print(self.dice)

    def render(self, keys, data, dice_numbers, now_playing, selected=[]):
        print('\033[2J')
        print("\033[0;30;43m")
        self.title()
        self.game_board(keys, data, now_playing, selected)
        self.double_dice(dice_numbers)
        print("\033[0m")
