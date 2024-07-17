import src
from src.save_load import JsonSerializable
from typing import Self, Any


class Commit(JsonSerializable):

    def __init__(
        self,
        author_id : int = 0,
        gd_id : int = 0,
        description : str = "",
        next_commits : list[Self] = None
    ):
        super().__init__()
        self.project_name : str = ""
        self.author_id = author_id
        self.gd_id : int = gd_id
        self.description = description

        if not next_commits:
            next_commits = []

        self.next_commits : list[Self] = next_commits


        self.serializable_commit = True

    def serialize(self) -> dict[str, Any]:
        return super().serialize()