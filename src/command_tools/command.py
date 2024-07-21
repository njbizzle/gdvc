import discord
import src
from src import command_tools
from abc import ABC, abstractmethod
from typing import Union


class Command(ABC):

    def __init__(
        self,
        name : str,
        command_args : list[command_tools.CommandArgument],
        missing_error : str = None,
        type_error : str = None,
        int_parse_error : str = None
    ):
        self.name : str = name
        self.command_args : list[command_tools.CommandArgument] = command_args

        self.missing_error = missing_error
        self.type_error = type_error
        self.int_parse_error = int_parse_error

    async def run(self, message : discord.Message, project : src.Project, args : dict[str, Union[str,int]]):
        for command_arg in self.command_args:
            try:
                command_arg.check(args)
            except ValueError as e:
                if str(e) == command_tools.CommandArgument.default_missing_error and self.missing_error:
                    raise ValueError(self.missing_error)
                elif str(e) == command_tools.CommandArgument.default_type_error and self.type_error:
                    raise ValueError(self.type_error)
                elif str(e) == command_tools.CommandArgument.default_int_parse_error and self.int_parse_error:
                    raise ValueError(self.int_parse_error)
                else:
                    raise e

        await self.run_abs(message, project, args)

    @abstractmethod
    async def run_abs(self, message : discord.Message, project : src.Project, args : dict[str, str]):
        pass