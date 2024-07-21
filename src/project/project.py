import src, src.save_load
import os

class Project(src.JsonSerializable):

    def __init__(
        self,
        name : str = None,
        author : str = "Unknown",
        author_id : int = "0",
        initial_commit_id : int = 0,
        guild_id : int = None,
        cmd_prefix : str = None,
    ):
        super().__init__()
        self.name : str = name
        self.guild_id : int = guild_id
        self.cmd_prefix : str = cmd_prefix
        self.next_commit_id : int = 1

        self.initial_commit = src.Commit(author_id, author, initial_commit_id, f"{self.name} initial commit.")
        self.initial_commit.project_name = self.name
        self.initial_commit.id = 0

        self.project_path: str = ""
        self.json_path: str = ""

        self.checked_out : bool = False
        self.checked_out_by_id : int = 0

    def save(self):
        self.save_to_path(self.json_path)

    def save_to_path(self, json_path : str):
        src.write_json(json_path, self.serialize())

    def add_commit(self, commit : src.Commit) -> int:
        self.checked_out = False
        commit_i : src.Commit = self.initial_commit
        print(self.__dict__)
        while not len(commit_i.next_commits) == 0:
            commit_i = commit_i.next_commits[0]

        print(f"commit : {commit}")
        commit_i.next_commits.append(commit)
        commit.project_name = self.name

        commit.id = self.next_commit_id
        self.next_commit_id += 1
        return commit.id

    def checkout(self, user_id : int) -> src.Commit:
        self.checked_out = True
        self.checked_out_by_id = user_id
        return self.get_latest_commit()

    def cancel_checkout(self):
        self.checked_out = False

    def _get_next_commit(self, commit : src.Commit, branch_path : dict[int, int]=None):
        if not branch_path:
            branch_path = {}
        try:
            next_commit_index = branch_path[commit.id]
        except KeyError:
            next_commit_index = 0
        return commit.next_commits[next_commit_index]

    def get_branch(self, branch_path : dict[int, int]=None) -> list[src.Commit]:
        if not branch_path:
            branch_path = {}
        commit_branch : list[src.Commit] = [self.initial_commit]
        current_commit = commit_branch[-1]
        while len(current_commit.next_commits) != 0:
            current_commit = self._get_next_commit(commit_branch[-1], branch_path)
            commit_branch.append(current_commit)

        return commit_branch

    def get_latest_commit(self, branch_path : dict[int, int]=None):
        if not branch_path:
            branch_path = {}
        return self.get_branch(branch_path)[-1]

    def get_commit(self, id : int) -> src.Commit:
        return self.get_commit_recurse(self.initial_commit, id)

    def get_commit_recurse(self, commit : src.Commit, id : int) -> src.Commit:
        if len(commit.next_commits) == 0:
            return None

        for next_commit in commit.next_commits:
            if next_commit.id == id:
                return next_commit
            else:
                if (self.get_commit_recurse(next_commit, id) == None):
                    continue
                else:
                    return next_commit
        return None