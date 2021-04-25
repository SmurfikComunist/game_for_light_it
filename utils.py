import random
from typing import List, Any, Dict

# Use random.SystemRandom to generate cryptographically secure random numbers
system_random = random.SystemRandom()


def get_distributed_chances_from_list(list: List[Any]) -> List[float]:
    """
    Return list with distributed chances.
    :param list: The list from which its length will be taken
    to calculate the distributed chances.
    :return: List with distributed chances.
    """
    average_chance: float = 1 / len(list)
    return [average_chance for x in range(len(list))]


def set_distributed_chances_to_dict(dict: Dict[Any, float]) -> None:
    """
    Set distributed chances on the passed dictionary.
    :param dict: The dictionary from which its length will be taken
    to calculate the distributed chances.
    :return: None.
    """
    average_chance: float = 1 / len(dict)
    for key in dict.keys():
        dict[key] = average_chance


def change_item_chance(
        items_chances: Dict[Any, float],
        item_key: Any,
        chance: float
) -> None:
    """
    Change the chance to the specified one for one item
    and change the chances for other items to get a total of 1.0 (100%).
    :param items_chances: Dictionary of items and their chances.
    :param item_key: The item to which the chance applies.
    :param chance: Chance value to be applied to the item.
    :return: None.
    """
    if chance > 1.0:
        raise ValueError("Chance can't be greater than 1.0")
    chance_for_rest_items: float = 0.0
    if (1.0 - chance) > 0.0:
        chance_for_rest_items = (1 - chance) / (len(items_chances) - 1)

    for key in items_chances.keys():
        items_chances[key] = chance_for_rest_items

    items_chances.update({item_key: chance})
