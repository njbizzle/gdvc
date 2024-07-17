import discord
import src
from abc import ABC, abstractmethod


class Command(ABC):

    def __init__(self, name):
        self.name = name

    @abstractmethod
    def run(self, message : discord.Message, project : src.Project, args : dict[str, str]):
        pass