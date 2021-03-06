from pypadre import _version, _name
from pypadre.core.model.code.code_mixin import PythonPackage, PipIdentifier, Function
from pypadre.core.model.pipeline.parameter_providers.parameters import ParameterProvider


def _create_combinations(ctx, **parameters: dict):
    import itertools

    # Generate every possible combination of the provided hyper parameters.
    master_list = []
    params_list = []
    for estimator in parameters:
        param_dict = parameters.get(estimator)
        # assert_condition(condition=isinstance(param_dict, dict),
        #                  source=self,
        #                  source=self,
        #                  message='Parameter dictionary is not of type dictionary for estimator:' + estimator)
        for params in param_dict:
            param = param_dict.get(params)
            if not isinstance(param, list):
                param = [param]
            # Append only the parameters to create a master list
            master_list.append(param)

            # Append the estimator name followed by the parameter to create a ordered list.
            # Ordering of estimator.parameter corresponds to the value in the resultant grid tuple
            params_list.append(''.join([estimator, '.', params]))

    grid = itertools.product(*master_list)
    return grid, params_list


# noinspection PyTypeChecker
# Create a default pip identifier
sklearn_grid_search = ParameterProvider(name="default_sklearn_provider",
                                        reference=PythonPackage(package=__name__, variable="sklearn_grid_search",
                                                                repository_identifier=PipIdentifier(
                                                                    pip_package=_name.__name__,
                                                                    version=_version.__version__)),
                                        code=Function(fn=_create_combinations, transient=True,
                                                      repository_identifier=PipIdentifier(pip_package=_name.__name__,
                                                                                          version=_version.__version__)))
