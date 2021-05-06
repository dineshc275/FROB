import logging
import datetime
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.utils import timezone
from django.utils.datastructures import MultiValueDictKeyError
from rest_framework import status
from rest_framework.exceptions import ParseError, ValidationError
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from FROB.constant_values import default_query_1, source_list
from FROB.project_utils import CustomMessage
from app_data.models import Banner
from app_data.serializers import HomepagePart1BannerV1Serializer, HomepagePart1BookReadV1Serializer, \
    HomepagePart1BookClubV1Serializer, HomepagePart1BookTalkV1Serializer, HomepagePart1BookV1Serializer, \
    HomepagePart1EventV1Serializer
from book.models import BookRead, BookTalk, Book
from book_club.models import BookClub, Event, BookClubFollower, BookClubBook

logger = logging.getLogger(__name__)


class Part1(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, version):
        try:
            source_type = request.query_params["source_type"]
            if source_type not in source_list:
                raise CustomMessage("Source Type is invalid")
            if version == "v1":
                banner_obj = Banner.objects.filter(default_query_1 & Q(start_timestamp__lte=timezone.now()) &
                                    (Q(end_timestamp__gte=timezone.now()) | Q(end_timestamp__isnull=True)))
                banner_serializer_data = HomepagePart1BannerV1Serializer(banner_obj, many=True).data

                book_read_obj = BookRead.objects.filter(default_query_1 & Q(user=request.user))
                if not book_read_obj:
                    book_read_serializer_data = HomepagePart1BookReadV1Serializer(book_read_obj, many=True).data
                else:
                    book_read_obj = Book.objects.filter(default_query_1).order_by("-visit_count")
                    book_read_serializer_data = HomepagePart1BookV1Serializer(book_read_obj, many=True).data

                book_club_following = BookClubFollower.objects.filter(default_query_1 & Q(receiver=request.user) &
                                                                  Q(receiver_status=True)).select_related("bookclub")
                book_club_following_serializer_data = HomepagePart1BookClubV1Serializer(book_club_following, many=True).data

                book_club_following_list = book_club_following.values_list("id", flat=True)

                book_club_obj = BookClub.objects.filter(Q(is_deleted=False) & Q(is_active=True)).exclude(
                    id__in=book_club_following_list).order_by("-visit_count")
                book_club_serializer_data = HomepagePart1BookClubV1Serializer(book_club_obj, many=True).data

                book_club_list = book_club_following.values_list("bookclub", flat=True)
                book_club_user_book_list = BookClubBook.objects.filter(default_query_1 & Q(bookclub__in=book_club_list)).values_list("book", flat=True)
                # book_club_user_book_list = book_club_following.books.all().values_list("book", flat=True)

                book_talk_obj = BookTalk.objects.filter(default_query_1 & Q(book__in=book_club_user_book_list))
                book_talk_serializer_data = HomepagePart1BookTalkV1Serializer(book_talk_obj, many=True).data
                if book_club_following_list:
                    upcoming_event_obj = Event.objects.filter(default_query_1 & Q(bookclub__in=book_club_following_list) & Q(from_timestamp__gte=timezone.now()))
                else:
                    upcoming_event_obj = Event.objects.filter(default_query_1 & Q(from_timestamp__gte=timezone.now()))

                upcoming_event_serializer_data = HomepagePart1EventV1Serializer(upcoming_event_obj, many=True).data

                return Response({"is_success": True, "message": "Success", "data":
                    {"banner": banner_serializer_data, "book_read": book_read_serializer_data,
                     "book_club_following": book_club_following_serializer_data, "book_talk": book_talk_serializer_data,
                     "book_club_interests": book_club_serializer_data, "upcoming_event": upcoming_event_serializer_data}},
                    status=status.HTTP_200_OK)
            else:
                raise CustomMessage("Version is invalid")

        except CustomMessage as e:
            return Response({"data": {"is_success": False, "message": e.message}}, status=status.HTTP_200_OK)
        except (ParseError, ZeroDivisionError, MultiValueDictKeyError, KeyError, ValueError, ValidationError,
                ObjectDoesNotExist):
            logger.info(f"class name: {self.__class__.__name__},request: {request.data}")
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"class name: {self.__class__.__name__},request: {request.data}, message: str({e})")
            return Response({"status": status.HTTP_500_INTERNAL_SERVER_ERROR, "message": "fail", "raw_message": str(e)})
