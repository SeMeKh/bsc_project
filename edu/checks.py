import inspect

from edu.models import Enrollment, EnrollmentError
from insanity.sanity_check import SanityCheck


class EnrollmentCheck1(SanityCheck):
    action_name = 'edu.models.Offering.enroll'

    def given(check, self, student, **payload):
        check.old_capacity = self.available_capacity
        return True

    def when(check, commit, **payload):
        return commit

    def then(check, payload, return_value, exc_type, **kwargs):
        assert exc_type is None
        assert check.old_capacity > 0
        assert payload['self'].available_capacity == check.old_capacity - 1
        assert isinstance(return_value, Enrollment)
        print('checked1')


class EnrollmentCheck2(SanityCheck):
    action_name = 'edu.models.Offering.enroll'

    def given(check, self, **payload):
        return self.available_capacity == 0

    def then(check, exc_type, **kwargs):
        assert issubclass(exc_type, EnrollmentError)
        print('checked2')


class EnrollmentCheck3(SanityCheck):
    action_name = 'edu.models.Offering.enroll'

    def then(check, payload, **kwargs):
        offering = payload['self']
        assert offering.capacity - offering.available_capacity == Enrollment.objects.filter(offering=offering).count()
        print('checked3')


class SampleContextCheck4(SanityCheck):
    action_name = 'offeringCapacityChangeByStaff'

    def then(check, payload, **kwargs):
        offering = payload['offering']
        assert offering.capacity - offering.available_capacity == Enrollment.objects.filter(offering=offering).count()
        print('checked4')


class SampleContextCheck5(SanityCheck):
    action_name = 'offeringCapacityChangeByStaff'

    def then(check, payload, **kwargs):
        offering = payload['offering']
        assert not offering.is_enrollable
        print('checked5')
