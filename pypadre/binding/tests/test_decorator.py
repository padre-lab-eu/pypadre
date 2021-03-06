import unittest

import numpy as np
from sklearn.datasets import load_iris

from pypadre.binding.model.sklearn_binding import SKLearnPipeline
from pypadre.pod.tests.base_test import PadreAppTest


class AppLocalBackends(PadreAppTest):

    def setUp(self):
        self.setup_reference(__file__)

    def test_workflow(self):
        self.app.datasets.load_defaults()
        id = '_iris_dataset'
        dataset = self.app.datasets.list({'name': id})

        @self.app.experiment(dataset=dataset.pop(), project_name="test_workflow",ptype=SKLearnPipeline, reference=self.test_reference)
        def create_test_pipeline():
            from sklearn.pipeline import Pipeline
            from sklearn.svm import SVC
            estimators = [('SVC', SVC(probability=True))]
            return Pipeline(estimators)

    def test_workflow_dataset(self):
        @self.app.dataset(name="iris", columns=['sepal length (cm)', 'sepal width (cm)', 'petal length (cm)',
                                                'petal width (cm)', 'class'], target_features='class')
        def get_dataset():
            data = load_iris().data
            target = load_iris().target.reshape(-1, 1)
            return np.append(data, target, axis=1)

        @self.app.experiment(dataset=get_dataset, project_name="test_workflow_dataset",ptype=SKLearnPipeline, reference=self.test_reference)
        def create_test_pipeline():
            from sklearn.pipeline import Pipeline
            from sklearn.svm import SVC
            estimators = [('SVC', SVC(probability=True))]
            return Pipeline(estimators)

    def test_no_auto_execute(self):
        @self.app.dataset(name="iris",
                          columns=['sepal length (cm)', 'sepal width (cm)', 'petal length (cm)', 'petal width (cm)',
                                   'class'], target_features='class')
        def get_dataset():
            data = load_iris().data
            target = load_iris().target.reshape(-1, 1)
            return np.append(data, target, axis=1)

        @self.app.experiment(dataset="iris", ptype=SKLearnPipeline, project_name="My Fun Project", auto_main=False,
                             reference=self.test_reference)
        def experiment():
            from sklearn.pipeline import Pipeline
            from sklearn.svm import SVC
            estimators = [('SVC', SVC(probability=True))]
            return Pipeline(estimators)

        experiment.execute()


if __name__ == '__main__':
    unittest.main()
