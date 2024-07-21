import discord

import src
from src import command_tools
from typing import Union


class CommitCommand(command_tools.Command):

    def __init__(self):
        super().__init__("commit",
            command_args=[
                command_tools.CommandArgument("id", int, True),
                command_tools.CommandArgument("desc", str, True)
            ]
        )

    async def run_abs(self, message : discord.Message, project : src.Project, args : dict[Union[str, int], Union[str, int]]):

        if not project.checked_out_by_id == message.author.id and project.checked_out:
            checked_out_user_ping = f"<@{project.checked_out_by_id}>"
            raise ValueError(f"Project is already checked out by {checked_out_user_ping}.")

        elif not project.checked_out:
            raise ValueError(f"Project is not checked out. Please checkout before adding a commit.")


        project.add_commit(
            src.Commit(
                author_id=message.author.id,
                author_name=message.author.name,
                gd_id=args["id"], description=args["desc"]
            )
        )
        project.save()
        await message.channel.send(f"committing yall : {project.name} | {args}")
