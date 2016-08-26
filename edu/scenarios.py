import inspect

from edu.models import Enrollment, EnrollmentError
from insanity.scenario import Scenario


class EnrollmentScenario1(Scenario):
    action_name = 'edu.models.Offering.enroll'

    def given(scenario, o1, s2, **payload):
        scenario.old_capacity = o1.available_capacity
        return True

    def when(scenario, commit, **payload):
        return commit

    def then(scenario, payload, return_value, exc_type, **kwargs):
        assert scenario.old_capacity > 0
        assert payload['self'].available_capacity == scenario.old_capacity - 1


class EnrollmentScenario2(Scenario):
    action_name = 'edu.models.Offering.enroll'

    def then(scenario, payload, **kwargs):
        o1 = payload['self']
        used_capacity = o1.capacity - o1.available_capacity
        enrollment_count = Enrollment.objects.filter(offering=o1).count()
        assert used_capacity == enrollment_count


class EnrollmentScenario3(Scenario):
    action_name = 'edu.models.Offering.enroll'

    def given(scenario, self, **payload):
        return self.available_capacity == 0

    def then(scenario, exc_type, **kwargs):
        assert issubclass(exc_type, EnrollmentError)
        print('checked2')


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
