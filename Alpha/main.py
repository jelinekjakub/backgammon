from double_dice import *
import verification
import graphics
from game import *

PLAYER_WHITE = 0
PLAYER_BLACK = 1

game = Game()
display = graphics.Display()
dice = DoubleDice()
# game.load()
# game.display()

# Pro zapnutí základní znakové sady odkomentovat
# graphics.disable_utf()

# print(game.valid_moves(19, [1,6]))
print(u'\u2713')
while True:
    rolled = dice.roll()
    pick1 = None
    pick2 = None
    while rolled:
        if game.bars[game.now_playing].has_any:
            if game.now_playing == PLAYER_WHITE:
                pick1 = 0
            else:
                pick1 = 25
        else:
            valid_points = game.valid_points(rolled)
            
            display.render(game, dice=rolled, selected=valid_points)
            print("Nyní na tahu:", game.now_playing)
            print("is_bearing_off:" ,game.is_bearing_off())
            pick1 = input("Vyberte: ")
            if pick1 == 0:
                if not game.quit_game():
                    continue
            if not verification.list_int(pick1, valid_points):
                display.set_error("Zadán neplatný znak")
                continue
        
        pick1 = int(pick1) #type: ignore
        
        valid_moves = game.valid_moves(pick1, rolled)
        if valid_moves == []:
            display.set_error("Hráč nemůže hrát nemá žádné dostupné taky, hraje další.")
            break
        display.render(game, dice=rolled, selected=valid_moves)
        print("Kam přesunout: ", valid_moves)
        pick2 = input("Vyberte: ")
        if pick2 == 0 or not verification.list_int(pick2, valid_moves):
            display.set_error("Zadán neplatný znak")
            continue
        pick2 = int(pick2)
        rolled.remove(game.move(pick1-1, pick2-1))

    game.save()
    game.switch_players()

