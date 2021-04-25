from typing import List, Dict, Callable

from player import BasePlayer, Computer, Human
from utils import system_random


class Game:
    """
    A class for controlling the game.
    """

    @staticmethod
    def choose_player(players: List[BasePlayer]) -> BasePlayer:
        """
        Returns a randomly selected player from all players.
        :param players: List of players.
        :return: Selected player.
        """
        return system_random.choice(players)

    @staticmethod
    def choose_action(actions_chances: Dict[Callable, float]) -> Callable:
        """
        Returns a randomly selected action from all actions,
        using their weights(chances).
        :param actions_chances: List of actions.
        :return: Selected action.
        """
        population: List[Callable] = []
        weights: List[float] = []
        for key, value in actions_chances.items():
            population.append(key)
            weights.append(value)

        return system_random.choices(population=population, weights=weights)[0]

    @staticmethod
    def print_players_health(players: List[BasePlayer]):
        """
        Print the names and health of all players.
        :param players: List of players.
        :return: None.
        """
        for player in players:
            print(f"{player.name} has {player.health} health points.")


def main():
    players: List[BasePlayer] = [
        Computer(name="Computer", health=100),
        Human(name="Human", health=100)
    ]

    print("Start game.")
    while True:
        print()
        selected_player: BasePlayer = Game.choose_player(players=players)
        selected_action: Callable = Game.choose_action(
            actions_chances=selected_player.actions_chances
        )
        selected_action()

        Game.print_players_health(players=players)
        if not selected_player.is_live:
            print(f"\nPlayer {selected_player.name} died.")
            print("Finish game.")
            break


if __name__ == "__main__":
    main()
