"""
Structure of Event Handling Mechanism in PyPaDRe
The event emitter fires only a single event called EVENT. In the argument to the event, the actual event name is passed
along with the required arguments to the Event Handler Function.

Each fired event is pushed to a queue, and gets handled one after the other. The logger_list variable contains the list 
of loggers that are to be used to handle the events. A single event can be handled by multiple loggers if needed. A 
single event can trigger multiple functions too.
"""


"""
This list contains the list of loggers which log each event occuring in the experiment. These functions call the 
corresponding functions in the logger after extracting the required arguments required by the logger function.
"""
from pymitter import EventEmitter
logger_list = []

def log_start_experiment(args):
    experiment = args.get('experiment', None)
    append_runs = args.get('append_runs', False)

    if experiment is not None:
        for logger in logger_list:
            logger.log_start_experiment(experiment=experiment, append_runs=append_runs)


def log_stop_experiment(args):
    experiment = args.get('experiment', None)

    if experiment is not None:
        for logger in logger_list:
            logger.log_stop_experiment(experiment=experiment)


def put_experiment_configuration(args):
    experiment = args.get('experiment', None)

    if experiment is not None:
        for logger in logger_list:
            logger.put_experiment_configuration(experiment=experiment)


def log_start_run(args):
    run = args.get('run', None)
    if run is not None:
        for logger in logger_list:
            logger.log_start_run(run=run)


def log_stop_run(args):
    run = args.get('run', None)
    if run is not None:
        for logger in logger_list:
            logger.log_stop_run(run=run)


def log_start_split(args):
    split = args.get('split', None)
    if split is not None:
        for logger in logger_list:
            logger.log_start_split(split=split)


def log_stop_split(args):
    split = args.get('split', None)
    if split is not None:
        for logger in logger_list:
            logger.log_stop_split(split=split)


def log_score(args):
    source = args.get('source', None)
    parameters = args.get('parameters', None)
    if source is not None and parameters is not None:
        for logger in logger_list:
            logger.log_score(source, **parameters)


def log_results(args):
    source = args.get('source', None)
    parameters = args.get('parameters', None)
    if source is not None and parameters is not None:
        for logger in logger_list:
            logger.log_results(source, **parameters)


def log_event(args):
    source = args.get('source', None)
    parameters = args.get('parameters', None)
    kind = args.get('kind', None)
    if source is not None and parameters is not None:
        for logger in logger_list:
            logger.log_event(source, kind, **parameters)


def log(args):
    print(args)


def warn(args):
    pass


def error(args):
    source = args.get('source', None)
    message = args.get('message', None)
    condition = args.get('condition', False)
    for logger in logger_list:
        # The condition is set as False as the condition is already validated
        logger.error(condition, source, message)



"""
This dictionary contains all the events that are to be handled and also their corresponding event handling function
"""
EVENT_HANDLER_DICT = {
    'EVENT_START_EXPERIMENT': [log_start_experiment],
    'EVENT_STOP_EXPERIMENT': [log_stop_experiment],
    'EVENT_START_RUN': [log_start_run],
    'EVENT_STOP_RUN': [log_stop_run],
    'EVENT_START_SPLIT': [log_start_split],
    'EVENT_STOP_SPLIT': [log_stop_split],
    'EVENT_PUT_EXPERIMENT_CONFIGURATION': [put_experiment_configuration],
    'EVENT_LOG_SCORE': [log_score],
    'EVENT_LOG_RESULTS': [log_results],
    'EVENT_LOG_EVENT': [log_event],
    'EVENT_LOG': [log],
    'EVENT_WARN': [warn],
    'EVENT_ERROR': [error]
}

"""
The event names are taken from the event handler dictionary
"""
EVENT_NAMES = list(EVENT_HANDLER_DICT.keys())

"""
As each event occurs, the event is pushed into the event queue, this would allow the events to be handled at their own 
pace and would not cause any out of order event handling(like closing the experiment while results are being written to 
the backend)
"""
EVENT_QUEUE = []
class event_queue:
    _event_queue = []
    _emptying_queue = False

    def __del__(self):
        """
        Check for any pending events in the event queue and process the events
        :return:
        """
        if self._event_queue:
            log(source=self, message=f"Event Queue is not empty. Emtpying Queue")
        self.process_events()

    def process_events(self):
        """
        This function processes the events currently pending in the queue.
        Functions corresponding to each event are obtained from the EVENT_HANDLER_DICT
        :return:
        """

        while self._event_queue:
            """
            The event should contain the EVENT_NAME and the args for the function call
            Args is a dictionary which would be unwrapped by the corresponding function call to obtain the required
            parameters
            """
            self._emptying_queue = True
            event = self._event_queue.pop(0)
            event_handlers = EVENT_HANDLER_DICT.get(event['EVENT_NAME'], None)
            if event_handlers is None:
                """
                UNHANDLED EVENT ENCOUNTERED
                """
                log(source=self, message='Unhandled event encountered ' + event['EVENT_NAME'])
            else:
                args = event.get('args', None)
                # If there are multiple event handlers for the same event, iterate through each handler
                if len(event_handlers) > 1:
                    for event_handler in event_handlers:
                        event_handler(args=args)
                else:
                    event_handlers[0](args)

        self._emptying_queue = False

    @property
    def event_queue(self):
        return self._event_queue

    @event_queue.setter
    def event_queue(self, event):
        self._event_queue.append(event)
        if not self._emptying_queue:
            # Create thread and empty queue
            self.process_events()


event_queue_obj = event_queue()

"""
This list contains all the loggers for the experiment. Each logger can have a backend. In this way the experiment 
can support multiple loggers and multiple backends
"""
logger_list = []


def add_event_to_queue(args):
    """
    This function appends the newly fired event to the event queue
    :param args: Arguments to be used for the event
    :return:
    """
    event_queue_obj.event_queue = args

eventemitter = EventEmitter()
eventemitter.on('EVENT', add_event_to_queue)


def trigger_event(event_name, **args):
    """
    This function provides a simplified interface to wrap all event related code and fire the event
    :param event_name: Name of the event
    :param args: Parameters to be passed to the event
    :return: None
    """
    event_dict = {'EVENT_NAME': event_name,
                  'args': args}

    eventemitter.emit('EVENT', event_dict)


def assert_condition(**args):
    """
    This function checks for the condition and if the condition is not true, triggers an exception
    :param condition: The condition to be checked
    :param source: Source of the condition
    :param message: Message to be logged if the condition fails
    :return:
    """

    error_event_handlers = EVENT_HANDLER_DICT.get('EVENT_ERROR')
    for logger in logger_list:
        for error_event_handler in error_event_handlers:
            error_event_handler(args)


def add_logger(logger):
    """
    This function appends a new logger to the list of loggers
    :param logger: The logger to be appended to the list
    :return:
    TODO: Create an abstract base class for loggers so that all functions are uniform among all the loggers
    """
    if logger is not None:
        logger_list.append(logger)

