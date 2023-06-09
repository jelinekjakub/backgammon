import verification
import graphics
from game import *
import datetime

PLAYER_WHITE = 0
PLAYER_BLACK = 1


def info():
    print("Nyní na tahu:", graphics.CHECKER_WHITE_ACTIVE if game.now_playing == PLAYER_WHITE else graphics.CHECKER_BLACK_ACTIVE)
    print("Kol odehráno: ", game.rounds_played)

def play():
    pick1 = None
    if not game.finished():
        while pick1 != 0:
            bar_active = False
            if game.rolled_history != []:
                rolled = game.rolled_history
            else:
                display.render(game, dice=[], selected=[])
                info()
                rolled = game.players[game.now_playing].roll_double_dice()
            pick1 = None
            pick2 = None
            while rolled:
                if game.bars[game.now_playing].has_any:
                    bar_active = True
                    if game.now_playing == PLAYER_WHITE:
                        pick1 = 0
                    else:
                        pick1 = 25
                else:
                    valid_points = game.valid_points(rolled)
                    if valid_points == []:
                        display.render(game, dice=rolled, selected=valid_points)
                        display.set_error(f"Hráč {graphics.CHECKER_WHITE_ACTIVE if game.now_playing == PLAYER_WHITE else graphics.CHECKER_BLACK_ACTIVE} nemůže hrát nemá žádné dostupné tahy, hraje další.")
                        print(f"Hráč {graphics.CHECKER_WHITE_ACTIVE if game.now_playing == PLAYER_WHITE else graphics.CHECKER_BLACK_ACTIVE} nemůže hrát nemá žádné dostupné tahy, hraje další.")
                        input("ENTER > ")
                        rolled = []
                        break
                    
                    display.render(game, dice=rolled, selected=valid_points)
                    info()
                    print("0 ukončí hru")
                    pick1 = game.players[game.now_playing].play(valid_points, "Vyberte > ")
                    if pick1 == 0:
                        if not game.quit_game():
                            continue
                        else:
                            break
                    if not verification.list_int(pick1, valid_points+[0]):
                        display.set_error("Zadán neplatný znak")
                        continue
                
                pick1 = int(pick1)
                if pick1 == 0 and not game.bars[game.now_playing].has_any:
                    if not game.quit_game():
                        continue
                    else:
                        break
                valid_moves = game.valid_moves(pick1, rolled)

                # Refaktorizace možných posunů kamenem, pro případ vyvádění ze hry
                move_memory1, move_memory2 = None, None
                for valid_move in valid_moves:
                    if valid_move < 0:
                        if move_memory1 == None:
                            index = valid_moves.index(valid_move)
                            move_memory1 = valid_moves.pop(index)
                        else:
                            index = valid_moves.index(valid_move)
                            move_memory2 = valid_moves.pop(index)
                    if valid_move > 25:
                        if move_memory1 == None:
                            index = valid_moves.index(valid_move)
                            move_memory1 = valid_moves.pop(index)
                        else:
                            index = valid_moves.index(valid_move)
                            move_memory2 = valid_moves.pop(index)
                if move_memory1 is not None or move_memory2 is not None:
                    if move_memory1 < 1: #type: ignore
                        valid_moves.append(0)
                    else:
                        valid_moves.append(25)
                
                # Hráč nemá dostupné tahy
                if valid_moves == []:
                    display.render(game, dice=rolled, selected=valid_moves)
                    display.set_error(f"Hráč {graphics.CHECKER_WHITE_ACTIVE if game.now_playing == PLAYER_WHITE else graphics.CHECKER_BLACK_ACTIVE} nemůže hrát nemá žádné dostupné tahy, hraje další.")
                    print(f"Hráč {graphics.CHECKER_WHITE_ACTIVE if game.now_playing == PLAYER_WHITE else graphics.CHECKER_BLACK_ACTIVE} nemůže hrát nemá žádné dostupné tahy, hraje další.")
                    input("ENTER > ")
                    rolled = []
                    break
                display.render(game, dice=rolled, selected=valid_moves)
                info()
                print("ENTER zruší tah")
                pick2 = game.players[game.now_playing].play(valid_moves, "Vyberte > ")
                if pick2 == 0 or not verification.list_int(pick2, valid_moves):
                    display.set_error("Zadán neplatný znak")
                    continue
                pick2 = int(pick2)
                number_used = game.move(pick1-1, pick2-1)
                if number_used in rolled:
                    rolled.remove(number_used)
                elif move_memory1 != None:
                    rolled.remove(abs(pick1-move_memory1))
                elif move_memory2 != None:
                    rolled.remove(abs(pick1-move_memory2))

                # Je-li hra dokončena cyklus se přeruší
                if game.finished():
                    break
            
            if game.finished():
                game.rolled_history = rolled
                game.save()
                break

            game.rolled_history = rolled
            game.save()
            
            if pick1 == 0 and bar_active == True:
                pick1 = None

            if pick1 != 0:
                game.switch_players()

    if game.finished():
        game_finished()

def game_finished():
    display.clear()
    print("Hra skončila")
    print(graphics.Text().blue("Finální statistika hry"))
    display.stats(game.collect_checkers(), game.get_average_lifespan(), game.victory_type())
    input("ENTER > ")


intro_display = graphics.Display()

mode = None
graphics_mode = None

while graphics_mode not in ["1", "2"]:
    intro_display.graphics_mode()
    graphics_mode = input("> ")

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
        input("ENTER > ")
    elif mode == "2":
        display.clear()
        if not verification.save_exists():
            print(graphics.Text().error("Není dostupný žádný SAVE! Vytvořte novou hru."))

            print("\nDo menu stiskem ENTER...")
            input("ENTER > ")
        else:
            game = Game()
            save_pick = None
            options = list(range(0, len(game.list_saves()) + 1))
            options = list(map(str, options))
            while not save_pick in options:
                print("Vyberte SAVE, který chcete načíst.\n\n")
                for i, save in enumerate(game.list_saves()):
                    save = save.split("\\")[1]
                    save = save.split(".")[0]
                    save = datetime.datetime.strptime(save, "%Y%m%d-%H%M%S")
                    save = datetime.datetime.strftime(save, "%H:%M:%S %d.%m.%Y")
                    save = "SAVE uložen " + save
                    print(f"{i+1}: {graphics.Text().info(save)}")
                save_pick = input("> ")
                if save_pick == "0":
                    break
                else:
                    game.load(game.list_saves()[int(save_pick)-1])
                    play()
        
            display.clear()
            print("\nHra uložena")
            print("\nDo menu stiskem ENTER...")
            input("ENTER > ")
    else:
        game = Game()
        ai_console = None
        while ai_console not in ["1", "2"]:
            display.ai_console_select()
            ai_console = input("> ")
        if ai_console == "1":
            game.players[0] = ConsolePlayer()
            game.players[1] = AIPlayer()
        else:
            game.players[0] = ConsolePlayer()
            game.players[1] = ConsolePlayer()

        game.choose_first()
        play()

        display.clear()
        print("\nHra uložena")
        print("\nDo menu stiskem ENTER...")
        input("ENTER > ")

display.reset_console()