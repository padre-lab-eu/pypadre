import os
import platform
from abc import abstractmethod, ABCMeta

from git import Repo

from pypadre.pod.repository.local.file.generic.i_file_repository import IFileRepository
from pypadre.pod.util.git_util import repo_exists, commit, create_repo

"""
For datasets, experiments and projects there would be separate repositories.
The Dataset, experiment and project classes implement the IBaseGitRepository
So, the only functionalities required by git are add_file, list_file, delete_file, get_file
"""

GIT_ATTRIBUTES = '.gitattributes.'


class IGitRepository(IFileRepository):
    """ This is the abstract class implementation of a class extending the basic file backend with git functionality """
    __metaclass__ = ABCMeta
    # Variable holding the repository
    _DEFAULT_GIT_MSG = 'Added file to git'

    @abstractmethod
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def _clone(self, repo, url, path, branch='master'):
        """
        Clone a remote repo
        :param repo: Repo object of the repository
        :param url: URL of the remote remo
        :param path: Path to clone the remote repo
        :param branch: Branch to pull from the remote repo
        :return: None
        """
        if self.repo is not None:
            repo.clone_from(url, path, branch)

    def _add_files(self, repo, file_path):
        """
        Adds the untracked files to the git
        :param file_path: An array containing the file paths to be added to git
        :return:
        """
        if self.is_backend_valid():
            if isinstance(file_path, str):
                repo.index.add([file_path])
            else:
                repo.index.add(file_path)

    def _get_untracked_files(self, repo):
        return repo.untracked_files if self.is_backend_valid() else None

    def _get_tags(self, repo):
        return repo.tags if self.is_backend_valid() else None

    def _get_working_tree_directory(self, repo):
        return repo.working_tree_dir if self.is_backend_valid() else None

    def _get_working_directory(self, repo):
        return repo.working_dir if self.is_backend_valid() else None

    def _get_git_path(self, repo):
        return repo.git_dir if self.is_backend_valid() else None

    def _is_head_remote(self, repo):
        return repo.head.is_remote() if self.is_backend_valid() else None

    def _is_head_valid(self, repo):
        return repo.head.is_valid() if self.is_backend_valid() else None

    def _get_heads(self, repo):
        return repo.heads if self.is_backend_valid() else None

    def _check_git_directory(self, repo, path):
        return repo.git_dir.startswith(path) if self.is_backend_valid() else None

    def _get_head(self, repo):
        return repo.head if self.is_backend_valid() else None

    def _has_untracked_files(self, repo):
        return True if self._get_untracked_files(repo=repo) is not None else False

    def _add_untracked_files(self, repo):
        if self._has_untracked_files(repo=repo):
            untracked_files = self._get_untracked_files(repo=repo)
            self._add_files(repo=repo, file_path=untracked_files)

    def _delete_tags(self, repo, tag_name):
        if not self.is_backend_valid():
            return

        tags = repo.tags
        if tag_name in tags:
            repo.delete_tag(tag_name)

        else:
            # Raise warning/error that tag is not present
            pass

    def _archive_repo(self, repo, path):
        if not self.is_backend_valid():
            return

        with open(path, 'wb') as fp:
            repo.archive(fp)

    def _push(self, repo):
        if self._remote is None:
            self._remote = repo.create_remote(self._remote_name, self._remote_url)

        # Push to the master branch from current master branch
        # https://gitpython.readthedocs.io/en/stable/reference.html#git.remote.Remote.push
        self._remote.push(refspec='{}:{}'.format('master', 'master'))

    # database backend functions
    def list(self, search, offset=0, size=100):
        """
        Function to list repos. Cannot be implemented in GitPython.
        :param search_id: Id to be searched for
        :param offset:
        :param size:
        :return:
        """
        # TODO: Possibly, look for in the remote repositories if possible
        return super().list(search)

    # Abstract method which would create a repo based on the requirements
    def put(self, obj, *args, merge=False, allow_overwrite=False, **kwargs):
        super().put(obj, *args, merge=merge, allow_overwrite=allow_overwrite, **kwargs)

        # Init repo if not already existing
        directory = self.to_directory(obj)
        if not repo_exists(directory):
            repo = Repo.init(path=directory, **kwargs.pop("repo_kwargs", {}))
        else:
            repo = self.get_repo(path=directory, **kwargs.pop("repo_kwargs", {}))
        # TODO add_and_commit if we have changes and put some commit message. Where can I define the message??? Is there a possibility to git status?
        return repo

    def get(self, uid):
        # Call the File backend get function
        return super().get(uid=uid)

    def get_repo(self, path=None, url=None, **kwargs):
        """
        Pull a repository from remote
        :param repo_name: Name of the repo to be cloned
        :param path: Path to be cloned
        :return:
        """
        if path is not None and url is not None:
            return Repo.clone_from(url=url, to_path=path)

        elif url is None and path is not None:
            # Open the local repository
            return Repo(path)

        super().get(**kwargs)

    def delete(self, id):
        """
        Deletes a repo from the Git backend
        :param id: id of the repo to be deleted
        :return:
        """
        # TODO: Remove the local directory
        # TODO: User will have to remove the remote repository by themselves
        super().delete(id)

    @staticmethod
    def is_backend_valid():
        """
        Check if repo is instantiated
        :return: True if valid, False otherwise
        """
        # TODO Implement validity checks for repo
        return True

    def has_remote_backend(self):
        # TODO Validate the remote_url
        return True if self.remote_url is not None else False

    def add_git_lfs_attribute_file(self, directory, file_extension):
        # Get os version and write content to file
        path = None
        # TODO: Verify path in Windows
        if platform.system() == 'Windows':
            path = os.path.join(directory, GIT_ATTRIBUTES)
        else:
            path = os.path.join(directory, GIT_ATTRIBUTES)

        with open(path, "w") as f:
            f.write(" ".join([file_extension, 'filter=lfs diff=lfs merge=lfs -text']))
        repo = create_repo(path=directory, bare=False)
        self._add_files(repo, file_path=path)
        commit(repo=repo, message='Added .gitattributes file for Git LFS')

        # Add all untracked files
        self._add_untracked_files(repo=repo)
        commit(repo, message=self._DEFAULT_GIT_MSG)

    def add_and_commit(self, obj):
        directory = self.to_directory(obj)
        repo = self.get_repo(path=directory)
        self._add_untracked_files(repo=repo)
        commit(repo, message=self._DEFAULT_GIT_MSG)


def _has_uncommitted_files(repo):
    # True if there are files with differences
    return True if len([item.a_path for item in repo.index.diff(None)]) > 0 else False
