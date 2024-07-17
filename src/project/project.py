import src, src.save_load
import os

class Project(src.JsonSerializable):

    def __init__(
        self,
        name : str = None,
        guild_id : int = None,
        cmd_prefix : str = None,
    ):
        super().__init__()
        self.name : str = name
        self.guild_id : int = guild_id
        self.cmd_prefix : str = cmd_prefix

        self.initial_commit = src.Commit(0, 0, "Initial Commit")

        self.project_path: str = ""
        self.json_path: str = ""

    def save(self):
        self.save_to_path(self.json_path)

    def save_to_path(self, json_path : str):
        src.write_json(self.json_path, self.serialize())

    def add_commit(self, commit : src.Commit) -> int:
        commit_i : src.Commit = self.initial_commit
        print(self.__dict__)
        while not len(commit_i.next_commits) == 0:
            commit_i = commit_i.next_commits[0]

        commit_i.next_commits.append(commit)
        commit.project_name = self.name

