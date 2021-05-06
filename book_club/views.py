import logging
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.utils.datastructures import MultiValueDictKeyError
from rest_framework import status
from rest_framework.exceptions import ParseError, ValidationError
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from FROB.project_utils import CustomMessage
from account.models import UserAccount
from book_club.models import BookClub, BookClubMedia
from book_club.serializers import BookClubSerializer

logger = logging.getLogger(__name__)


class BookClubAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        try:
            source_type = request.query_params["source_type"]
            key_user = request.data.get('key_user', None)
            if key_user:
                try:
                    key_user_obj = UserAccount.objects.get(id=key_user)
                except UserAccount.DoesNotExist:
                    raise CustomMessage("Key user ID is invalid")
            else:
                key_user_obj = None
            name = request.data['name']
            short_description = request.data.get('short_description', None)
            description = request.data.get('description', None)
            image_list = request.FILES.getlist('image')
            if len(image_list) > 1:
                raise CustomMessage("Cannot accept multiple images")
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                ip = x_forwarded_for.split(',')[0]
            else:
                ip = request.META.get('REMOTE_ADDR')

            book_club_obj = BookClub.objects.create(name=name, short_description=short_description,
                                                    description=description, created_user=request.user,
                                                    key_user=key_user_obj, ip=ip)
            if image_list:
                BookClubMedia.objects.create(image=image_list[0], book_club=book_club_obj)

            serializer_data = BookClubSerializer(book_club_obj).data

            return Response({"is_success": True, "data": serializer_data}, status=status.HTTP_200_OK)
        except CustomMessage as e:
            return Response({"data": {"is_success": False, "message": e.message}}, status=status.HTTP_200_OK)
        except (ParseError, ZeroDivisionError, MultiValueDictKeyError, KeyError, ValueError, ValidationError,
                ObjectDoesNotExist):
            logger.info(f"class name: {self.__class__.__name__},request: {request.data}")
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"class name: {self.__class__.__name__},request: {request.data}, message: str({e})")
            return Response({"status": status.HTTP_500_INTERNAL_SERVER_ERROR, "message": "fail", "raw_message": str(e)})
