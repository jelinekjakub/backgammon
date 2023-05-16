from double_dice import *
import verification
from game import *

game = Game()
game.display()
print(game.valid_moves(19, [1,6]))