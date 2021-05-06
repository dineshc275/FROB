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
from app_data.serializers import BookClubAPIV1Serializer, UserBookTalkV1Serializer, BookTalkCommentV1Serializer
from book.models import BookTalk, BookTalkComment
from book_club.models import BookClub

logger = logging.getLogger(__name__)


class UserBookTalksAPI(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, version, pk):
        try:
            source_type = request.query_params["source_type"]
            if source_type not in source_list:
                raise CustomMessage("Source Type is invalid")
            if version == "v1":
                booktalk_obj = BookTalk.objects.filter(default_query_1 & Q(talk_by=pk))
                serializer_data = UserBookTalkV1Serializer(booktalk_obj, many=True).data
                return Response({"is_success": True, "message": "Success", "data": serializer_data}, status=status.HTTP_200_OK)
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


class BookTalkDetailAPI(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, version, pk):
        try:
            source_type = request.query_params["source_type"]
            if source_type not in source_list:
                raise CustomMessage("Source Type is invalid")
            if version == "v1":
                try:
                    booktalk_obj = BookTalk.objects.filter(default_query_1 & Q(id=pk))
                except BookTalk.DoesNotExist:
                    raise CustomMessage("BookTalk Doesn't Exist")
                serializer_data = UserBookTalkV1Serializer(booktalk_obj, many=False).data
                return Response({"is_success": True, "message": "Success", "data": serializer_data}, status=status.HTTP_200_OK)
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


class BookTalkCommentAPI(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, version, pk):
        try:
            source_type = request.query_params["source_type"]
            if source_type not in source_list:
                raise CustomMessage("Source Type is invalid")
            if version == "v1":
                comment = request.query_params["comment"]
                try:
                    book_talk_obj = BookTalk.objects.get(id=pk)
                except BookTalk.DoesNotExist:
                    raise CustomMessage("Book Talk Doesn't Exist")
                book_talk_comment_obj = BookTalkComment.objects.create(book_talk=book_talk_obj, user=request.user, comment=comment)
                serializer_data = BookTalkCommentV1Serializer(book_talk_comment_obj, many=False).data
                return Response({"is_success": True, "message": "Success", "data": serializer_data}, status=status.HTTP_200_OK)
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
