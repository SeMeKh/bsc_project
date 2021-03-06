from django.db import models
from django.apps import apps

from insanity.action import action


class Course(models.Model):
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name


class Student(models.Model):
    user = models.OneToOneField('auth.User', blank=True, null=True)

    def __str__(self):
        return 'Student%d' % (self.id or -1)


class Professor(models.Model):
    user = models.OneToOneField('auth.User', blank=True, null=True)

    def __str__(self):
        return self.user.get_full_name()


class EnrollmentError(Exception):
    pass


class ChangeCapacityError(Exception):
    pass


class Offering(models.Model):
    course = models.ForeignKey('edu.Course')
    semester = models.ForeignKey('edu.Semester')
    professor = models.ForeignKey('edu.Professor')
    capacity = models.IntegerField()
    available_capacity = models.IntegerField()
    is_enrollable = models.BooleanField(default=False)

    @action()
    def enroll(self, student, commit=True):
        if self.available_capacity == 0:
            raise EnrollmentError("There is no available capacity")
        if not self.is_enrollable:
            raise EnrollmentError("This offering is not enabled for enrollment")

        Enrollment = apps.get_model('edu.Enrollment')
        enrollment = Enrollment(offering=self, student=student)
        if commit:
            enrollment.save()
            self.available_capacity = self.available_capacity - 1
            self.save()
        return enrollment

    def get_students(self):
        return Student.objects.filter(id__in=self.enrollment_set.values_list('student', flat=True))

    @action()
    def change_capacity(self, new_capacity, commit=True):
        enrollment_count = self.capacity - self.available_capacity
        self.capacity = new_capacity
        self.available_capacity = new_capacity - enrollment_count
        if commit:
            self.save()


class Enrollment(models.Model):
    offering = models.ForeignKey('edu.Offering')
    student = models.ForeignKey('edu.Student')


class Semester(models.Model):
    name = models.CharField(max_length=16)

    def __str__(self):
        return self.name
