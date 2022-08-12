"""The German dice game Kniffel for Python"""

from abc import abstractmethod
import random
from types import NoneType

class Dice:
    def __init__(self) -> None:
        self.pips = None

    def roll(self) -> None:
        self.pips = random.randint(1,6)

class Scoreboard:
    def __init__(self) -> None:
        self.table = {
            'aces':None,
            'twos':None,
            'threes':None,
            'fours':None,
            'fives':None,
            'sixes':None,
            'three_of_a_kind':None,
            'four_of_a_kind':None,
            'full_house':None,
            'small_straight':None,
            'large_straight':None,
            'kniffel':None,
            'chance':None
        }

    def split_dices(self, dices: list[Dice]) -> list[Dice]:
        dices_split = [[] for _ in range(6)]
        for i in range(6):
            dices_split[i] = [dice for dice in dices if dice.pips == i+1]
        return dices_split

    def calculate(self, dices: list[Dice]) -> int:
        sum = 0
        for dice in dices:
            sum += dice.pips
        return sum

    def check_entry(self, category: str, dices: list[Dice]) -> bool:
        if self.table[category] is not None:
            return False
        dices_split = self.split_dices(dices)

        if category == 'three_of_a_kind':
            for d in dices_split:
                if len(d) >= 3:
                    return True
            return False

        elif category == 'four_of_a_kind':
            for d in dices_split:
                if len(d) >= 4:
                    return True
            return False

        elif category == 'full_house':
            two = False
            three = False
            for d in dices_split:
                if len(d) == 2:
                    two = True
                elif len(d) == 3:
                    three = True
            return two and three

        elif category == 'small_straight':
            values = [False for _ in range(6)]
            for i in range(6):
                if len(dices_split[i]) >= 1:
                    values[i] = True
            streak = 0
            for v in values:
                if v:
                    streak += 1
                else:
                    streak = 0
                if streak == 4:
                    return True
            return False

        elif category == 'large_straight':
            values = [False for _ in range(6)]
            for i in range(6):
                if len(dices_split[i]) >= 1:
                    values[i] = True
            streak = 0
            for v in values:
                if v:
                    streak += 1
                else:
                    streak = 0
            if streak != 5:
                return False

        elif category == 'kniffel':
            for d in dices_split:
                if len(d) == 5:
                    return True
            return False
        
        return True

    def enter(self, category: str, dices: list[Dice]) -> None:
        actions = (
            {'aces':0,'twos':1,'threes':2,'fours':3,'fives':4,'sixes':5},
            {'full_house':25,'small_straight':30,'large_straight':40,'kniffel':50}
        )

        if category in actions[0]:
            dices_split = self.split_dices()
            self.table[category] = self.calculate(dices_split(actions[0[category]]))
        elif category in actions[1]:
            self.table[category] = actions[1[category]]
        else:
            self.table[category] = self.calculate(dices)

class Player:
    def __init__(self, name: str) -> None:
        self.name = name
        self.scoreboard = Scoreboard()

    def reset(self) -> None:
        self.scoreboard = Scoreboard()

class Game:
    def __init__(self) -> None:
        self.players = []
        self.dices = [Dice() for _ in range(5)]
        self._current_player_index = None
        self.rolls = 0
    
    @property
    def current_player(self) -> Player:
        return self.players[self._current_player]

    @property
    def current_player_index(self) -> int:
        return self.current_player_index

    @current_player_index.setter
    def current_player_index(self, current_player_index:int) -> None:
        self._current_player_index = current_player_index % len(self.players)
    
    def add_player(self, player: Player) -> None:
        self.players.append(player)

    def new_game(self) -> None:
        for p in self.players:
            p.reset()
        self.current_player_index = random.randint(0,len(self.players))

    def move(self, chosen_dices: list[Dice]) -> list[Dice]:
        for dice in chosen_dices:
            dice.roll()
        result = []
        for dice in self.dices:
            result.append(dice.pips)
        if self.rolls == 2:
            self.rolls = 0
            self.current_player_index += 1
        else:
            self.rolls += 1
        return result