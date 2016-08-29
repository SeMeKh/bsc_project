from django.contrib.auth import get_user_model

from edu.factory import StudentFactory, CourseFactory, SemesterFactory, OfferingFactory, ProfessorFactory
from edu.models import Course, Student, Semester, Professor, Offering, EnrollmentError
import random


def run():
    User = get_user_model()
    User.objects.all().delete()
    User.objects.create_superuser('admin', 'admin@admin.com', '321321')

    Course.objects.all().delete()
    courses = CourseFactory.create_batch(10)
    for c in courses:
        c.save()

    Student.objects.all().delete()
    students = StudentFactory.create_batch(10)
    for s in students:
        s.user.save()
        s.save()

    Semester.objects.all().delete()
    semesters = SemesterFactory.create_batch(10)
    for s in semesters:
        s.save()

    Professor.objects.all().delete()
    professors = ProfessorFactory.create_batch(10)
    for p in professors:
        p.user.save()
        p.save()

    offerings = OfferingFactory.create_batch(20)
    for o in offerings:
        o.save()

    for i in range(10):
        offering = random.choice(list(Offering.objects.filter(available_capacity__gt=0, is_enrollable=True)))
        student = random.choice(students)
        offering.enroll(student)

    try:
        offering = random.choice(list(Offering.objects.filter(available_capacity=0)))
        student = random.choice(students)
        offering.enroll(student, commit=False)
    except EnrollmentError:
        "That's OK"
        pass

