from collections import Counter
import random

class Identity:
    """
    Represents a participant in the game with a specific role, managing the participant's actions, state, and interactions with the game and other participants.
    """
    item_map = {
        'gun': 'shoot gun',
    }
    
    def __init__(self, role, game, client):
        """
        Initializes a new Identity instance.

        Args:
            role (str): The role of the identity.
            game (Game): The game object to which this identity belongs.
            client: The client interface handling communications.
        """
        self.role = role
        self.actions = Game.role_actions[role]
        self.game = game
        self.items = []
        self.alive = True
        self.blocked = False
        self.protected = False
        self.client = client

    def speak(self, message):
        """
        Adds a message to the game's transcript as spoken by this identity.

        Args:
            message (str): The message to be spoken.
        """
        self.game.transcript.append(f"{self.role} says: {message}")

    def listen(self):
        """
        Generates and returns a summary of the game's current state from this identity's perspective.

        Returns:
            str: A summary of the current state.
        """
        text = f"The transcript of the game so far: {self.game.transcript}"
        text += f"\nYour role is {self.role}."
        text += f"\nYou can take the following actions: {self.actions}"
        text += f"\nYou have the following items: {self.items}"
        return text

    def take_action(self, action, target):
        """
        Executes a specified action against a target identity if possible.

        Args:
            action (str): The action to be taken.
            target (Identity): The target of the action.
        """
        if self.blocked or action not in self.actions or not target.alive:
            return

        if action == 'give gun':
            target.items.append('gun')
        if action == 'shoot gun':
            target.alive = False
        if action == 'block':
            target.blocked = True
        if action == 'heal':
            target.protected = True
    
    async def night_turn(self):
        """
        Handles the actions and interactions for this identity during the night phase of the game.
        """
        if self.alive:
            self.client.send(self.listen())
            response = await self.client.respond()
            if response:
                action, target = response.split()
                self.take_action(action, target)

    async def day_turn(self):
        """
        Handles the actions and interactions for this identity during the day phase of the game.
        """
        if self.alive:
            self.client.send(self.listen())
            response = await self.client.respond()
            if response:
                speech = response.split()
                self.speak(speech)

    def get_killed(self):
        """
        Marks this identity as not alive if it is not protected.
        """
        if not self.protected:
            self.alive = False

class Game:
    """
    Manages the entire game, including the sequence of events, game rounds, and the status of all identities.
    """
    role_actions = {
        'Mafia': ['kill'],
        'Villager': [],
        'Arms Dealer': ['give gun'],
        'Doctor': ['heal'],
        'Cop': ['investigate'],
        'Bartender': ['block'],
    }

    role_alignments = {
        'Mafia': 'Mafia',
        'Villager': 'Town',
        'Arms Dealer': 'Town',
        'Doctor': 'Town',
        'Cop': 'Town',
        'Bartender': 'Town',
    }

    acting_order = ['Bartender', 'Arms Dealer', 'Cop', 'Doctor', 'Mafia', 'Villager']

    def __init__(self, roles):
        """
        Initializes a new Game instance with specified roles.

        Args:
            roles (list): A list of roles to be assigned to the identities in the game.
        """
        roles = sorted(roles, key=self.acting_order.index)
        self.identities = [Identity(role, self) for role in roles]
        self.transcript = []

    def night(self):
        """
        Executes the night phase of the game, allowing each identity to perform night actions.
        """
        for identity in self.identities:
            if identity.alive:
                action = identity.night_turn()
                self.resolve_action(identity, action)
        for identity in self.identities:
            identity.blocked = False
            identity.protected = False
    
    def day(self):
        """
        Executes the day phase of the game, involving discussion and voting processes among identities.
        """
        for speaking_round in range(2):
            order = random.shuffle(self.identities)
            for identity in order:
                if identity.alive:
                    identity.day_turn()

        votes = [identity.vote() for identity in self.identities]
        vote_counts = Counter(votes)
        max_votes = max(vote_counts.values())
        most_voted = [name for name, count in vote_counts.items if count == max_votes]
        chosen = random.choice(most_voted) 
        if chosen=='no one':
            return
        chosen.get_killed()

    def start_round(self):
        """
        Starts a new round of the game, consisting of both night and day phases.
        """
        self.night()
        self.day()
    
    def play(self):
        """
        Begins and manages the sequence of rounds until the game is over.
        """
        while not self.game_over():
            self.start_round()
    
    def game_over(self):
        """
        Determines whether the game has ended based on the number of Mafia and Town members still alive.

        Returns:
            bool: True if the game is over, False otherwise.
        """
        mafia_count = sum(1 for identity in self.identities if identity.role == 'Mafia' and identity.alive)
        town_count = sum(1 for identity in self.identities if identity.role != 'Mafia' and identity.alive)
        return mafia_count >= town_count
