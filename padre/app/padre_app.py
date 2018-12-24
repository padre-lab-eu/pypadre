"""
Padre app as single point of interaction.

Defaults:

- The default configuration is provided under `.padre.cfg` in the user home directory


Architecture of the module
++++++++++++++++++++++++++

- `PadreConfig` wraps the configuration for the app. It can read/write the config from a file (if provided)

"""

# todo merge with cli. cli should use app and app should be configurable via builder pattern and configuration files

import os
import configparser

import copy
from beautifultable import BeautifulTable
from beautifultable.enums import Alignment
from scipy.stats.stats import DescribeResult

from padre.datasets import formats

from padre.backend.file import DatasetFileRepository, PadreFileBackend
from padre.backend.http import PadreHTTPClient
from padre.backend.dual_backend import DualBackend
import padre.ds_import
from padre.experimentcreator import ExperimentCreator
from padre.experiment import Experiment
from padre.metrics import ReevaluationMetrics
from padre.metrics import CompareMetrics
from padre.base import default_logger

if "PADRE_BASE_URL" in os.environ:
    _BASE_URL = os.environ["PADRE_BASE_URL"]
else:
    _BASE_URL = "http://localhost:8080/api"

if "PADRE_CFG_FILE" in os.environ:
    _PADRE_CFG_FILE = os.environ["PADRE_CFG_FILE"]
else:
    _PADRE_CFG_FILE = os.path.expanduser('~/.padre.cfg')


def _sub_list(l, start=-1, count=9999999999999):
    start = max(start, 0)
    stop = min(start + count, len(l))
    if start >= len(l):
        return []
    else:
        return l[start:stop]


def _wheel_char(n_max):
    chars = ["/", "-", "\\", "|", "/", "-", "\\", "|"]
    for i in range(n_max):
        yield "\r" + chars[i % len(chars)]

def dict_merge(dct, merge_dct):
    """ Recursive dict merge. Inspired by :meth:``dict.update()``, instead of
    updating only top-level keys, dict_merge recurses down into dicts nested
    to an arbitrary depth, updating keys. The ``merge_dct`` is merged into
    ``dct``.
    :param dct: dict onto which the merge is executed
    :param merge_dct: dct merged into dct
    :return: None
    """
    import collections
    for k, v in merge_dct.items():
        if (k in dct and isinstance(dct[k], dict)
                and isinstance(merge_dct[k], collections.Mapping)):
            dict_merge(dct[k], merge_dct[k])
        else:
            dct[k] = merge_dct[k]

def get_default_table():
    table = BeautifulTable(max_width=150, default_alignment=Alignment.ALIGN_LEFT)
    table.row_seperator_char = ""
    return table


class PadreConfig:
    """
    PadreConfig class covering functionality for viewing or updating default
    configurations for PadreApp.
    Configuration file is placed at ~/.padre.cfg

    Expected values in config are following
    ---------------------------------------
    [HTTP BACKEND]
    user = username
    passwd = user_password
    base_url = http://localhost:8080/api
    token = oauth_token

    [LOCAL BACKEND]
    root_dir = ~/.pypadre/

    [GENERAL]
    offline = True
    ---------------------------------------

    Implemented functionality.

    1- Get list of dicts containing key, value pairs for all sections in config
    2- Get value for given key.
    3- Set value for given key in config
    4- Authenticate given user and update new token in the config
    """
    def __init__(self, config_file: str=_PADRE_CFG_FILE, create: bool=True, config:dict=None):
        """
        PRecedence of Configurations: default gets overwritten by file which gets overwritten by config parameter
        :param config: str pointing to the config file or None if no config file should be used
        :param create: true if the config file should be created
        :param config: Additional configuration
        """
        self._config = self.default()
        # handle file here
        self._config_file = config_file
        if self._config_file is not None:
            self.__load_config()
            if not os.path.exists(self._config_file) and create:
                self.save()
        # now merge
        self.__merge_config(config)


    def __merge_config(self, to_merge):
        # merges the provided dictionary into the config.
        if to_merge is not None:
            dict_merge(self._config, to_merge)

    def __load_config (self):
        """
        loads a padre configuration from the given file or from the standard file ~/.padre.cfg if no file is provided
        :param config_file: filename of config file
        :return: config accessable as dictionary
        """
        config = configparser.ConfigParser()
        if os.path.exists(self._config_file):
            config.read(self._config_file)
            self.__merge_config(dict(config._sections))

    def default(self):
        """
        :return: default values for
        """
        return {
            "HTTP BACKEND": {
                    "base_url": _BASE_URL,
                     "user": "mgrani",
            },
            "LOCAL BACKEND": {
                "root_dir": os.path.expanduser("~/.pypadre/")
            },
            "GENERAL": {
                "offline": True
            }
        }

    @property
    def config_file(self):
        return self._config_file

    @property
    def config(self):
        return self._config

    @config.setter
    def config(self, config):
        self._config = config

    @property
    def http_backend_config(self):
        return self._config["HTTP BACKEND"]

    @property
    def general(self):
        return self._config["GENERAL"]

    @property
    def local_backend_config(self):
        return self._config["LOCAL BACKEND"]

    def load(self) -> None:
        """
        reloads the configuration specified under the current config path
        """
        self.__load_config()
    def save(self) -> None:
        """
        saves the current configuration to the configured file
        """
        pconfig = configparser.ConfigParser()
        for k, v in self._config.items():
            pconfig[k] = v
        with open(self._config_file, "w") as cfile:
            pconfig.write(cfile)

    def sections(self) -> list:
        """
        :return: returns all sections of the config file
        """
        return self._config.keys()

    def set(self, key, value, section='HTTP BACKEND'):
        """
        Set value for given key in config

        :param key: Any key in config
        :type key: str
        :param value: Value to be set for given key
        :type value: str
        :param section: Section to be changed in config, default HTTP
        :type section: str
        """
        if not self.config[section]:
            self.config[section] = dict()
        self.config[section][key]=value

    def get(self, key, section='HTTP BACKEND'):
        """
        Get value for given key.
        :param key: Any key in config for any section
        :type key: str
        :return: Found value or False
        """
        return self._config[section][key]

    def authenticate(self, user=None, passwd=None, url=None):
        """
        Authenticate given user and update new token in the config.

        :param url: url of the server
        :type url: str
        :param user: Given user
        :type user: str
        :param passwd: Given password
        :type passwd: str
        """
        self.http_backend_config["user"]=user
        http = PadreHTTPClient(**self.http_backend_config)
        token = http.get_access_token(url, user, passwd)
        self.set('token', token)


