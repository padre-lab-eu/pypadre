from pypadre.core.base import MetadataMixin, ChildMixin
from pypadre.core.model.generic.i_executable_mixin import ValidateableExecutableMixin
from pypadre.core.model.generic.i_model_mixins import StoreableMixin
from pypadre.core.printing.tablefyable import Tablefyable
from pypadre.core.validation.json_validation import make_model

WRITE_RESULTS = "write_results"
WRITE_METRICS = "write_metrics"


run_model = make_model(schema_resource_name='run.json')


class Run(StoreableMixin, ValidateableExecutableMixin, MetadataMixin, ChildMixin, Tablefyable):

    EXECUTION_ID = "experiment_id"


    @classmethod
    def _tablefy_register_columns(cls):
        pass

    def __init__(self, execution,  **kwargs):
        # Add defaults
        defaults = {}

        # Merge defaults
        metadata = {**defaults, **{self.EXECUTION_ID: execution.id}, **kwargs.pop("metadata", {})}
        super().__init__(model_clz=run_model, parent=execution, result=self, metadata=metadata, **kwargs)

    def _execute_helper(self, *args, **kwargs):

        # Send signal
        self.send_put()

        # Start execution of the pipeline
        # pipeline_parameters = kwargs.get('parameters', None)
        pipeline_parameters, write_parameters = \
            self.separate_hyperparameters_and_component_parameters(kwargs.pop('parameters', None))
        return self.pipeline.execute(dataset=self.dataset, run=self, pipeline_parameters=pipeline_parameters,
                                     write_parameters=write_parameters,
                                     *args, **kwargs)

    @property
    def execution(self):
        return self.parent

    @property
    def dataset(self):
        return self.execution.dataset

    @property
    def experiment(self):
        return self.execution.experiment

    @property
    def pipeline(self):
        return self.execution.pipeline

    def separate_hyperparameters_and_component_parameters(self, parameters:dict):

        parameter_dict = dict()
        write_result_metric_dict = dict()

        # Iterate through every parameter
        if parameters is not None:
            for component_name in parameters:
                params = parameters.get(component_name)
                # Save the hyperparamters in a separate dictionary
                if params.get('parameters', None) is not None:
                    parameter_dict[component_name] = params.get('parameters')

                # If the user wants to dump the results of the component, set the Flag
                write_results = params.get(WRITE_RESULTS, False)

                # The user can specify multiple metrics if needed, so it is a list
                write_metrics = params.get(WRITE_METRICS, None)

                write_result_metric_dict[component_name] = {WRITE_RESULTS: write_results,
                                                            WRITE_METRICS: write_metrics}
            if not parameter_dict:
                parameter_dict = None

            return parameter_dict, write_result_metric_dict
        else:
            return {}, {}
