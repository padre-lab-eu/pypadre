"""
This is a minimal example of a PaDRE experiment.
"""

import numpy as np
from sklearn.datasets import load_iris

# Import the metrics to register them!
# noinspection PyUnresolvedReferences
from pypadre.binding.metrics import sklearn_metrics
from pypadre.examples.base_example import example_app

app = example_app()


@app.dataset(name="iris",
             columns=['sepal length (cm)', 'sepal width (cm)', 'petal length (cm)',
                      'petal width (cm)', 'class'], target_features='class')
def dataset():
    data = load_iris().data
    target = load_iris().target.reshape(-1, 1)
    return np.append(data, target, axis=1)


@app.experiment(dataset=dataset, reference_git=__file__,
                experiment_name="Iris SVC - metric suggestion", seed=1, project_name="Metric Examples")
def experiment():
    from sklearn.pipeline import Pipeline
    from sklearn.svm import SVC
    estimators = [('SVC', SVC(probability=True))]
    return Pipeline(estimators)
