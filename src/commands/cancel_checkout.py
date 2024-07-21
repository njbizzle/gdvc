import discord

import src
from src import command_tools

class CancelCheckout(command_tools.Command):

    def __init__(self):
        super().__init__("cancel_checkout",
            command_args=[

            ]
        )

    async def run_abs(self, message : discord.Message, project : src.Project, args : dict[str, str]):
        if not project.checked_out:
            raise ValueError("The project has no ongoing checkout.")
        project.cancel_checkout()

        await message.channel.send(f"<@{project.checked_out_by_id}>'s checkout was canceled.")