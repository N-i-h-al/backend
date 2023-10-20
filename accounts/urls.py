
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from rest_framework.authtoken.views import obtain_auth_token

router = DefaultRouter()
router.register("user", views.UserViewSet, basename="user")


urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),
    path('login/', obtain_auth_token, name='login'),
    path('logout/',views.LogoutView.as_view(),name="user_logout")
]
urlpatterns += router.urls