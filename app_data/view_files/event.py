import logging
import datetime
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.utils.datastructures import MultiValueDictKeyError
from rest_framework import status
from rest_framework.exceptions import ParseError, ValidationError
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from FROB.constant_values import default_query_1, source_list
from FROB.project_utils import CustomMessage
from app_data.serializers import BookClubAPIV1Serializer, UserAccountV1Serializer, EventSubscribeV1Serializer
from book.models import Book, BookRead
from book_club.models import BookClub, Event, EventSubscribe

logger = logging.getLogger(__name__)


class EventDetailAPI(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, version, pk):
        try:
            source_type = request.query_params["source_type"]
            if source_type not in source_list:
                raise CustomMessage("Source Type is invalid")
            if version == "v1":
                try:
                    event_obj = Event.objects.get(default_query_1 & Q(id=pk))
                except Event.DoesNotExist:
                    raise CustomMessage("Event Doesn't Exist")
                event_serializer_data = BookClubAPIV1Serializer(event_obj, many=False).data
                attending_user_obj = EventSubscribe.objects.filter(default_query_1 & Q(event=pk))
                attending_user_serializer_data = EventSubscribeV1Serializer(attending_user_obj, many=True).data
                return Response({"is_success": True, "message": "Success", "data": {"event_data": event_serializer_data,
                                "attending_user_data": attending_user_serializer_data}}, status=status.HTTP_200_OK)
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


class EventAttendAPI(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, version, pk):
        try:
            source_type = request.query_params["source_type"]
            if source_type not in source_list:
                raise CustomMessage("Source Type is invalid")
            if version == "v1":
                try:
                    event_obj = Event.objects.get(default_query_1 & Q(id=pk))
                except Event.DoesNotExist:
                    raise CustomMessage("Event doesn't exist")
                attending_user_obj = EventSubscribe.objects.create(event=event_obj, user=request.user, is_subscribed=True,
                                                          is_attending=True)
                attending_user_serializer_data = EventSubscribeV1Serializer(attending_user_obj, many=True).data
                return Response({"is_success": True, "message": "Success", "data": attending_user_serializer_data},
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
