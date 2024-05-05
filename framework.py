from collections import Counter
import random


class Identity:
    """
    Represents a participant in the game with a specific role, managing the participant's actions, state, and interactions with the game and other participants.
    """
    item_map = {
        'gun': 'shoot gun',
    }

    def __init__(self, role, game, client, name):
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
        self.name = name
        self.transcript = []
        self.alignment = Game.role_alignments[role]

    def speak(self, message):
        """
        Adds a message to the game's transcript as spoken by this identity.

        Args:
            message (str): The message to be spoken.
        """
        self.game.broadcast(f"{self.name} says: {message}")

    def heard(self, message):
        """
        Adds a message to the game's transcript as heard by this identity.

        Args:
            message (str): The message to be heard.
        """
        self.transcript.append(f"{message}")

    def listen(self):
        """
        Generates and returns a summary of the game's current state from this identity's perspective.

        Returns:
            str: A summary of the current state.
        """
        text = f"Game history: {self.transcript}"
        return text

    def take_action(self, action, target_name):
        """
        Executes a specified action against a target identity if possible.

        Args:
            action (str): The action to be taken.
            target (Identity): The target of the action.
        """
        # target_index = self.game.names.index(target_name)
        target_index = next((index for index, name in enumerate(
            self.game.names) if name.lower() == target_name.lower()), None)
        target = self.game.identities[target_index]

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
        if action == 'investigate':
            self.heard(f'{target_name} is {target.role}')
        if action == 'kill':
            target.get_killed()

    def night_turn(self):
        """
        Handles the actions and interactions for this identity during the night phase of the game.
        """
        if self.alive:
            self.client.send(self.listen())
            response = self.client.act()
            if response:
                action, target = map(str.lower, response.split())
                self.take_action(action, target)

    def day_turn(self):
        """
        Handles the actions and interactions for this identity during the day phase of the game.
        """
        if self.alive:
            self.client.send(
                f'{self.listen()}. It is Day. Say something and vote.')
            response = self.client.respond()
            if response:
                self.speak(response)

    def get_killed(self):
        """
        Marks this identity as not alive if it is not protected.
        """
        if not self.protected:
            self.alive = False
            self.client.got_killed()
            self.game.broadcast(f'{self.name} has been killed.')
            if result:=self.game.game_over():
                self.game.callback("game_over", self.game.game_over())
        else:
            self.game.broadcast(f'{self.name} was attacked but survived.')

    def vote(self):
        if self.alive:
            self.client.send(
                f'{self.listen()} Who would you like to vote for?')
            return self.client.vote()


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

    acting_order = ['Bartender', 'Arms Dealer',
                    'Cop', 'Doctor', 'Mafia', 'Villager']

    def __init__(self, roles, names, clients, callback):
        """
        Initializes a new Game instance with specified roles.

        Args:
            roles (list): A list of roles to be assigned to the identities in the game.
        """
        roles = sorted(roles, key=self.acting_order.index)
        self.identities = [Identity(role, self, None, names[index]) \
                           for index, role in enumerate(roles)]
        self.transcript = []
        self.names = names
        self.roles = roles

        # General-purpose callback for external updates. Params: message_type, data
        self.callback = callback
        if not self.callback:
            self.callback = lambda x, y: None

        for identity, client in zip(self.identities, clients):
            identity.client = client
            client.connect(identity)

        self.callback("game_start", None)

    def broadcast(self, message):
        self.callback("broadcast", message)
        for identity in self.identities:
            identity.transcript.append(message)

    def night(self):
        """
        Executes the night phase of the game, allowing each identity to perform night actions.
        """
        for identity in self.identities:
            if identity.alive:
                identity.night_turn()
        for identity in self.identities:
            identity.blocked = False
            identity.protected = False

    def day(self):
        """
        Executes the day phase of the game, involving discussion and voting processes among identities.
        """
        for speaking_round in range(2):
            order = random.sample(self.identities, len(self.identities))
            for identity in order:
                if identity.alive:
                    identity.day_turn()

        votes = [identity.vote() for identity in self.identities]
        vote_counts = Counter(votes)
        max_votes = max(vote_counts.values())
        most_voted = [name for name, \
                      count in vote_counts.items if count == max_votes]
        chosen = random.choice(most_voted)
        if chosen == 'nobody':
            return

        self.identities[self.names.index(chosen)].get_killed()
        self.broadcast(f'{chosen} has been lynched.')

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
        while not (result:=self.game_over()):
            self.start_round()
        return result

    def game_over(self):
        """
        Determines whether the game has ended based on the number of Mafia and Town members still alive.

        Returns:
            bool: True if the game is over, False otherwise.
        """
        mafia_count = sum(
            1 for identity in self.identities if identity.role == 'Mafia' and identity.alive)
        town_count = sum(
            1 for identity in self.identities if identity.role != 'Mafia' and identity.alive)
        if mafia_count >= town_count:
            result = "Mafia"
        if mafia_count == 0:
            result = "Town"
        else:
            result = None
        return result
        if result := self.game_over():
            return self.callback("game_over", result)
