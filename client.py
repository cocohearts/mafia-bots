class TestBot:
    def __init__(self, prompts):
        self.prompts = prompts

    def connect(self,identity):
        self.prompt = self.prompts[identity.role]
        self.identity = identity

    def send(self, message):
        print("\n\n")
        print(f'{self.prompt}{message}')
    
    def respond(self):
        print(f'Names are {self.identity.game.names}')
        print(f'Your name is {self.identity.name}')
        return input('Enter your response: ')
    
    def got_killed(self):
        print('You have been killed.')