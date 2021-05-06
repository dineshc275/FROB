import logging

from django.db.models import Q
from django.utils.datastructures import MultiValueDictKeyError
from rest_framework import status
from rest_framework.exceptions import ParseError, ValidationError
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken

from FROB.project_utils import CustomMessage, mobile_validation
from account.account_utils import send_mobile_otp, mobile_otp_verify
from account.models import UserAccount
from account.serializers import UserAccountSerializer

logger = logging.getLogger(__name__)
otp_modes = ["register", "login", "forgot_password"]


class GenerateOtp(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        try:
            mobile = int(request.data['mobile'])
            otp_type = request.data['otp_type']

            if otp_type not in otp_modes:
                raise CustomMessage("OTP type is invalid")

            if not mobile_validation(mobile):
                raise CustomMessage("Enter valid Mobile number")
            try:
                UserAccount.objects.get(mobile=mobile)
                if otp_type == "register":
                    raise CustomMessage("Mobile Number is already Registered")
                send_mobile_otp(mobile, mode=otp_type)
            except UserAccount.DoesNotExist:
                if otp_type == 'forgot_password' or otp_type == "login":
                    raise CustomMessage("Mobile Number is not Registered")
                else:
                    send_mobile_otp(mobile, mode=otp_type)
            return Response({"is_success": True, "data": {"user_input": mobile, "user_message": "OTP Sent to your Mobile"}},
                            status=status.HTTP_200_OK)
        except CustomMessage as e:
            return Response({"is_success": False, "data": {"user_input": mobile, "user_message": e.message}},
                            status=status.HTTP_200_OK)
        except (ParseError, ZeroDivisionError, MultiValueDictKeyError, KeyError, ValueError, ValidationError):
            logger.debug(f"class name: {self.__class__.__name__},request: {request.data}")
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"class name: {self.__class__.__name__},request: {request.data}, message: str({e})")
            return Response(
                {"status": status.HTTP_500_INTERNAL_SERVER_ERROR, "message": "fail", "raw_message": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class VerifyOtp(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        try:
            mobile = int(request.data['mobile'])
            otp = request.data['otp']
            otp_type = request.data['otp_type']

            if otp_type not in otp_modes:
                raise CustomMessage("OTP type is invalid")
            try:
                user_obj = UserAccount.objects.get(mobile=mobile)
                otp_verification = mobile_otp_verify(mobile=mobile, otp=otp, mode=otp_type)
                if not otp_verification['status']:
                    raise CustomMessage(otp_verification['message'])
            except UserAccount.DoesNotExist:
                otp_verification = mobile_otp_verify(mobile=mobile, otp=otp, mode=otp_type)
                if otp_verification['status']:
                    UserAccount.objects.create_mobile_user(mobile=mobile)
                    user_obj = UserAccount.objects.get(mobile=mobile)
                else:
                    raise CustomMessage(otp_verification['message'])

                if user_obj.first_name:
                    user_input = user_obj.first_name
                else:
                    user_input = mobile
            if otp_type != "forgot_password":

                token = user_obj.generate_token(user_obj)

                return Response({"data": {"is_otp_verified": True, "user_input": user_input, "message": "Success",
                                          "token": token, "user_detail": UserAccountSerializer(request.user, many=False).data}},
                                status=status.HTTP_200_OK)
            else:
                password1 = request.data['password1']
                password2 = request.data['password2']
                if password1 != password2:
                    raise CustomMessage("Both Passwords didn't match")
                user_obj.set_password(password1)
                user_obj.save()
                return Response({"is_success": True, "data": {"is_otp_verified": True, "user_input": mobile,
                                          "message": "Password Updated Successfully",}}, status=status.HTTP_200_OK)
        except CustomMessage as e:
            return Response({"data": {"is_success": False, "user_input": mobile, "message": e.message}},
                            status=status.HTTP_200_OK)
        except (ParseError, ZeroDivisionError, MultiValueDictKeyError, KeyError, ValueError, ValidationError):
            logger.debug(f"class name: {self.__class__.__name__},request: {request.data}")
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"class name: {self.__class__.__name__},request: {request.data}, message: str({e})")
            return Response(
                {"status": status.HTTP_500_INTERNAL_SERVER_ERROR, "message": "fail", "raw_message": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class Login(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        try:
            user_input = request.data['user_input']
            password = request.data['password']
            from django.contrib.auth import authenticate
            user_obj = UserAccount.objects.get(Q(mobile=user_input) | Q(email=user_input))
            user = authenticate(username=user_obj.id, password=password)
            if user is not None:
                token = user_obj.generate_token(user_obj)
                return Response({"is_success": True, "data": {"user_input": user_input, "message": "Success",
                                "token": token, "user_detail": UserAccountSerializer(user_obj, many=False).data}},
                                status=status.HTTP_200_OK)
            else:
                raise CustomMessage("Credentials Didn't Match")
        except CustomMessage as e:
            return Response({"is_success": False, "data": {"user_input": user_input, "message": e.message}},
                            status=status.HTTP_200_OK)
        except (ParseError, ZeroDivisionError, MultiValueDictKeyError, KeyError, ValueError, ValidationError):
            logger.debug(f"class name: {self.__class__.__name__},request: {request.data}")
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"class name: {self.__class__.__name__},request: {request.data}, message: str({e})")
            return Response(
                {"status": status.HTTP_500_INTERNAL_SERVER_ERROR, "message": "fail", "raw_message": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UpdateDetail(APIView):
    permission_classes = (IsAuthenticated, )

    def post(self, request):
        try:
            first_name = request.data.get('first_name')
            last_name = request.data.get('last_name')
            email = request.data.get('email')
            password = request.data.get('password')
            if first_name:
                request.user.first_name = first_name
            if last_name:
                request.user.last_name = last_name
            if email:
                request.user.email = email
            if password:
                request.user.set_password(password)
            request.user.save()
            return Response({"is_success": True, "data": {"user_input": request.user.mobile,
                                      "message": "Successfully Updated", "user_detail": UserAccountSerializer(request.user, many=False).data}}, status=status.HTTP_200_OK)
        except CustomMessage as e:
            return Response({"is_success": False, "data": {"user_input": request.user.mobile, "message": e.message}},
                            status=status.HTTP_200_OK)
        except (ParseError, ZeroDivisionError, MultiValueDictKeyError, KeyError, ValueError, ValidationError):
            logger.debug(f"class name: {self.__class__.__name__},request: {request.data}")
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"class name: {self.__class__.__name__},request: {request.data}, message: str({e})")
            return Response(
                {"status": status.HTTP_500_INTERNAL_SERVER_ERROR, "message": "fail", "raw_message": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request):
        try:
            return Response({"is_success": True, "data": {"user_detail": UserAccountSerializer(request.user, many=False).data}},
                            status=status.HTTP_200_OK)
        except CustomMessage as e:
            return Response({"is_success": False, "data": {"user_input": request.user.mobile, "message": e.message}},
                            status=status.HTTP_200_OK)
        except (ParseError, ZeroDivisionError, MultiValueDictKeyError, KeyError, ValueError, ValidationError):
            logger.debug(f"class name: {self.__class__.__name__},request: {request.data}")
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"class name: {self.__class__.__name__},request: {request.data}, message: str({e})")
            return Response(
                {"status": status.HTTP_500_INTERNAL_SERVER_ERROR, "message": "fail", "raw_message": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)