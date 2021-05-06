import logging
import datetime
import os
from PIL import Image, ImageDraw, ImageFont
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from django.core.files import File
from django.db.models import Q
from django.utils import timezone
from django.utils.datastructures import MultiValueDictKeyError
from django_extensions.settings import BASE_DIR
from rest_framework import status
from rest_framework.exceptions import ParseError, ValidationError
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from FROB.constant_values import default_query_1, source_list, project_path
from FROB.project_utils import CustomMessage
from account.models import UserAccount
from app_data.models import Banner
from app_data.serializers import BookClubAPIV1Serializer, UserAccountV1Serializer, UserAccountTest2V1Serializer
from book.models import Book, BookRead, Genre, BookGenre, ReadAlong, BookMedia, BookTalk, BookTalkComment
from book_club.models import BookClub, BookClubBook, BookClubMedia, BookClubFollower, BookClubKeyContributor, \
    BookClubKeyUser, Event, EventMedia, EventSubscribe
from random import randint as random_number
from random import choice as random_choice

logger = logging.getLogger(__name__)
file_name = "image_1.jpeg"


def pil_image(file_name, msg_text):
    W, H = 900, 500
    image = Image.new(mode="RGB", size=(W, H), color=(random_number(0,256), random_number(0,256), random_number(0,256)))
    draw = ImageDraw.Draw(image)
    fnt = ImageFont.truetype('arial.ttf', 60)
    draw.text((300, 200), msg_text, font=fnt, fill=(random_number(0,256), random_number(0,256), random_number(0,256)))
    image.save(file_name, dpi=(3000, 3000))


