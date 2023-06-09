from random import randint

class DoubleDice:
    def __init__(self) -> None:
        pass

    def roll(self):
        numbers = [randint(1,6), randint(1,6)]
        if numbers[0] == numbers[1]:
            numbers.extend(numbers)
        return numbers
    
class Dice:
    def __init__(self) -> None:
        pass

    def roll(self):
        number = randint(1,6)
        return number