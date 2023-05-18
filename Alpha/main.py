from double_dice import *
import verification
import graphics
from game import *

game = Game()
dice = DoubleDice()

# print(game.valid_moves(19, [1,6]))
while True:
    rolled = dice.roll()
    pick1 = None
    while rolled:
        graphics.Display().render(keys=game.keys.primary, data=game.points, dice_numbers=rolled, now_playing=game.now_playing, selected=game.valid_points(rolled))
        print("Nyní na tahu:", game.now_playing)
        print("is_bearing_off:" ,game.is_bearing_off())
        print("Lze vybrat: ", game.valid_points(rolled))
        pick1 = int(input("Vyberte: "))
        if pick1 == 0:
            break
        graphics.Display().render(keys=game.keys.primary, data=game.points, dice_numbers=rolled, now_playing=game.now_playing, selected=game.valid_moves(pick1, rolled))
        print("Kam přesunout: ", game.valid_moves(pick1, rolled))
        pick2 = int(input("Vyberte: "))
        if pick2 == 0:
            continue
        rolled.remove(game.move(pick1-1, pick2-1))
    if pick1 == 0:
        break
    game.switch_players()

