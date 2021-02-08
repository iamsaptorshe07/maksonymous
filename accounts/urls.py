from django.urls import path
from accounts import views
from .views import Verification

urlpatterns = [
    path('register', views.signup, name='signup'),
    path('', views.signup, name='login'),
    path('a', views.a, name='a'),
    path('login', views.login_, name='login_'),
    path('activate/<uidb64>/<token>', Verification.as_view(), name='activate'),
]
