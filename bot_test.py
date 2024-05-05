from bot import Bot
from framework import Game

names = ['Alice', 'Bob', 'Charlie']
prompts = {
    'Doctor' : 'You are the Doctor. Your goal is to uncover and vote to eliminate the Mafia. Use your powers carefully, and do not reveal that you are the Doctor, otherwise you may be targeted by the Mafia.\n',
    'Cop' : 'You are the Cop. Your goal is to uncover and vote to eliminate the Mafia. Use your powers carefully, and do not reveal that you are the Cop, otherwise you may be targeted by the Mafia.\n',
    'Mafia' : 'You are the Mafia. Your goal is to kill all of the Townspeople without being revealed and voted off.\n',
    'Villager' : 'You are a Villager. Your goal is to uncover and vote to eliminate the Mafia.\n'
}

roles = ['Mafia', 'Cop', 'Doctor']

def main():
    clients = [Bot(prompts) for _ in range(3)]
    my_game = Game(roles, names, clients)
    my_game.play()

# Run the main function until it is complete
main()