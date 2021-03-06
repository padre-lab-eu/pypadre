from pypadre.core.model.computation.run import Run
from pypadre.pod.backend.i_padre_backend import IPadreBackend
from pypadre.pod.repository.i_repository import IRunRepository
from pypadre.pod.repository.local.file.generic.i_file_repository import File, IChildFileRepository
from pypadre.pod.repository.local.file.generic.i_log_file_repository import ILogFileRepository
from pypadre.pod.repository.serializer.serialiser import JSonSerializer

NAME = "runs"

META_FILE = File("metadata.json", JSonSerializer)
RESULT_FILE = File("result.json", JSonSerializer)


class RunFileRepository(IChildFileRepository, ILogFileRepository, IRunRepository):

    @staticmethod
    def placeholder():
        return '{RUN_ID}'

    def __init__(self, backend: IPadreBackend):
        super().__init__(parent=backend.execution, name=NAME, backend=backend)

    def _get_by_dir(self, directory):
        metadata = self.get_file(directory, META_FILE)
        #hyperparameter = self.get_file(directory, HYPERPARAMETER_FILE)
        #workflow = self.get_file(directory, WORKFLOW_FILE)

        # TODO what to do with hyperparameters?
        execution = self.parent.get_by_dir(self.get_parent_dir(directory))
        run = Run(execution=execution, metadata=metadata)
        return run

    def put_progress(self, run, **kwargs):
        self.log(
            "RUN PROGRESS: {curr_value}/{limit}. phase={phase} \n".format(**kwargs))

    def get(self, uid):
        return super().get(uid)

    def _put(self, obj, *args, directory: str, merge=False, **kwargs):
        run = obj
        self.write_file(directory, META_FILE, run.metadata)
