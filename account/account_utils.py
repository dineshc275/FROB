import datetime
import json
import random
from django.db.models import Q
import http.client

from django.utils import timezone

from FROB.constant_values import otp_attempts
from account.models import Otp


def jwt_get_secret_key(user):
    return user.secret_key


def msg91_otp_service(mobile, otp, mode):
    dict_of_keys = {
        # "login": constant_values.MSG91_TEMPLATE_ID,
        # "forgot_password": constant_values.MSG91_TEMPLATE_ID,
        # "register": constant_values.MSG91_TEMPLATE_ID,
    }

    template_id = dict_of_keys[mode]
    conn = http.client.HTTPSConnection("api.msg91.com")
    payload = ""
    headers = {'content-type': "application/json"}
    msg91link = f"https://api.msg91.com/api/v5/otp?otp={otp}&template_id={template_id}&mobile={mobile}&authkey={constant_values.AUTHKEY1}"
    conn.request("POST", msg91link, payload, headers)
    res = conn.getresponse()
    data = res.read()
    response = json.loads(data.decode('utf-8'))
    return response


def send_mobile_otp(mobile, mode):
    try:
        otp_obj1 = Otp.objects.filter(Q(input=mobile) & Q(otp_type=mode)
                                      & Q(expiry_timestamp__gte=timezone.now())).latest('created_timestamp')
        if otp_obj1.attempts >= otp_attempts:
            # otp = random.randint(100001, 999999)
            otp = "123123"
            otp_obj1 = Otp.objects.create(input=mobile, otp=otp, otp_type=mode)
    except Otp.DoesNotExist:
        # otp = random.randint(100001, 999999)
        otp = "123123"
        otp_obj1 = Otp.objects.create(input=mobile, otp=otp, otp_type=mode)
    otp = otp_obj1.otp
    # msg91_response = msg91_otp_service(mobile, otp, mode=mode)


def mobile_otp_verify(mobile, otp, mode):
    try:
        otp_obj1 = Otp.objects.filter(Q(input=mobile) & Q(otp_type=mode)
                                      & Q(expiry_timestamp__gte=timezone.now())).latest('created_timestamp')
        if otp_obj1.attempts == otp_attempts:
            return {"status": False, "message": "You tried many times, Generate a new OTP"}
    except Otp.DoesNotExist:
        otp_obj2 = Otp.objects.filter(Q(input=mobile) & Q(otp_type=mode))
        if otp_obj2:
            return {"status": False, "message": "OTP is Expired, Click on Resend"}
        return {"status": False, "message": "OTP is not generated"}
    if otp_obj1.otp == int(otp):
        Otp.objects.filter(Q(input=mobile) & Q(otp_type=mode)).delete()
        return {"status": True, "message": "OTP Verified"}
    else:
        otp_obj1.attempts += 1
        otp_obj1.save()
        return {"status": False, "message": "OTP didn't match"}