class AddTestData1(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, version, pk):
        try:
            source_type = request.query_params["source_type"]
            if source_type not in source_list:
                raise CustomMessage("Source Type is invalid")
            if version == "v1":
                # CREATING USERS
                pk = int(pk)
                for i in range(1, pk*4):
                    user_obj = UserAccount.objects.create_user(mobile=i, first_name=f"name_{i}",
                                                               email=f"test_{i}@test.com", password=f"Test_{i}_Test")
                    user_obj.media = File(file=open(file_name, 'rb'))
                    user_obj.save()
                    access_token = user_obj.generate_token(user_obj)["access"]
                    print("access token is ", access_token)
                print("--------------------- users created -----------------------------")
                # CREATING USER LIST
                user_list = UserAccount.objects.filter(default_query_1).values_list("id", flat=True)

                for i in range(1, pk * 2):
                    # GENRE CREATION
                    Genre.objects.create(name=f"Genre_{i}", description=f"{'description' * i}_{i}",
                                         visit_count=random_number(10, 50), manual_popularity=random_number(10, 20), created_user_id=random_choice(user_list))
                print("--------------------- genres created -----------------------------")

                # CREATING LIST OF GENRES
                genre_list = Genre.objects.filter(default_query_1).values_list("id", flat=True)
                # print("genre list is -------------- ", genre_list)
                # import pdb; pdb.set_trace()
                for i in range(1, pk * 3):

                    # BOOK CREATION
                    book_obj = Book.objects.create(name=f"Book_{i}", description=f"{'description' * i}_{i}",
                                                   author=f"author_{i}", published_year=random_number(1990, 2021),
                                                   publisher=f"publisher_{i}", chapter_count=random_number(10, 30),
                                                   pages_count=random_number(150, 400),
                                                   visit_count=random_number(10, 100),
                                                   manual_popularity=random_number(10, 30), created_user_id=random_choice(user_list))

                    # SHUFFLING GENRE LIST AND ACCESSING SOME OF THEM
                    list_1 = list(set(genre_list))
                    # CREATING BOOK AND GENRE MAPPING
                    for j in range(1, random_number(4, len(genre_list))):
                        genre_obj = Genre.objects.get(id=list_1[j])
                        BookGenre.objects.create(genre=genre_obj, book=book_obj, created_user_id=random_choice(user_list))
                    # BOOKMEDIA -----------------> PENDING
                    for k in range(1, random_number(5,10)):
                        is_primary = True if k == 1 else False
                        pil_image(file_name=file_name, msg_text=f"user_{k}")

                        BookMedia.objects.create(book=book_obj, media=File(file=open(file_name, 'rb')), is_primary=is_primary, created_user_id=random_choice(user_list))
                print("--------------------- books created -----------------------------")
                print("--------------------- book genre created -----------------------------")
                print("--------------------- book media created -----------------------------")
                # import pdb; pdb.set_trace()

                # CREATING BOOK LIST
                book_list = Book.objects.filter(default_query_1).values_list("id", flat=True)
                # list_2 = list(set(user_list))[random_number(6, len(user_list))]
                #
                # # CREATING BOOK READ
                for i in range(random_number(20, 30)):
                    u_e_obj = UserAccount.objects.get(id=random_choice(user_list))
                    b_e_obj = Book.objects.get(id=random_choice(book_list))
                    BookRead.objects.create(user=u_e_obj, book=b_e_obj, created_user_id=random_choice(user_list))
                    # user_1 = random_choice(book_list)
                # print("--------------------- book read created -----------------------------")

                # CREATE READ ALONG --> PENDING
                for i in range(1, pk * 4):
                    receiver_user = random_choice(user_list)
                    if i == receiver_user:
                        receiver_user -= 1

                    r_u_obj = UserAccount.objects.get(id=random_choice(user_list))
                    i_u_obj = UserAccount.objects.get(id=random_choice(user_list))
                    b_e_obj = Book.objects.get(id=random_choice(book_list))

                    ReadAlong.objects.create(inviter=i_u_obj, receiver=r_u_obj, book=b_e_obj,
                                             receiver_status="accepted", accepted_timestamp=timezone.now(), created_user_id=random_choice(user_list))

                print("--------------------- book along created -----------------------------")

                # CREATING BOOKTALK
                for i in range(1, random_number(30, 80)):
                    pil_image(file_name=file_name, msg_text=f"book_talk_{i}")
                    b_e_obj = Book.objects.get(id=random_choice(book_list))
                    t_u_obj = UserAccount.objects.get(id=random_choice(user_list))

                    book_talk_obj = BookTalk.objects.create(name=f"name_{i}", description="description" * i,
                            book=b_e_obj, media=File(file=open("audio_1.mp3", 'rb')), image=File(file=open(file_name, 'rb')),
                            talk_by=t_u_obj, created_user_id=random_choice(user_list))

                    # BOOKTALK COMMENT CREATE
                    user_r1_list = list(set(user_list))
                    c = 0
                    for j in range(1, random_number(5,50)):
                        bc_u_obj = UserAccount.objects.get(id=random_choice(user_list))

                        BookTalkComment.objects.create(book_talk=book_talk_obj, user=bc_u_obj,
                                                       comment= f"comment_{random_number(1000, 10000)}", created_user_id=random_choice(user_list))
                #         c += 1
                print("--------------------- book talk created -----------------------------")
                print("--------------------- book comment created -----------------------------")

                # import pdb; pdb.set_trace()

                # BOOKCLUB CREATE
                for i in range(1, pk * 2):
                    bookclub_obj = BookClub.objects.create(name=f"BookClub_{i}",
                                                           short_description=f"random description {i}",
                                                           description=f"{'description' * random_number(10, 100)} i",
                                                           visit_count=random_number(10, 1000),
                                                           manual_popularity=random_number(10, 30), created_user_id=random_choice(user_list))
                    book_r1_list = list(set(book_list))
                    c = 0
                    for j in range(1, random_number(5, 10)):
                        bcb_e_obj = Book.objects.get(id=random_choice(book_list))

                        BookClubBook.objects.create(bookclub=bookclub_obj, book=bcb_e_obj, created_user_id=random_choice(user_list))

                    for k in range(1, random_number(5,12)):
                        pil_image(file_name=file_name, msg_text=f"book_club_{k}")
                        is_primary= True if k == 1 else False
                        BookClubMedia.objects.create(bookclub=bookclub_obj, media=File(file=open(file_name, 'rb')), is_primary=is_primary, created_user_id=random_choice(user_list))

                    for m in range(1, random_number(2,6)):
                        event_obj = Event.objects.create(bookclub= bookclub_obj, name=f"event_{m}",
                            short_description="short_description", description="description" * m,
                            from_timestamp=timezone.now()+datetime.timedelta(days=random_number(5,10)),
                            to_timestamp=timezone.now()+datetime.timedelta(days=random_number(11,25)),
                            link=f"www.test_{m}.com", fee=random_number(100, 1000), location="location", created_user_id=random_choice(user_list))

                        for n in range(1, random_number(3,10)):
                            pil_image(file_name=file_name, msg_text=f"event_{n}")
                            is_primary = True if n == 3 else False
                            EventMedia.objects.create(event=event_obj, media=File(file=open(file_name, 'rb')), is_primary=is_primary, created_user_id=random_choice(user_list))

                        # CREATE BOOK CLUB CONTRIBUTORS
                        c = 0
                        for x in range(1, pk * 2):
                            e_u_obj = UserAccount.objects.get(id=random_choice(user_list))
                            EventSubscribe.objects.create(event=event_obj, user=e_u_obj, created_user_id=random_choice(user_list))
                            c += 1

                # BOOK CLUB LIST
                # book_club_list = BookClub.objects.all().values_list("id", flat=True)

                    # CREATE BOOK CLUB FOLLOWER
                    for a1 in range(1, random_number(1,20)):

                        r_u_obj = UserAccount.objects.get(id=random_choice(user_list))
                        i_u_obj = UserAccount.objects.get(id=random_choice(user_list))

                        BookClubFollower.objects.create(inviter=i_u_obj, receiver=r_u_obj, bookclub=bookclub_obj,
                                                 receiver_status="accepted", accepted_timestamp=timezone.now(), created_user_id=random_choice(user_list))

                    # CREATE BOOK CLUB CONTRIBUTORS
                    for b1 in range(1, pk * 2):
                        r_u_obj = UserAccount.objects.get(id=random_choice(user_list))
                        i_u_obj = UserAccount.objects.get(id=random_choice(user_list))
                        BookClubKeyContributor.objects.create(inviter=i_u_obj, receiver=r_u_obj, bookclub=bookclub_obj,
                                                 receiver_status="accepted", accepted_timestamp=timezone.now(), created_user_id=random_choice(user_list))

                    # CREATE BOOK CLUB KEY USER
                    for c1 in range(1, random_number(2, 6)):
                        r_u_obj = UserAccount.objects.get(id=random_choice(user_list))
                        i_u_obj = UserAccount.objects.get(id=random_choice(user_list))
                        BookClubKeyUser.objects.create(inviter=i_u_obj, receiver=r_u_obj,
                                                              bookclub=bookclub_obj,
                                                              receiver_status="accepted",
                                                              accepted_timestamp=timezone.now(), created_user_id=random_choice(user_list))
                print("--------------------- book club created -----------------------------")
                print("--------------------- book club book created -----------------------------")
                print("--------------------- book club media created -----------------------------")
                print("--------------------- book club event created -----------------------------")
                print("--------------------- book club event media created -----------------------------")
                return Response({"is_success": True, "message": "Success", "data": 1}, status=status.HTTP_200_OK)
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


