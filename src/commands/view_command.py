import discord
from typing import Union
from src import command_tools

import src


class ViewCommand(command_tools.Command):

    def __init__(self):
        super().__init__("view",
            command_args=[
                command_tools.CommandArgument("count", Union[int, str]),
                command_tools.IntIndexedCommandArgument(int)
            ],
            missing_error="Please specify at an ID (id:999), and a short description (desc:\"This is a short description.\")"
        )

    async def run_abs(self, message : discord.Message, project : src.Project, args : dict[str, str]):
        count = 3

        try:
            count = int(args["count"])
            del args["count"]
        except KeyError:
            pass
        except ValueError:
            if args["count"] == "all":
                count = 0
            del args["count"]

        try:
            args_int = {int(key):int(value) for key, value in args.items()}
        except ValueError:
            raise ValueError("Arguments are not formatted correctly.")

        branch = project.get_branch(args_int)

        branch_displays = [commit.display() for commit in branch]
        branch_displays_truncated = branch_displays[-count:]

        hidden_count = len(branch) - len(branch_displays_truncated)
        content = f"```{hidden_count} previous commits hidden, use argument 'count:all' to view all.```\n"
        content += "\n".join(branch_displays_truncated)

        await message.channel.send(content=content)