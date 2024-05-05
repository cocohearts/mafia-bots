class TestBot:
    def __init__(self, prompts):
        self.prompts = prompts

    def connect(self,identity):
        self.identity = identity
        self.prompt = f'\nNames are {self.identity.game.names}'
        self.prompt += f'\nRoles are {self.identity.game.roles}'
        self.prompt += f'\nYour name is {self.identity.name}'
        self.prompt += f'\n{self.prompts[identity.role]}'

    def send(self, message):
        print(f'{message}\n\n{self.prompt}')
    
    def respond(self):
        answer = input('Enter your response: ')
        print("\n\n")
        return answer
    
    def got_killed(self):
        print('You have been killed.')
    
    def vote(self):
        return input('Enter your vote:')