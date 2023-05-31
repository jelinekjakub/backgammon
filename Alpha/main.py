from double_dice import *
import verification
import graphics
from game import *

PLAYER_WHITE = 0
PLAYER_BLACK = 1


# game.load()
# game.display()

# Pro zapnutí základní znakové sady odkomentovat
# graphics.disable_utf()

# Co ještě chybí
# Vyvádění z pole ven
# ládování z jsonu
# Random hráč / AI
# počet vyvedených kamenů
# po výhře typ výhry
# po ukončení se zobrazí statistika o všech kamenech ve hře (zvlášť pro bílého a černého), například:
#   počet kamenů vyhozených, vyvedených a opuštěných
#   průměrná životnost kamene v tazích


def play():
    pick1 = None
    while pick1 != 0:
        if game.rolled_history != []:
            rolled = game.rolled_history
        else:
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
                print("Kol odehráno: ", game.rounds_played)
                print("is_bearing_off:" ,game.is_bearing_off())
                pick1 = input("Vyberte (0 Ukončí hru): ")
                if pick1 == 0:
                    if not game.quit_game():
                        continue
                if not verification.list_int(pick1, valid_points+[0]):
                    display.set_error("Zadán neplatný znak")
                    continue
            
            pick1 = int(pick1)
            if pick1 == 0 and not game.bars[game.now_playing].has_any:
                # game.rolled_history = rolled
                break
            valid_moves = game.valid_moves(pick1, rolled)
            if valid_moves == []:
                display.set_error("Hráč nemůže hrát nemá žádné dostupné taky, hraje další.")
                break
            display.render(game, dice=rolled, selected=valid_moves)
            print("Kam přesunout: ", valid_moves)
            pick2 = input("Vyberte (ENTER zrušit): ")
            if pick2 == 0 or not verification.list_int(pick2, valid_moves):
                display.set_error("Zadán neplatný znak")
                continue
            pick2 = int(pick2)
            rolled.remove(game.move(pick1-1, pick2-1))
        
        game.save()
        
        if pick1 == 0 and game.bars[game.now_playing].has_any:
            pick1 = None

        if pick1 != 0:
            game.switch_players()


     

intro_display = graphics.Display()

mode = None
graphics_mode = None

while graphics_mode not in ["1", "2"]:
    intro_display.graphics_mode()
    graphics_mode = input(">")

if graphics_mode == "2":
    graphics.disable_utf()

display = graphics.Display()

while mode != "4":
    mode = 0
    while mode not in ["1","2","3","4"]:
        display.welcome()
        mode = input()
    if mode == "4":
        break
    elif mode == "3":
        display.author()

        print("\nDo menu stiskem ENTER...")
        input()
    elif mode == "2":
        display.clear()
        if not verification.save_exists():
            print(graphics.Text().error("Není dostupný žádný SAVE! Vytvořte novou hru."))

        print("\nDo menu stiskem ENTER...")
        input()
    else:
        game = Game()
        print(game.list_saves())
        input()
        dice = DoubleDice()
        play()
        print("Konec hry")
        input()

display.reset_console()