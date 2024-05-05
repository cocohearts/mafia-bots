from bot import Bot
from framework import Game
from dotenv import load_dotenv

names = ['Alice', 'Bob', 'Charlie']
prompts = {
    'Doctor': 'Your goal is to uncover and vote to eliminate the Mafia. Use your powers carefully, and do not reveal that you are the Doctor, otherwise you may be targeted by the Mafia.\n',
    'Cop': 'Your goal is to uncover and vote to eliminate the Mafia. Use your powers carefully, and do not reveal that you are the Cop, otherwise you may be targeted by the Mafia.\n',
    'Mafia': 'Your goal is to kill all of the Townspeople without being revealed and voted off.\n',
    'Villager': 'Your goal is to uncover and vote to eliminate the Mafia.\n'
}

load_dotenv()

roles = ['Mafia', 'Cop', 'Doctor']

def empty_callback(p1,p2):
    pass

def main():
    clients = [Bot(prompts) for _ in range(3)]
    my_game = Game(roles, names, clients, empty_callback)
    my_game.play()


# Run the main function until it is complete
main()