class DatasetApp:
    """
    Class providing commands for managing datasets.
    """
    def __init__(self, parent):
        self._parent = parent

    def list_datasets(self, start=0, count=999999999, search=None):
        datasets = self._parent.remote_backend.list_datasets(start, count, search)

        if self._parent.has_print():
            table = get_default_table()
            table.column_headers = ["ID", "Name", "Type", "#att", "created"]
            ch_it = _wheel_char(9999999999)
            self._print("Loading.....")
            for ds in datasets:
                print(next(ch_it), end="")
                table.append_row([str(x) for x in [ds.id, ds.name, ds.type, ds.num_attributes, ds.metadata["createdAt"]]])
            self._print(table)
        return datasets

    def do_default_imports(self, sklearn=True):
        if sklearn:
            for ds in padre.ds_import.load_sklearn_toys():
               self.do_import(ds)

    def _print(self, output):
        self._parent.print(output)

    def has_printer(self):
        return self._parent.has_print()

    def do_import(self, ds):
        if self.has_printer():
            self._print("Uploading dataset %s, %s, %s" % (ds.name, str(ds.size), ds.type))
        self._parent.remote_backend.upload_dataset(ds, True)

    def upload_scratchdatasets(self,auth_token,max_threads=8,upload_graphs=True):
        if(max_threads<1 or max_threads>50):
            max_threads=2
        if("api"in _BASE_URL):
            url=_BASE_URL.strip("/api")
        else:
            url=_BASE_URL
        padre.ds_import.sendTop100Datasets_multi(auth_token,url,max_threads)
        print("All openml datasets are uploaded!")
        if(upload_graphs):
            padre.ds_import.send_top_graphs(auth_token,url,max_threads>=3)




    def get_dataset(self, dataset_id, binary=True, format=formats.numpy,
            force_download=True, cache_it=False):
        # todo check force_download=False and cache_it True
        ds = None
        if not force_download: # look in cache first
            ds = self._parent.local_backend.get_dataset(dataset_id)
        if ds is None: # no cache or not looked --> go to http client
            ds = self._parent.remote_backend.get_dataset(dataset_id, binary, format=format)
            if cache_it:
                self._parent.local_backend.put_dataset(ds)

        if self.has_printer():
            self._print(f"Metadata for dataset {ds.id}")
            for k, v in ds.metadata.items():
                self._print("\t%s=%s" % (k, str(v)))
            self._print("Available formats:")
            formats = self._parent.remote_backend.get_dataset_formats(dataset_id)
            for f in formats:
                self._print("\t%s" % (f))
            self._print("Binary description:")
            for k, v in ds.describe().items():
                # todo printing the statistics is not ideal. needs to be improved
                if k == "stats" and isinstance(v, DescribeResult):
                    table = get_default_table()
                    h = ["statistic"]
                    for a in ds.attributes:
                        h.append(a.name)
                    table.column_headers = h
                    for m in [("min", v.minmax[0]), ("max", v.minmax[1]), ("mean", v.mean),
                              ("kurtosis", v.kurtosis), ("skewness", v.skewness)]:
                        r = [m[0]]
                        for val in m[1]: r.append(val)
                        table.append_row(r)
                    self._print(table)
                else:
                    self._print("\t%s=%s" % (k, str(v)))
        return ds

