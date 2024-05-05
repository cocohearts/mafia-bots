from framework import Game
from console_bot import TestBot

names = ['Alice', 'Bob', 'Charlie']
prompts = {
    'Doctor' : 'You are the Doctor. Who would you like to heal?\n',
    'Cop' : 'You are the Cop. Who would you like to investigate?\n',
    'Mafia' : 'You are the Mafia. Who would you like to kill?\n',
    'Villager' : 'You are a Villager. You have no special abilities.\n'
}
roles = ['Mafia', 'Cop', 'Doctor']

def main():
    clients = [TestBot(prompts) for _ in range(3)]
    my_game = Game(roles, names, clients)
    my_game.play()

main()