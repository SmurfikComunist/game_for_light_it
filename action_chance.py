import attr
from typing import Any


@attr.s(auto_attribs=True)
class ActionChance:
    """
    A class that represents the chance of an action and
    when you need to enable it.
    :var chance: Chance of action [0.0 - 1.0].
    :var condition: The condition under which you need to change the chance.
    :var enabled: Shows whether the chance is enabled or not.
    """
    chance: float
    condition: Any
    enabled: bool
