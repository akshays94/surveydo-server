from django.conf import settings
from django.urls import path, re_path, include, reverse_lazy
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic.base import RedirectView
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views
from .app.viewsets.user import UserViewSet
from .app.viewsets.user import UserCreateViewSet
from .app.viewsets.user import CustomAuthToken
from .app.viewsets.user import LogoutViewSet
from .app.viewsets.survey import SurveyViewSet
from .app.viewsets.question import SurveyQuestionViewSet
from .app.viewsets.health_check import HealthCheckViewSet

router = DefaultRouter()
router.register(r'v1/users', UserViewSet)
router.register(r'v1/register-users', UserCreateViewSet)
router.register(r'v1/auth', LogoutViewSet, basename='logout')
router.register(r'v1/surveys', SurveyViewSet, basename='surveys')
router.register(r'v1/questions', SurveyQuestionViewSet, basename='questions')
router.register(r'v1/health-check', HealthCheckViewSet, basename='health-check')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('login/', CustomAuthToken.as_view()),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    # the 'api-root' from django rest-frameworks default router
    # http://www.django-rest-framework.org/api-guide/routers/#defaultrouter
    re_path(r'^$', RedirectView.as_view(url=reverse_lazy('api-root'), permanent=False)),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
