from django_tables2 import columns

from edu.models import Offering
from edu.views.generic import create_basic_crud

offering_views = create_basic_crud(
    Offering, 'professor_offering',
    list_fields=[],
    list_columns=dict(
        semester=columns.Column(accessor='semester.name', verbose_name='Semester'),
        course=columns.Column(accessor='course.name', verbose_name='Course'),
    ),
)
