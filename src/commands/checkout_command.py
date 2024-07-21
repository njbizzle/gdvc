import discord

import src
from src import command_tools


class CheckoutCommand(command_tools.Command):

    def __init__(self):
        super().__init__("checkout",
            command_args=[

            ]
        )

    async def run_abs(self, message : discord.Message, project : src.Project, args : dict[str, str]):
        if project.checked_out:
            checked_out_user_ping = f"<@{project.checked_out_by_id}>"
            raise ValueError(f"Project is already checked out by {checked_out_user_ping}.")

        checked_out_commit = project.checkout(message.author.id)
        await message.channel.send(content=f"Checked out commit: {checked_out_commit.display()}")
