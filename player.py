import attr
from typing import List, Final, Tuple, Dict, Callable

import utils
from action_chance import ActionChance


@attr.s(auto_attribs=True)
class BasePlayer:
    """
    A class to represent base player.
    :var _name: Player's name.
    :var _health: Player's current health.
    :var _is_live: Indicates whether the player is alive or not.
    When a player's health drops to zero, it means that the player is dead.
    :var actions_chances: Dictionary of chances of each action.
    """
    _name: str
    _health: int
    _is_live: bool = attr.ib(init=False)
    actions_chances: Dict[Callable, float] = attr.ib(init=False)

    def __attrs_post_init__(self) -> None:
        self._is_live = (self.health > 0)
        actions: List[Callable] = [
            self.deal_damage_in_small_range,
            self.deal_damage_in_wide_range,
            self.heal
        ]
        chances: List[float] = \
            utils.get_distributed_chances_from_list(list=actions)

        self.actions_chances = dict(zip(actions, chances))

    @property
    def name(self) -> str:
        """
        The getter of player's name.
        :return: Player's name.
        """
        return self._name
    
    @name.setter
    def name(self, value: str) -> None:
        """
        The setter of player's name.
        :param value: Name to set.
        :return: None.
        """
        self._name = value
    
    @property
    def health(self) -> int:
        """
        The getter of player's health.
        :return: Player's health points.
        """
        return self._health

    @health.setter
    def health(self, value: int) -> None:
        """
        The setter of player's health.
        :param value: Health to set.
        If health is below zero, this means that the player is died.
        :return: None.
        """
        if value > 0:
            self._health = value
        else:
            self._health = 0
            self._is_live = False

    @property
    def is_live(self) -> bool:
        """
        The getter of player's is alive indicator.
        :return: Is alive indicator.
        """
        return self._is_live

    def deal_damage(self, damage_amount: int) -> None:
        """
        Deal damage to player.
        :param damage_amount: Damage amount to deal.
        :return: None.
        """
        self.health -= damage_amount

        print(f"Deal {damage_amount} damage to {self.name}.")

    def deal_damage_in_small_range(self) -> None:
        """
        Deal damage to player in a small range.
        :return: None.
        """
        range: Final[Tuple[int, int]] = (18, 25)

        self.deal_damage(damage_amount=utils.system_random.randint(*range))

    def deal_damage_in_wide_range(self) -> None:
        """
        Deal damage to player in a wide range.
        :return: None.
        """
        range: Final[Tuple[int, int]] = (10, 35)

        self.deal_damage(damage_amount=utils.system_random.randint(*range))

    def heal(self) -> None:
        """
        Heal player.
        :return: None.
        """
        range: Final[Tuple[int, int]] = (18, 25)
        heal_points: int = utils.system_random.randint(*range)

        self.health += heal_points

        print(f"Heal {self.name} by {heal_points} points.")


class Computer(BasePlayer):
    """
    A player's subclass to represent Computer player.
    :var _heal_chance: The chance of healing will be applied when
    the condition for health points is met.
    """
    _heal_chance: ActionChance = \
        ActionChance(chance=0.45, condition=0.35, enabled=False)

    @property
    def heal_chance(self) -> ActionChance:
        """
        The getter of player's heal chance.
        :return: Player's heal chance
        """
        return self._heal_chance

    def deal_damage(self, damage_amount: int) -> None:
        """
        Deal damage to player.
        Increase the chance of healing
        when health points meets the condition for health points.
        Also reduce the chances of other actions.
        :param damage_amount: Damage amount to deal.
        :return: None.
        """
        super().deal_damage(damage_amount=damage_amount)
        if self.is_live and \
                ((self.health / 100) <= self.heal_chance.condition):

            utils.change_item_chance(items_chances=self.actions_chances,
                                     item_key=self.heal,
                                     chance=self.heal_chance.chance)
            self._heal_chance.enabled = True

    def heal(self) -> None:
        """
        Heal player.
        Also disable increased healing chance
        when health points do not meet
        the condition for increased healing chance.
        Also reset chances to defaults for other actions.
        :return: None.
        """
        super().heal()
        if self.heal_chance.enabled and \
                ((self.health / 100) > self.heal_chance.condition):

            utils.set_distributed_chances_to_dict(dict=self.actions_chances)
            self._heal_chance.enabled = False


class Human(BasePlayer):
    """
    A player's subclass to represent Human player.
    """
    pass
