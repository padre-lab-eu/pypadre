from typing import List

from pypadre.core.events.events import connect
from pypadre.core.model.project import Project
from pypadre.pod.repository.i_repository import IProjectRepository
from pypadre.pod.service.base_service import ModelServiceMixin
from pypadre.pod.service.logging_service import LoggingService


class ProjectService(ModelServiceMixin, LoggingService):
    """
    Class providing commands for managing datasets.
    """

    def __init__(self, backends: List[IProjectRepository], **kwargs):
        super().__init__(model_clz=Project, backends=backends, **kwargs)

        @connect(Project)
        def put(obj, **kwargs):
            self.put(obj)
        self.save_signal_fn(put)

        @connect(Project)
        def delete(obj, **kwargs):
            self.delete(obj)
        self.save_signal_fn(delete)

    def execute(self, id):
        project = self.get(id)
        return project.execute()
