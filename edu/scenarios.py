import inspect

from edu.models import Enrollment, EnrollmentError
from insanity.scenario import Scenario


class CapacityDecreasesByEnroll(Scenario):
    """
    Scenario: Capacity should decrease by enroll
    Given student s1, offering o1 with available capacity c0
    When s1 commits enrollment in o1
    Then available capacity of o1 should become c0-1
    """

    def given(scenario, self, student, **payload):
        scenario.s1 = student
        scenario.o1 = self
        scenario.c0 = self.available_capacity
        return True

    when = 'edu.models.Offering.enroll'

    def when_params(scenario, commit, **payload):
        return commit == True

    def then(scenario, payload, return_value, exc_type, **kwargs):
        assert scenario.o1.available_capacity == scenario.c0 - 1


class AvailableCapacityRemainsConsistentWhenCapacityChanges(Scenario):
    """
    Scenario: Available Capacity Remains Consistent When Capacity Changes
    Given offering o1
    When it's capacity changes
    Then it's available capacity should equal its total capacity minus number of it's enrollments
    And it's total capacity should remain at least as many as number of it's enrollments
    """

    def given(scenario, self):
        scenario.o1 = self
        return True

    when = 'edu.models.Offering.change_capacity'

    def then(scenario, payload, **kwargs):
        available_capacity = scenario.o1.available_capacity
        total_capacity = scenario.o1.capacity
        enrollment_count = scenario.o1.enrollment_set.count()
        assert available_capacity == total_capacity - enrollment_count
        assert total_capacity >= enrollment_count


class EnrollmentShouldFailForOfferingWithZeroCapacity(Scenario):
    """
    Scenario: Enrollment should fail for offering with zero capacity
    Given offering o1 with zero capacity
    When someone enrolls in it
    Then it should fail with error
    """

    def given(scenario, self, **payload):
        return self.available_capacity == 0

    when = 'edu.models.Offering.enroll'

    def then(scenario, exc_type, **kwargs):
        assert issubclass(exc_type, EnrollmentError)
