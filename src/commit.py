import src
from src.save_load import JsonSerializable
from typing import Self, Any


class Commit(JsonSerializable):

    def __init__(
        self,
        author_id : int = 0,
        author_name : str = "",
        gd_id : int = 0,
        description : str = "",
        next_commits : list[Self] = None
    ):
        super().__init__()
        self.project_name : str = ""
        self.id : int = -1
        self.author_name : str = author_name
        self.author_id = author_id
        self.gd_id : int = gd_id
        self.description = description

        if not next_commits:
            next_commits = []

        self.next_commits : list[Self] = next_commits

        self.serializable_commit = True

    def serialize(self) -> dict[str, Any]:
        return super().serialize()

    def display(self) -> str:
        display_text = "```"

        next_commit_ids_display = ", ".join(
            [str(commit.id) for commit in self.next_commits]
        ) if not len(self.next_commits) == 0 else "None (Branch End)"

        display_text += f"""
Commit ID: {self.id}, Authored By: {self.author_name}, GD ID: {self.gd_id}
Description: {self.description}
Next Commits IDs: {next_commit_ids_display}"""

        display_text += "```"
        return display_text

