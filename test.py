from client import TestBot
# import asyncio
from framework import Game, Identity

names = ['Alice', 'Bob', 'Charlie']
prompts = {
    'Doctor' : 'You are the Doctor. Who would you like to heal?\n',
    'Cop' : 'You are the Cop. Who would you like to investigate?\n',
    'Mafia' : 'You are the Mafia. Who would you like to kill?\n',
    'Villager' : 'You are a Villager. You have no special abilities.\n'
}
roles = ['Mafia', 'Cop', 'Doctor']

def main():
    my_game = Game(roles, names)
    clients = [TestBot(prompts) for _ in range(3)]
    my_game.connect(clients)
    my_game.play()

# Run the main function until it is complete
main()