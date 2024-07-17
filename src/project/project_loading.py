import os
import src
from src.project import Project

loaded_projects: set[Project] = set()

def new_project(name: str, guild_id: int, prefix : str) -> Project:
    project = Project(name, guild_id, prefix)
    src.create_project_json(project)

    loaded_projects.add(project)

    return project

def get_loaded_projects() -> set[Project]:
    return loaded_projects

def get_loaded_project_prefix_map() -> dict[str, Project]:
    return {project.cmd_prefix : project for project in loaded_projects}

def load_guild_projects(guild_id : int):
    guild_data = os.path.join(src.gdvc_root, f"data/{guild_id}")

    for project_name in os.listdir(guild_data):
        load_project_from_path(os.path.join(guild_data, project_name, f"{project_name}_data.json"))


def get_project(name : str) -> Project:
    data = os.path.join(src.gdvc_root, "data")

    for project_dir in os.listdir(data):
        if name == project_dir:
            return load_project_from_path(os.path.join(data, name, f"{name}_data.json"))

def load_project_from_path(path) -> Project:
    project = Project()
    project.deserialize(src.read_json(path))
    loaded_projects.add(project)
    return project

def clear_loaded_projects():
    global loaded_projects
    loaded_projects = set()

def create_project_json(project : Project) -> None:
    os.makedirs(f"data/{project.guild_id}/{project.name}", exist_ok=True)

    project_root : str = os.path.join(
        src.save_load.gdvc_root,
        "data",
        str(project.guild_id),
        project.name
    )

    project_json : str = os.path.join(
        project_root,
        f"{project.name}_data.json"
    )

    project.root_path = project_root
    project.json_path = project_json

    project.save()
