from django.urls import path, re_path
from FROB.constant_values import api_versions
from app_data.view_files import homepage, bookclub, booktalk, book, event, test_data


urlpatterns = [
    re_path(rf'^(?P<version>[{api_versions}]+)/home/$', homepage.Part1.as_view(), name='homepage-part1'),
    re_path(rf'^(?P<version>[{api_versions}]+)/(?P<pk>[0-9a-f-]+)/bookclub/$', bookclub.BookClubAPI.as_view(), name='detail-bookclub'),
    re_path(rf'^(?P<version>[{api_versions}]+)/user/(?P<pk>[0-9a-f-]+)/booktalk/$', booktalk.UserBookTalksAPI.as_view(), name='user-booktalk'),
    re_path(rf'^(?P<version>[{api_versions}]+)/(?P<pk>[0-9a-f-]+)/booktalk/$', booktalk.BookTalkDetailAPI.as_view(), name='detail-booktalk'),
    re_path(rf'^(?P<version>[{api_versions}]+)/comment/(?P<pk>[0-9a-f-]+)/booktalk/$', booktalk.BookTalkCommentAPI.as_view(), name='comment-booktalk'),
    re_path(rf'^(?P<version>[{api_versions}]+)/(?P<pk>[0-9a-f-]+)/book/$', book.BookDetailAPI.as_view(), name='detail-book'),
    re_path(rf'^(?P<version>[{api_versions}]+)/(?P<pk>[0-9a-f-]+)/event/$', event.EventDetailAPI.as_view(), name='detail-event'),
    re_path(rf'^(?P<version>[{api_versions}]+)/attend/(?P<pk>[0-9a-f-]+)/event/$', event.EventAttendAPI.as_view(), name='attend-event'),


    # TEST API'S
    re_path(rf'^(?P<version>[{api_versions}]+)/test/(?P<pk>[0-9a-f-]+)/data1/$', test_data.AddTestData1.as_view(), name='add-test-data'),
    re_path(rf'^(?P<version>[{api_versions}]+)/test/data2/$', test_data.AddTestData2.as_view(), name='add-test-data2'),
    re_path(rf'^(?P<version>[{api_versions}]+)/test/data3/$', test_data.AddTestData3.as_view(), name='add-test-data3'),

]
