from django.core.urlresolvers import reverse
from django.views.generic.base import TemplateView, RedirectView


class IndexView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        user = self.request.user
        if user is None:
            return reverse('login')
        if hasattr(user, 'student'):
            return reverse('student')
        if user.is_staff:
            return reverse('staff')
        if hasattr(user, 'professor'):
            return reverse('professor')
        return '/admin/auth/user/'
