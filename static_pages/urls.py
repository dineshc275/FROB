from django.urls import path

from static_pages import views

urlpatterns = [
    path('', views.PageLoadView.as_view()),
]
