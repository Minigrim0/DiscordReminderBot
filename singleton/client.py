import discord

from discord_slash import SlashCommand
from singleton.command_manager import CommandManager


class Bert(discord.Client):
    instance = None

    @staticmethod
    def getInstance():
        """Returns the instance of the singleton

        Returns:
            Bert: The instance
        """
        if Bert.instance is None:
            Bert()
        return Bert.instance

    def __init__(self):
        if Bert.instance is not None:
            raise Exception("This class is a singleton")

        Bert.instance = self
        super().__init__()

        self.slash = SlashCommand(self, sync_commands=True)
        self.commandManager = CommandManager(self)

    async def on_ready(self) -> None:
        """Function called when the bot is connected to the API"""
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message: discord.Message) -> None:
        """Called when a message is sent womewhere the bot can access

        Args:
            message (discord.Message): The message with its metadata
        """
        if message.content and message.content[0] == "/":
            await self.commandManager.execCommand(message.content[1:], message.channel)

    def run(self, token: str) -> None:
        """Sets the bot as only and ready to receive messages

        Args:
            token (str): The secret token used to interact with discord API
        """
        super().run(token)
