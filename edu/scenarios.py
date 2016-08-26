import inspect

from edu.models import Enrollment, EnrollmentError
from insanity.scenario import Scenario


class EnrollmentScenario1(Scenario):
    action_name = 'edu.models.Offering.enroll'

    def given(scenario, self, student, **payload):
        scenario.old_capacity = self.available_capacity
        return True

    def when(scenario, commit, **payload):
        return commit

    def then(scenario, payload, return_value, exc_type, **kwargs):
        assert exc_type is None
        assert scenario.old_capacity > 0
        assert payload['self'].available_capacity == scenario.old_capacity - 1
        assert isinstance(return_value, Enrollment)
        print('checked1')


class EnrollmentScenario2(Scenario):
    action_name = 'edu.models.Offering.enroll'

    def given(scenario, self, **payload):
        return self.available_capacity == 0

    def then(scenario, exc_type, **kwargs):
        assert issubclass(exc_type, EnrollmentError)
        print('checked2')


class EnrollmentScenario3(Scenario):
    action_name = 'edu.models.Offering.enroll'

    def then(scenario, payload, **kwargs):
        offering = payload['self']
        assert offering.capacity - offering.available_capacity == Enrollment.objects.filter(offering=offering).count()
        print('checked3')


class SampleContextScenario4(Scenario):
    action_name = 'offeringCapacityChangeByStaff'

    def then(scenario, payload, **kwargs):
        offering = payload['offering']
        assert offering.capacity - offering.available_capacity == Enrollment.objects.filter(offering=offering).count()
        print('checked4')


class SampleContextScenario5(Scenario):
    action_name = 'offeringCapacityChangeByStaff'

    def then(scenario, payload, **kwargs):
        offering = payload['offering']
        assert not offering.is_enrollable
        print('checked5')
