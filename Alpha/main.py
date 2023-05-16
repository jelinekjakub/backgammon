from double_dice import *
import verification
import graphics
from game import *

game = Game()
dice = DoubleDice()

# print(game.valid_moves(19, [1,6]))
while True:
    print('\033[2J','\033[33m')
    rolled = dice.roll()
    graphics.Display().render(keys=game.keys.primary, data=game.points)
    print("now_playing", game.now_playing)
    print("is_bearing_off:" ,game.is_bearing_off())
    print("Kostky hodily: ", rolled)
    print("Lze vybrat: ", game.valid_points(rolled))
    pick1 = int(input("Vyberte: "))
    print("Kam přesunout: ", game.valid_moves(pick1, rolled))
    pick2 = int(input("Vyberte: "))
    game.move(pick1-1, pick2-1)
    game.switch_players()

