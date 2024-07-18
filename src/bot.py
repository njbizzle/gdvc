import src
import discord

class Bot(discord.Client):

    def __init__(self, intents: discord.Intents) -> None:
        super().__init__(intents=intents)

    async def on_ready(self):
        src.create_project_json(src.Project("name", self.guilds[0].id, "prefix"))

        def is_subclass(cls1, cls2):
            try:
                return issubclass(cls1, cls2)
            except TypeError:
                return False

        self.bot_commands : dict[str, src.commands] = {cmd().name:cmd for name, cmd in src.commands.__dict__.items() if is_subclass(cmd, src.Command)}

        src.clear_loaded_projects()
        for guild in self.guilds:
            src.load_guild_projects(guild.id)

        print(f"Number of Projects Loaded : {len(src.get_loaded_projects())}")

        print(f"Projects Loaded : {", ".join([project.name for project in src.get_loaded_projects()])}")
        print(f"Commands Loaded : {", ".join(self.bot_commands)}")


    async def on_message(self, message : discord.Message):
        if message.content[0] == "/":
            try:
                await self.parse_project_cmd(message)
            except ValueError as e:
                await message.channel.send(content=str(e))


    async def parse_project_cmd(self, message : discord.Message):
        message.content = message.content[1:] # get rid of slash
        print(f" - COMMAND : {message.content}")
        project_prefix_map = src.get_loaded_project_prefix_map()

        try:
            project = project_prefix_map[message.content.split(" ")[0]]
        except KeyError:
            raise ValueError("Bad Input. Project Does not exist. (Never created)")

        if not message.guild.id == project.guild_id:
            raise ValueError("Bad Input. Project Does not exist. (Other guild)")

        command_name, args = self.split_command_args(message.content)
        try:
            command = self.bot_commands[command_name]
        except KeyError:
            raise ValueError("Bad Input. Command Does not exist.")

        await command().run(message, project, args)


    def split_command_args(self, content) -> tuple[str, dict[str, str]]:
        in_quotes : bool = False
        args_raw = []
        split_raw = content.split(" ")
        try:
            project_prefix = split_raw[0]
            cmd_name = split_raw[1]
            args_split_raw = split_raw[2:]
        except IndexError:
            raise ValueError("Bad input. Arguments formatted incorrectly.")

        for chunk in args_split_raw:
            has_quotes = "\"" in chunk
            chunk.replace("\"", "")

            # exit quotes
            if has_quotes and in_quotes:
                args_raw[-1] += " " + chunk
                in_quotes = False
                continue

            # append to quotes
            if in_quotes:
                args_raw[-1] += " " + chunk
            # add normal
            elif not has_quotes:
                args_raw.append(chunk)
            else: # not in quotes and has quotes
                args_raw.append(chunk)
                in_quotes = True
        try:
            args = {arg_split[0] : arg_split[1] for arg_split in [arg_raw.split(":") for arg_raw in args_raw]}
        except IndexError:
            raise ValueError("Bad input. Arguments formatted incorrectly.")

        # print(f"project_prefix {project_prefix}")
        # print(f"cmd_name {cmd_name}")
        # print(f"args {args}")
        return (cmd_name, args)