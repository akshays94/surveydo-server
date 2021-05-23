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

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'register-users', UserCreateViewSet)
router.register(r'auth', LogoutViewSet, basename='logout')
router.register(r'surveys', SurveyViewSet, basename='surveys')
router.register(r'questions', SurveyQuestionViewSet, basename='questions')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(router.urls)),
    path('login/', CustomAuthToken.as_view()),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    # the 'api-root' from django rest-frameworks default router
    # http://www.django-rest-framework.org/api-guide/routers/#defaultrouter
    re_path(r'^$', RedirectView.as_view(url=reverse_lazy('api-root'), permanent=False)),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
