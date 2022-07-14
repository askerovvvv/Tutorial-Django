from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView

from account.views import *

urlpatterns = [
    path('register/', RegisterApiView.as_view()),
    path('login/', TokenObtainPairView.as_view()),
    path('activate/<uuid:activation_code>/', ActivationView.as_view()),
    path('forgotpassword/', ForgotPasswordApiView.as_view()),
    path('forgotpasswordcomplete/', ForgotPasswordCompleteApiView.as_view())

]

