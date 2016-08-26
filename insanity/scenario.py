class Scenario(object):
    action_name = None

    def __init__(scenario, action):
        scenario.action = action

    def given(scenario, **payload):
        return True

    def when(scenario, **payload):
        return True

    def then(scenario, exc_type, exc_val, exc_tb, return_value, payload):
        assert exc_type is None
