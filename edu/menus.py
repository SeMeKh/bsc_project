# Add two items to our main menu
from django.core.urlresolvers import reverse
from menu import Menu, MenuItem

professor_children = (
    MenuItem("My Offerings", reverse('professor_offering_list')),
)

Menu.add_item('main', MenuItem("Professor Panel",
                               reverse('index'),
                               weight=10,
                               children=professor_children,
                               check=lambda request: hasattr(request.user, 'professor'),
                               ))

student_children = (
    MenuItem("My Courses", reverse('student_enrollment_list')),
)

Menu.add_item('main', MenuItem("Student Panel",
                               reverse('student'),
                               weight=20,
                               children=student_children,
                               check=lambda request: hasattr(request.user, 'student'),
                               ))

staff_children = (
    MenuItem("Users", reverse('staff_user_list')),
    MenuItem("Students", reverse('staff_student_list')),
    MenuItem("Professors", reverse('staff_professor_list')),
    MenuItem("Courses", reverse('staff_course_list')),
    MenuItem("Semesters", reverse('staff_semester_list')),
    MenuItem("Offerings", reverse('staff_offering_list')),
)

Menu.add_item('main', MenuItem("Staff Panel",
                               reverse('staff'),
                               weight=20,
                               children=staff_children,
                               check=lambda request: request.user.is_staff,
                               ))

Menu.add_item('main', MenuItem("Django Admin",
                               '/admin/',
                               check=lambda request: request.user.is_superuser,
                               ))
