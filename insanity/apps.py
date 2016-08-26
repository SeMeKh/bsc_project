import logging
import importlib
import inspect
from collections import defaultdict
from django.apps import AppConfig, apps
from insanity.scenario import Scenario

logger = logging.getLogger('insanity')

all_scenarios = defaultdict(list)


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
                        all_scenarios[obj.action_name].append(obj)
            except:
                pass
