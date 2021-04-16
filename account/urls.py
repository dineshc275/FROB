from django.urls import path

from account import views

urlpatterns = [
    path('otp/generate/', views.GenerateOtp.as_view()),
    path('otp/verify/', views.VerifyOtp.as_view()),
    path('login/', views.Login.as_view()),
    path('detail/', views.UpdateDetail.as_view()),
]