class AddTestData2(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, version):
        try:
            source_type = request.query_params["source_type"]
            if source_type not in source_list:
                raise CustomMessage("Source Type is invalid")
            if version == "v1":
                # CREATING USERS
                i = random_number(10000, 1000000)
                file_name = "image_1.jpeg"
                pil_image(file_name=file_name, msg_text=f"user_{i}")
                #
                user_obj = UserAccount.objects.create_user(mobile=i, first_name=f"name_{i}",
                            email=f"test_{i}@test.com", password=f"Test_{i}_Test")

                user_obj.media= File(file=open(file_name, 'rb'))
                user_obj.save()
                access_token = user_obj.generate_token(user_obj)["access"]

                return Response({"is_success": True, "message": "Success",
                        "data": UserAccountTest2V1Serializer(user_obj, many=False).data, "access_token": access_token},
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


class AddTestData3(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, version):
        try:
            source_type = request.query_params["source_type"]
            if source_type not in source_list:
                raise CustomMessage("Source Type is invalid")
            if version == "v1":
                user_list = UserAccount.objects.filter(default_query_1).values_list("id", flat=True)

                content_book_obj = ContentType.objects.get_for_model(Book)
                content_bookclub_obj = ContentType.objects.get_for_model(BookClub)
                content_booktalk_obj = ContentType.objects.get_for_model(BookTalk)
                content_bookevent_obj = ContentType.objects.get_for_model(Event)

                book_list = list(set(list(Book.objects.filter(default_query_1).values_list("id", flat=True))))
                bookclub_list = list(set(list(BookClub.objects.filter(default_query_1).values_list("id", flat=True))))
                booktalk_list = list(set(list(BookTalk.objects.filter(default_query_1).values_list("id", flat=True))))
                bookevent_list = list(set(list(Event.objects.filter(default_query_1).values_list("id", flat=True))))

                pil_image(file_name=file_name, msg_text=f"banner_book_1")
                Banner.objects.create(content_type=content_book_obj, content_id=random_choice(book_list), media=File(file=open(file_name, 'rb')),
                                      end_timestamp=timezone.now() + datetime.timedelta(days=random_number(4, 15)), created_user_id=random_choice(user_list))

                pil_image(file_name=file_name, msg_text=f"banner_bookclub_2")
                Banner.objects.create(content_type=content_bookclub_obj, content_id=random_choice(bookclub_list), media=File(file=open(file_name, 'rb')),
                                      end_timestamp=timezone.now() + datetime.timedelta(days=random_number(4, 15)), created_user_id=random_choice(user_list))

                pil_image(file_name=file_name, msg_text=f"banner_book_2")
                Banner.objects.create(content_type=content_book_obj, content_id=random_choice(book_list), media=File(file=open(file_name, 'rb')),
                                      end_timestamp=timezone.now() + datetime.timedelta(days=random_number(4, 15)), created_user_id=random_choice(user_list))

                pil_image(file_name=file_name, msg_text=f"banner_booktalk_4")
                Banner.objects.create(content_type=content_booktalk_obj, content_id=random_choice(booktalk_list), media=File(file=open(file_name, 'rb')),
                                      end_timestamp=timezone.now() + datetime.timedelta(days=random_number(4, 15)), created_user_id=random_choice(user_list))

                pil_image(file_name=file_name, msg_text=f"banner_book_5")
                Banner.objects.create(content_type=content_bookevent_obj, content_id=random_choice(book_list), media=File(file=open(file_name, 'rb')),
                                      end_timestamp=timezone.now() + datetime.timedelta(days=random_number(4, 15)), created_user_id=random_choice(user_list))

                pil_image(file_name=file_name, msg_text=f"banner_bookclub_6")
                Banner.objects.create(content_type=content_bookclub_obj, content_id=random_choice(bookclub_list), media=File(file=open(file_name, 'rb')),
                                      end_timestamp=timezone.now() + datetime.timedelta(days=random_number(4, 15)), created_user_id=random_choice(user_list))

                pil_image(file_name=file_name, msg_text=f"banner_event_1")
                Banner.objects.create(content_type=content_bookclub_obj, content_id=random_choice(bookevent_list), media=File(file=open(file_name, 'rb')),
                                      end_timestamp=timezone.now() + datetime.timedelta(days=random_number(4, 15)), created_user_id=random_choice(user_list))

                pil_image(file_name=file_name, msg_text=f"banner_event_2")
                Banner.objects.create(content_type=content_bookclub_obj, content_id=random_choice(bookevent_list), media=File(file=open(file_name, 'rb')),
                                      end_timestamp=timezone.now() + datetime.timedelta(days=random_number(4, 15)), created_user_id=random_choice(user_list))

                # print("------------------------------------", Banner._meta.many_to_many)

                return Response({"is_success": True, "message": "Success", "data": 'Success'}, status=status.HTTP_200_OK)
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
