"""
This file shows an example on how to upload local experiment to server.
"""
from pypadre.ds_import import load_sklearn_toys
import pprint
from pypadre.core import Experiment


def create_test_pipeline():
    from sklearn.pipeline import Pipeline
    from sklearn.svm import SVC
    from sklearn.decomposition import PCA
    # estimators = [('reduce_dim', PCA()), ('clf', SVC())]
    estimators = [('SVC', SVC(probability=True))]
    return Pipeline(estimators)


def create_preprocessing_pipeline():
    from sklearn.pipeline import Pipeline
    from sklearn.decomposition import PCA
    # estimators = [('reduce_dim', PCA()), ('clf', SVC())]
    estimators = [('PCA', PCA())]
    return Pipeline(estimators)


def split(idx):
    # Do a 70:30 split
    limit = int(.7 * len(idx))
    return idx[0:limit], idx[limit:], None


if __name__ == '__main__':
    from pypadre.app import p_app
    p_app.set_printer(print)

    # NOTE: Server MUST BE RUNNING!!! See Padre Server!
    # Start PADRE Server and run
    ds = None
    try:
        p_app.datasets.list()
        ds = p_app.datasets.get_dataset("http://localhost:8080/api/datasets/5")
    except:
        ds = [i for i in load_sklearn_toys()][4]

    if ds is None:
        ds = [i for i in load_sklearn_toys()][4]
    print(ds)
    experiment_name = "Test Experiment SVM upload local"
    ex = Experiment(name=experiment_name,
                    description="Testing Support Vector Machines via SKLearn Pipeline",
                    dataset=ds, preprocessing=create_preprocessing_pipeline(),
                    workflow=create_test_pipeline(), keep_splits=True, strategy="random",
                    function=split)
    conf = ex.configuration()  # configuration, which has been automatically extracted from the pipeline
    pprint.pprint(ex.hyperparameters())  # get and print hyperparameters
    ex.execute()  # run the experiment and report

    p_app.authenticate("hmafnan", "test")
    p_app.experiments.upload_local_experiment(experiment_name)