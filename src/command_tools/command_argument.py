class CommandArgument:

    default_missing_error = "Missing required arguments."
    default_type_error = "Arguments formatted incorrectly."
    default_int_parse_error = "Numbers formatted incorrectly."

    def __init__(
        self,
        arg_name : str,
        arg_type : type,
        required : bool = False,
        missing_error : str = default_missing_error,
        type_error : str = default_type_error,
        int_parse_error : str = default_int_parse_error
    ):
        self.arg_name = arg_name
        self.arg_type = arg_type
        self.required = required

        self.missing_error = missing_error
        self.type_error = type_error
        self.int_parse_error = int_parse_error

    def check(self, args : dict):
        try:
            args[self.arg_name]
        except KeyError:
            if self.required:
                raise ValueError(self.missing_error)
            else:
                return

        if self.arg_type == int:
            try:
                args[self.arg_name] = int(args[self.arg_name])
            except ValueError:
                raise ValueError(self.int_parse_error)

        if not isinstance(args[self.arg_name], self.arg_type):
            raise ValueError(self.type_error)

