import discord

import src

class TestCommand(src.Command):

    def __init__(self):
        super().__init__("testcmd")
        pass

    async def run(self, message : discord.Message, project : src.Project, args : dict[str, str]):
        await message.channel.send(f"this was test command, project name : {project.name} | {args}")