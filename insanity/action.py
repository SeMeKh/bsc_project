import functools
import inspect
from insanity.apps import all_scenarios, report_exec


class Action(object):
    return_value = None
    exc_type = None
    exc_val = None
    exc_tb = None

    def __init__(self, name, payload):
        self.name = name
        self.payload = payload
        self._scenarios = []

    def __getitem__(self, item):
        return self.payload[item]

    def _collect_scenarios(self):
        for scenario_class in all_scenarios[self.name]:
            scenario = scenario_class(self)
            if scenario.when(**self.payload) and scenario.given(**self.payload):
                self._scenarios.append(scenario)

    def _assert_scenarios(self):
        for scenario in self._scenarios:
            try:
                scenario.then(exc_type=self.exc_type, exc_val=self.exc_val, exc_tb=self.exc_tb,
                              return_value=self.return_value, payload=self.payload)
                report_exec(scenario, fail=False)
            except:
                report_exec(scenario, fail=True)


class action(object):
    """
    ContextManager and Decorator for creating Action instances
    """

    def __init__(__insanity_self__, __insanity_action_name__=None, **payload):
        __insanity_self__.name = __insanity_action_name__
        __insanity_self__._payload = payload
        __insanity_self__._stack = []
        __insanity_self__._self_name = None

    def __enter__(self):
        if self.name is None:
            raise ValueError('Action should be decorator or have explicit name')
        action_instance = Action(self.name, self._payload)
        action_instance._collect_scenarios()
        self._stack.append(action_instance)
        return action_instance

    def __exit__(self, exc_type, exc_val, exc_tb):
        action_instance = self._stack.pop()
        action_instance.exc_type = exc_type
        action_instance.exc_val = exc_val
        action_instance.exc_tb = exc_tb
        action_instance._assert_scenarios()
        return False  # Do not suppress exception

    def rename_self(self, name):
        self._self_name = name
        return self

    def _build_context_manager(self, signature, name, args, kwargs):
        bound_signature = signature.bind(*args, **kwargs)
        bound_signature.apply_defaults()
        payload = dict(**self._payload, **bound_signature.arguments)
        return action(name, **payload)

    def _get_signature(self, func):
        s = inspect.signature(func)
        return s

    def __call__(self, func):
        name = self.name if self.name is not None else '%s.%s' % (func.__module__, func.__qualname__)
        signature = self._get_signature(func)

        @functools.wraps(func)
        def inner(*args, **kwargs):
            with self._build_context_manager(signature, name, args, kwargs) as action_instance:
                return_value = func(*args, **kwargs)
                action_instance.return_value = return_value
                return return_value

        return inner
