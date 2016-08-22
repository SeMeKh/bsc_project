from decorator_include import decorator_include
from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.urlresolvers import reverse_lazy
from django.http.response import HttpResponseForbidden
from django.views.generic.base import RedirectView, TemplateView, View
from functools import wraps
from edu.models import Student, Professor
from edu.views import index, student, staff, professor


def student_required(view):
    @login_required
    @wraps(view)
    def wrapper(request, *args, **kwargs):
        try:
            kwargs['student'] = request.user.student
        except Student.DoesNotExist:
            return HttpResponseForbidden()
        return view(request, *args, **kwargs)

    return wrapper


def professor_required(view):
    @login_required
    @wraps(view)
    def wrapper(request, *args, **kwargs):
        try:
            kwargs['professor'] = request.user.professor
        except Professor.DoesNotExist:
            return HttpResponseForbidden()
        return view(request, *args, **kwargs)

    return wrapper


def basic_crud(name_prefix, create_view=None, list_view=None, edit_view=None, delete_view=None):
    urls = []
    for regex, view, name_suffix in (
        (r'^create/$', create_view, '_create'),
        (r'^$', list_view, '_list'),
        (r'^(?P<pk>\d+)/edit/$', edit_view, '_edit'),
        (r'^(?P<pk>\d+)/delete/$', delete_view, '_delete'),
    ):
        if view is None:
            continue
        if issubclass(view, View):
            view = view.as_view()
        urls.append(url(regex, view, name=name_prefix + name_suffix))
    return urls


staff_required = user_passes_test(lambda user: user.is_staff)

student_urls = [
    url(r'^$', RedirectView.as_view(url=reverse_lazy('student_enrollment_list')), name='student'),
    url(r'^enrollments/', include(basic_crud('student_enrollment', **student.enrollment_views))),
]

professor_urls = [
    url(r'^$', TemplateView.as_view(template_name='edu/dashboard.html'), name='professor'),
    url(r'^offerings/', include(basic_crud('professor_offering', **professor.offering_views))),
]

staff_urls = [
    url(r'^$', RedirectView.as_view(url=reverse_lazy('staff_student_list')), name='staff'),
    url(r'^users/', include(basic_crud('staff_user', **staff.user_views))),
    url(r'^students/', include(basic_crud('staff_student', **staff.student_views))),
    url(r'^professors/', include(basic_crud('staff_professor', **staff.professor_views))),
    url(r'^courses/', include(basic_crud('staff_course', **staff.course_views) + [
        url(r'^(?P<pk>\d+)/capacity/$', staff.OfferingChangeCapacityView.as_view(), name='staff_offering_capacity')
    ])),
    url(r'^semesters/', include(basic_crud('staff_semester', **staff.semester_views))),
    url(r'^offering/', include(basic_crud('staff_offering', **staff.offering_views))),
]

urlpatterns = [
    url(r'^$', index.IndexView.as_view(), name='index'),
    url(r'^student/', decorator_include(student_required, student_urls)),
    url(r'^professor/', decorator_include(professor_required, professor_urls)),
    url(r'^staff/', decorator_include(staff_required, staff_urls)),
    url(r'^admin/', admin.site.urls),
    url(r'^hijack/', include('hijack.urls')),
    url(r'^accounts/', include('django.contrib.auth.urls')),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
