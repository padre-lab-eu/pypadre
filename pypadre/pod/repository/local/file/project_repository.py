import os
import re

from pypadre.core.model.project import Project
from pypadre.pod.backend.i_padre_backend import IPadreBackend
from pypadre.pod.repository.i_repository import IProjectRepository
from pypadre.pod.repository.local.file.generic.i_file_repository import File
from pypadre.pod.repository.local.file.generic.i_git_repository import IGitRepository
from pypadre.pod.repository.local.file.generic.i_log_file_repository import ILogFileRepository
from pypadre.pod.repository.serializer.serialiser import JSonSerializer

NAME = 'projects'
META_FILE = File("metadata.json", JSonSerializer)


class ProjectFileRepository(IGitRepository, IProjectRepository, ILogFileRepository):

    @staticmethod
    def placeholder():
        return '{PROJECT_ID}'

    def __init__(self, backend: IPadreBackend):
        super().__init__(root_dir=os.path.join(backend.root_dir, NAME), backend=backend)

    def _get_by_dir(self, directory):
        metadata = self.get_file(directory, META_FILE)
        return Project(name=metadata.pop("name"), description=metadata.pop("description"), metadata=metadata)

    def to_folder_name(self, project):
        # TODO only name for folder okay? (maybe a uuid, a digest of a config or similar?)
        return project.name

    def list(self, search, offset=0, size=100):
        if search is not None and "name" in search:
            # Shortcut because we know name is the folder name. We don't have to search in metadata.json
            name = search.pop("name")
            search[self.FOLDER_SEARCH] = name
        return super().list(search, offset, size)

    def _put(self, obj, *args, directory: str, merge=False, **kwargs):
        project = obj
        self.write_file(directory, META_FILE, project.metadata)
