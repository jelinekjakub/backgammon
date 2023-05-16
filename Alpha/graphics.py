from prettytable import PrettyTable

PLAYER_WHITE = 0
PLAYER_BLACK = 1

class Text:
    def bold(self, text):
        return "\033[1;33;43m"+text+"\033[0;33;43m"
    
    def highlight(self, text):
        return "\033[2;33;43m"+text+"\033[0;33;43m"

class Display():
    def __init__(self) -> None:
        self.table = PrettyTable()
        self.table.header = False
        self.table.title = "Herní deska"

    def render(self, keys, data):
        height = 0
        for key in keys:
            if data[key].count_checkers() > height:
                height = data[key].count_checkers()
        
        difference = 1
        for key in range(11, -1, -1):
            checkers = []
            checkers.append(str(key+1))
            if data[keys[key]].get_color() == PLAYER_WHITE:
                checker = "⚪"
            else:
                checker = "⚫"

            if data[keys[key+difference]].get_color() == PLAYER_WHITE:
                checker_opposite = "⚪"
            else:
                checker_opposite = "⚫"

            for i in range(data[keys[key]].count_checkers()):
                checkers.append(checker)

            if data[keys[key]].count_checkers() < height:
                for i in range(data[keys[key]].count_checkers(), height):
                    checkers.append("")

            checkers.append("-")

            if data[keys[key+difference]].count_checkers() < height:
                for i in range(data[keys[key+difference]].count_checkers(), height):
                    checkers.append("")

            for i in range(data[keys[key+difference]].count_checkers()):
                checkers.append(checker_opposite)

            
            checkers.append(str(key+difference+1))

            self.table.add_column(keys[key], checkers)

            difference = difference + 2

        print("\033[0;30;43m")
        print(self.table)
        #print("\033[0m")

        
def test():
    print("\033[0;33;43m")
    table = PrettyTable()
    table.header = False
    table.title = "Herní deska"
    table.add_row(["12", "11", "10", "09", "08", "07", "Bar", "06", "05", "04", "03", "02", "01"], divider=True)
    table.add_row(["⬤","","","","⚪","","",Text().highlight("⚪ "),"","","","","⬤"])
    table.add_row(["⬤","","","","⚪","","",Text().highlight("⚪ "),"","","","","⬤"])
    table.add_row(["⬤","","","","⚪","","",Text().highlight("⚪ "),"","","","",""])
    table.add_row(["⬤","","","","","","",Text().highlight("⚪ "),"","","","",""])
    table.add_row(["⬤","","","","","","",Text().highlight("⚪ "),"","","","",""])
    table.add_row(["-","-","-","-","-","-","","-","-","-","-","-","-"])
    #table.add_row(["","","","","","","","","","","","",""])
    table.add_row(["⚪","","","","","","","⬤","","","","",""])
    table.add_row(["⚪","","","","","","","⬤","","","","",""])
    table.add_row(["⚪","","","","⬤","","","⬤","","","","",""])
    table.add_row(["⚪","","","","⬤","","","⬤","","","","","⚪"])
    table.add_row(["⚪","","","","⬤","","","⬤","","","","","⚪"], divider=True)
    table.add_row(["13", "14", "15", "16", "17", "18", "Bar", "19", "20", "21", "22", "23", "24"])

    print(table)

    print("\033[2;33;43m")
    print("Tohle je zpráva")
    print("\033[0m")