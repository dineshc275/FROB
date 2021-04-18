from django.urls import path

from book_club import views

urlpatterns = [
    path('', views.BookClubAPIView.as_view()),
]
