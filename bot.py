import octoai
import json
from octoai.client import OctoAI
from octoai.text_gen import ChatMessage
import os
from dotenv import load_dotenv
import random

import logging
import sys
logging.basicConfig(stream=sys.stderr, level=logging.INFO)

# logging.debug('A debug message!')

# logging.info('We processed %d records', len(processed_records))

# load_dotenv()
octoai = OctoAI()


class LLM:
    def __init__(self, prompt):
        self.prompt = prompt

    def call(self, query, action="speak"):
        rules = {
            "speak": "\nSpeak to the rest of the players. Communicate or obfuscate your intentions. You only have 100 tokens.",
            "act": "\nChoose an action. You must respond with exactly two words, the first being your action, and the second being the name of your target (could be yourself).",
            "vote": "\nVote someone to kill. You must respond with exactly one word, the name of the person you want to vote for."
        }
        logging.info(self.prompt)
        logging.info(query + rules[action])
        completion = octoai.text_gen.create_chat_completion(
            model="llama-2-70b-chat",
            messages=[
                ChatMessage(role="system", content=self.prompt),
                ChatMessage(role="user", content=query + rules[action]),
            ],
            max_tokens=100,
        )
        response = completion.choices[0].message.content
        logging.info(response)
        return response


class Bot:
    def __init__(self, prompts):
        self.prompts = prompts

    def connect(self, identity):
        self.identity = identity
        prompt = f'\nNames are {self.identity.game.names}'
        prompt += f'\nRoles are {random.sample(self.identity.game.roles,len(self.identity.game.roles))}, in random order'
        prompt += f'\nYour name is {self.identity.name}'
        prompt += f'\nYour role is {self.identity.role}'
        prompt += f"\nYou can take the following actions: {self.identity.actions}"
        prompt += f"\nYou have the following items: {self.identity.items}"
        prompt += f"\n{self.prompts[identity.role]}"

        self.prompt = prompt
        self.LLM = LLM(prompt)

    def send(self, message):
        """Receives a recap of game history from the game instance.

        Args:
            message (str): The message received.
        """
        self.history = message

    def respond(self):
        """Responds to the game instance with a message.

        Returns:
            str: Response to game
        """
        return self.LLM.call(self.history, action="speak")

    def got_killed(self):
        logging.info('You have been killed.')

    def act(self):
        return self.LLM.call(self.history, action="act")

    def vote(self):
        """Enters a vote.

        Returns:
            str: Name.
        """
        alive = [
            identity.name for identity in self.identity.game.identities if identity.alive]
        return self.LLM.call(f'{self.history}\nEnter your vote. It must be one of the names {alive} or `no one`', action="vote")
