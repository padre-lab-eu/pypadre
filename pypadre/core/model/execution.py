from pypadre.core.base import MetadataEntity, ChildEntity
from pypadre.core.model.generic.i_executable_mixin import IExecuteable
from pypadre.core.model.generic.i_model_mixins import IStoreable, IProgressable
from pypadre.core.printing.tablefyable import Tablefyable
from pypadre.core.model.computation.run import Run


class Execution(IStoreable, IProgressable, IExecuteable, MetadataEntity, ChildEntity, Tablefyable):
    """
    A execution should save data about the running env and the version of the code on which it was run .
    An execution is linked to the version of the code being executed. The execution directory is the hash of the commit
    of the source code file.
    """

    EXPERIMENT_ID = "experiment_id"

    _runs = []
    @classmethod
    def _tablefy_register_columns(cls):
        # Add entries for tablefyable
        cls.tablefy_register_columns({'hash': 'hash', 'cmd': 'cmd'})

    def __init__(self, experiment, codehash=None, command=None, **kwargs):
        # Add defaults
        defaults = {}

        # Merge defaults
        metadata = {**defaults, **kwargs.pop("metadata", {}), **{self.EXPERIMENT_ID: experiment.id}}

        if codehash is not None:
            metadata['hash'] = codehash

        super().__init__(parent=experiment, schema_resource_name="execution.json", metadata=metadata, **kwargs)

        self._command = command

    def _execute_helper(self, *args, **kwargs):
        self.send_put()
        run = Run(execution=self)
        self._runs.append(run)
        return run.execute(data=self.dataset, execution=self, **kwargs)

    @property
    def hash(self):
        return self.metadata.get('hash', None)

    @property
    def command(self):
        return self._command

    @property
    def experiment(self):
        return self.parent

    @property
    def dataset(self):
        return self.experiment.dataset

    @property
    def pipeline(self):
        return self.experiment.pipeline

    @property
    def run(self):
        return self._runs
