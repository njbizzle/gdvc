import discord

import src

class CommitCommand(src.Command):

    def __init__(self):
        super().__init__("commit")
        pass

    async def run(self, message : discord.Message, project : src.Project, args : dict[str, str]):
        try:
            id = int(args["id"])
            desc = args["desc"]
        except KeyError:
            raise ValueError(
                "Missing correct arguments. Please provide an a level ID (id:999) and a description (desc:\"Here is a short description.\")"
            )
        except ValueError:
            raise ValueError(
                "Please enter the ID as a number."
            )

        project.add_commit(
            src.Commit(
                author_id=message.author.id,
                gd_id=id, description=desc
            )
        )
        project.save()
        await message.channel.send(f"committing yall : {project.name} | {args}")