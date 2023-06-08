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
    # Tučný text
    def bold(self, text):
        return "\033[1;33;43m"+text+"\033[0;30;43m"
    
    # Zvýrazněný text
    def highlight(self, text):
        return "\033[2;33;43m"+text+"\033[0;30;43m"
    
    # Červený text
    def error(self, text):
        return "\033[2;31;43m"+text+"\033[0;30;43m"
    
    # Světle modrý text
    def info(self, text):
        return "\033[2;36;43m"+text+"\033[0;30;43m"
    
    # Tmavě modrý text
    def blue(self, text):
        return "\033[2;34;43m"+text+"\033[0;30;43m"
    

class Display():
    # Inicializace displeje
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

    # Název
    def title(self) -> None:
        print(Text().highlight("Vrchcáby"))

    # Vyčistí konzoli
    def clear(self):
        print('\033[2J')
    
    # Nastaví error
    def set_error(self, message: str) -> None:
        self.table.title = Text().error(message)

    # Nastaví zprávu
    def set_message(self, message: str) -> None:
        self.table.title = Text().info(message)    

    # Vyresetuje zprávu
    def reset_message(self) -> None:
        self.table.title = "Herní deska"

    # Zobrazí herní desku
    def game_board(self, keys, data, now_plaing, selected:list, homes, bars):
        height = 0
        
        for key in keys:
            if data[key].count_checkers() > height:
                height = data[key].count_checkers()
        if height < len(homes[0].checkers):
            height = len(homes[0].checkers)
        if height < len(homes[1].checkers):
            height = len(homes[1].checkers)

        empty_col = []
        for i in range(height+1):
            empty_col.append("\033[40m \033[0;30;43m")
        empty_col.append("-")
        for i in range(height+1):
            empty_col.append("\033[47m \033[0;30;43m")
        

        checkers_bar = []
        checkers_bar.append("Bar")
        for i in range(len(bars[1].checkers)):
            checkers_bar.append(CHECKER_BLACK_ACTIVE)
        for i in range(0, height - len(bars[1].checkers)):
            checkers_bar.append(" ")
        checkers_bar.append("-")
        for i in range(0, height - len(bars[0].checkers)):
            checkers_bar.append(" ")
        for i in range(len(bars[0].checkers)):
            checkers_bar.append(CHECKER_WHITE_ACTIVE)
                
        checkers_bar.append("Bar")
        self.table.add_column(300, checkers_bar)

        self.table.add_column(200, empty_col)

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
        
        self.table.add_column(100, empty_col)

        checkers_home = []
        checkers_home.append("0")
        for i in range(len(homes[1].checkers)):
            if 0 in selected:
                checkers_home.append(f"\033[41m{CHECKER_BLACK_ACTIVE}\033[0;30;43m")
            else:
                checkers_home.append(CHECKER_BLACK_ACTIVE)
        for i in range(0, height - len(homes[1].checkers)):
            if 0 in selected:
                checkers_home.append(f"\033[41m \033[0;30;43m")
            else:
                checkers_home.append(" ")
        checkers_home.append("-")
        for i in range(0, height - len(homes[0].checkers)):
            if 25 in selected:
                checkers_home.append(f"\033[41m \033[0;30;43m")
            else:
                checkers_home.append(" ")
        for i in range(len(homes[0].checkers)):
            if 25 in selected:
                checkers_home.append(f"\033[41m{CHECKER_WHITE_ACTIVE}\033[0;30;43m")
            else:
                checkers_home.append(CHECKER_WHITE_ACTIVE)
                
        checkers_home.append("25")
        self.table.add_column(0, checkers_home)

        print(self.table)
        self.table.clear()
        self.dice.clear()

    # Refaktorizace baru z čísel barev na kameny
    def bar_refactor(self, checkers):
        refactored = []
        for item in checkers:
            if item.color == PLAYER_WHITE:
                refactored.append(CHECKER_WHITE_ACTIVE)
            else:
                refactored.append(CHECKER_BLACK_ACTIVE)
        return refactored

    # Zobrazí autora
    def author(self):
        self.clear()
        print("Autor: Jakub Jelínek\n2023")

    # Resetuje nastavení konzole
    def reset_console(self):
        print('\033[2J')
        print("\033[0m")

    # Inicializuje barevnou konzoli
    def init_colors(self):
        self.clear()
        print("\033[0;30;43m")

    # Uvítací obrazovka (hlavní menu)
    def welcome(self):
        self.clear()
        print("Vrchcáby\n\n")
        print(f"1: {Text().blue('Nová hra')}\n2: {Text().blue('Načíst hru ...')}\n3: {Text().blue('Autor')}\n4: {Text().blue('Ukončit')}")

    # Volba grafického módu
    def graphics_mode(self):
        self.clear()
        print("Vrchcáby\n\n")
        print("Zobrazují se vám všechny znaky níže správně?")
        print(f"{CHECKER_WHITE} {CHECKER_BLACK} {CHECKER_WHITE_ACTIVE} {CHECKER_BLACK_ACTIVE} {DOUBLE_DICE}\n\n")
        print(f"1: {Text().blue('ANO (spustí hru s pokročilou znakovou sadou)')}\n2: {Text().error('NE (spustí hru se základní znakovou sadou)')}")
        print(f"\n{Text().highlight('Pokud se vám nezobrazují znaky správně, a přesto chcete používat pokročilou grafiku ve vaší konzoli, spusťte hru v konzoli podporující znaky UNICODE. Windows 11 - nativně, Windows 10: https://apps.microsoft.com/store/detail/windows-terminal/9N0DX20HK701')}")

    # Zobrazí dvojkostku
    def double_dice(self, numbers):
        if numbers != []:
            self.dice.add_row(numbers)
        else:
            self.dice.add_row([" ", " "])

        print(self.dice)

    # Zobrazí statistiku
    def stats(self, checkers, lifespan):
        checkers1 = dict()
        checkers2 = dict()
        for checker_id in checkers:
            if checker_id % 2 == 0:
                checkers1[checker_id] = checkers[checker_id]
            else:
                checkers2[checker_id] = checkers[checker_id]
        
        bar1 = 0
        home1 = 0
        bar2 = 0
        home2 = 0
        for checker_id in checkers1:
            bar1 += checkers1[checker_id].point_history.count("bar")
        for checker_id in checkers1:
            home1 += checkers1[checker_id].point_history.count("home")
        for checker_id in checkers2:
            bar2 += checkers2[checker_id].point_history.count("bar")
        for checker_id in checkers2:
            home2 += checkers2[checker_id].point_history.count("home")

        
        print("\n\nBílý:")
        print(f"Kamenů opuštěných: {bar1}")
        print(f"Kamenů vyhozených: {bar2}")
        print(f"Kamenů vyvedených: {home1}")
        print(f"Průměrná životnost v tazích: {round(lifespan[0], 2)}")
        print("\nKameny")
        for checker_id in checkers1:
            print(f"ID: {checker_id if checker_id > 9 else '0' + str(checker_id)} {CHECKER_WHITE_ACTIVE if checkers1[checker_id].color == PLAYER_WHITE else CHECKER_BLACK_ACTIVE} HISTORIE POLÍ: {checkers1[checker_id].point_history}")
        

        print("\nČerný:")
        print(f"Kamenů opuštěných: {bar2}")
        print(f"Kamenů vyhozených: {bar1}")
        print(f"Kamenů vyvedených: {home2}")
        print(f"Průměrná životnost v tazích: {round(lifespan[1], 2)}")
        print("\nKameny")
        for checker_id in checkers2:
            print(f"ID: {checker_id if checker_id > 9 else '0' + str(checker_id)} {CHECKER_WHITE_ACTIVE if checkers2[checker_id].color == PLAYER_WHITE else CHECKER_BLACK_ACTIVE} HISTORIE POLÍ: {checkers2[checker_id].point_history}")

    # Zobrazí bar
    def bars(self, bars):
        if bars[0].has_any or bars[1].has_any:
            self.bar.add_row(["Bar"] + self.bar_refactor(bars[0].checkers) + self.bar_refactor(bars[1].checkers))
            print(self.bar)
            self.bar.clear()

    # Zobrazuje hru, bar, kostku
    def render(self, game, dice, selected=[]):
        self.clear()
        self.title()
        self.game_board(game.keys.primary, game.points, game.now_playing, selected, game.homes, game.bars)
        self.bars(game.bars)
        self.double_dice(dice)

        self.reset_message()

    # Zobrazí výběr herního módu
    def ai_console_select(self):
        self.clear()
        print("Vrchcáby\n\n")
        print("Vyberte herní mód")
        print(f"1: {Text().blue('Hra proti počítači')}\n2: {Text().blue('Hra dvou hráčů')}")