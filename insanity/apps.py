import logging
import importlib
import inspect
from collections import defaultdict
from django.apps import AppConfig, apps
from insanity.scenario import Scenario

logger = logging.getLogger('insanity')

all_scenarios = defaultdict(list)
all_stats = dict()

STATS_FAIL = 'fail'
STATS_COUNT = 'count'
STATS_PASS = 'pass'


def fqn(cls):
    return '%s.%s' % (cls.__module__, cls.__name__)


def report_exec(scenario, fail):
    name = fqn(scenario.__class__)
    stats = all_stats[name]
    if fail:
        stats[STATS_FAIL] += 1
    else:
        stats[STATS_PASS] += 1
    stats[STATS_COUNT] += 1


class InsanityConfig(AppConfig):
    name = 'insanity'

    def ready(self):
        logging.info("Harvesting")
        for _, app in apps.app_configs.items():
            module = app.module
            scenario_name = module.__name__ + '.scenarios'
            try:
                scenarios = importlib.import_module(scenario_name)

                for name, obj in inspect.getmembers(scenarios, inspect.isclass):
                    if obj.__module__ == scenario_name and issubclass(obj, Scenario):
                        _name = fqn(obj)
                        all_stats[_name] = {
                            STATS_FAIL: 0,
                            STATS_COUNT: 0,
                            STATS_PASS: 0,
                        }
                        all_scenarios[obj.action_name].append(obj)
            except:
                pass
