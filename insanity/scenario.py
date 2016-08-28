class Scenario(object):

    def __init__(scenario, action):
        scenario.action = action

    def given(scenario, **payload):
        return True

    when = None

    def when_params(scenario, **payload):
        return True

    def then(scenario, exc_type, exc_val, exc_tb, return_value, payload):
        assert exc_type is None
