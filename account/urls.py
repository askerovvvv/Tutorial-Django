from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView

from account.views import RegisterApiView, ActivationView

urlpatterns = [
    path('register/', RegisterApiView.as_view()),
    path('login/', TokenObtainPairView.as_view()),
    path('activate/<uuid:activation_code>/', ActivationView.as_view()),

]