class ExperimentApp:
    """
    Class providing commands for managing datasets.
    """
    def __init__(self, parent):
        self._parent = parent

    def delete_experiments(self, search):
        """
           lists the experiments and returns a list of experiment names matching the criterions
           :param search: str to search experiment name only or
           dict object with format {field : regexp<String>} pattern to search in particular fields using a regexp.
           None for all experiments
        """
        if isinstance(search, dict):
            s = copy.deepcopy(search)
            file_name = s.pop("name")
        else:
            file_name = search
            s = None

        self._parent.local_backend.experiments.delete_experiments(search_id=file_name, search_metadata=s)



    def list_experiments(self, search=None, start=-1, count=999999999, ):
        """
        lists the experiments and returns a list of experiment names matching the criterions
        :param search: str to search experiment name only or
        dict object with format {field : regexp<String>} pattern to search in particular fields using a regexp.
        None for all experiments
        :param start: start in the list to be returned
        :param count: number of elements in the list to be returned
        :return:
        """
        if search is not None:
            if isinstance(search, dict):
                s = copy.deepcopy(search)
                file_name = s.pop("name")
            else:
                file_name = search
                s = None
            return _sub_list(self._parent.local_backend.experiments.list_experiments(search_id=file_name,
                                                                                     search_metadata=s)
                             , start, count)
        else:
            return _sub_list(self._parent.local_backend.experiments.list_experiments(), start, count)

    def list_runs(self, ex_id, start=-1, count=999999999, search=None):
        return _sub_list(self._parent.local_backend.experiments.list_runs(ex_id), start, count)

    def run(self, **ex_params):
        """
        runs an experiment either with the given parameters or, if there is a parameter decorated=True, runs all
        decorated experiments.
        Befor running the experiments, the backend for storing results is configured as file_repository.experiments
        :param ex_params: kwargs for an experiment or decorated=True
        :return:
        """
        if "decorated" in ex_params and ex_params["decorated"]:
            from padre.decorators import run
            return run(backend=self._parent.local_backend.experiments)
        else:
            p = ex_params.copy()
            p["backend"] = self._parent.local_backend.experiments
            ex = Experiment(**p)
            ex.run()
            return ex


class PadreApp:

    # todo improve printing. Configure a proper printer or find a good ascii printing package

    def __init__(self, config=None, printer=None):
        if config is None:
            self._config = PadreConfig()
        self._offline = "offline" not in self._config.general or self._config.general["offline"]
        self._http_repo = PadreHTTPClient(**self._config.http_backend_config)
        self._file_repo = PadreFileBackend(**self._config.local_backend_config)
        self._dual_repo = DualBackend(self._file_repo, self._http_repo)
        self._print = printer
        self._dataset_app = DatasetApp(self)
        self._experiment_app = ExperimentApp(self)
        self._experiment_creator = ExperimentCreator()
        self._metrics_evaluator = CompareMetrics()
        self._metrics_reevaluator = ReevaluationMetrics()

    @property
    def offline(self):
        """
        sets the current offline / online status of the app. Permanent changes need to be done via the config.
        :return: True, if requests are not passed to the server
        """
        return self._offline

    @offline.setter
    def set_offline(self, offline):
        self._offline = offline

    @property
    def datasets(self):
        return self._dataset_app

    @property
    def experiments(self):
        return self._experiment_app

    @property
    def experiment_creator(self):
        return self._experiment_creator

    @property
    def metrics_evaluator(self):
        return self._metrics_evaluator

    @property
    def metrics_reevaluator(self):
        return self._metrics_reevaluator

    @property
    def config(self):
        return self._config

    def set_printer(self, printer):
        """
        sets the printer, i.e. the output of console text. If None, there will be not text output
        :param printer: object with .print(str) function like sys.stdout or None
        """
        self._print = printer

    def status(self):
        """
        returns the status of the app, i.e. if the server is running, the client, the config etc.
        :return:
        """
        pass

    def print(self, output):
        if self.has_print():
            self._print(output)

    def has_print(self):
        return self._print is not None

    @property
    def remote_backend(self):
        return self._http_repo

    @property
    def local_backend(self):
        return self._file_repo

    @property
    def repository(self):
        return self._dual_repo


pypadre = PadreApp()   # load the default app
