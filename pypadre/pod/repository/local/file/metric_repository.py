import os
from types import GeneratorType

from pypadre.core.metrics.metrics import Metric
from pypadre.pod.backend.i_padre_backend import IPadreBackend
from pypadre.pod.repository.i_repository import IMetricRepository
from pypadre.pod.repository.local.file.generic.i_file_repository import File, IChildFileRepository
from pypadre.pod.repository.local.file.generic.i_log_file_repository import ILogFileRepository
from pypadre.pod.repository.serializer.serialiser import JSonSerializer

NAME = "metrics"

META_FILE = File("metadata.json", JSonSerializer)
RESULT_FILE = File("results.json", JSonSerializer)


class MetricFileRepository(IChildFileRepository, ILogFileRepository, IMetricRepository):

    @staticmethod
    def placeholder():
        return '{METRIC_ID}'

    def __init__(self, backend: IPadreBackend):
        super().__init__(parent=backend.run, name=NAME, backend=backend)

    def _get_by_dir(self, directory):
        if not os.path.isdir(directory):
            return None

        metadata = self.get_file(directory, META_FILE)
        result = self.get_file(directory, RESULT_FILE)
        computation = self.backend.computation.get(metadata.get(Metric.COMPUTATION_ID))

        # TODO Computation
        metric = Metric(name=metadata.get(Metric.NAME), computation=computation, metadata=metadata, result=result)
        return metric

    def _put(self, obj, *args, directory: str, merge=False, **kwargs):
        metric = obj
        self.write_file(directory, META_FILE, metric.metadata)
        if not isinstance(metric.result, GeneratorType):
            self.write_file(directory, RESULT_FILE, metric.result)
