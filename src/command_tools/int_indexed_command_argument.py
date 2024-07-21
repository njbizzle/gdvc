from src import command_tools


class IntIndexedCommandArgument(command_tools.CommandArgument):
    def __init__(
        self,
        arg_type : type,
        missing_error : str = "Missing required arguments.",
        type_error : str = "Arguments formatted incorrectly.",
        int_parse_error : str = "Numbers formatted incorrectly."
    ):
        super().__init__("", arg_type, False, missing_error, type_error, int_parse_error)

    def check(self, args : dict):
        for key, value in args.items():
            try:
                args[int(key)] = value
            except ValueError:
                continue

            self.arg_name = int(key)
            super().check(args)