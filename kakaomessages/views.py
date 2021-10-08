from django.shortcuts import render
import json
import sys
import re

from .message import *
from django.http import HttpResponse


def send_kakao_message(
    phonenum,
    templateId="",
    args={},
):
    phonenum = re.sub(r"[^0-9]", "", phonenum)
    data = {
        "messages": [
            # 변수가 있는 경우
            {
                "to": phonenum,
                # array 사용으로 동일한 내용을 여러 수신번호에 전송 가능
                # "to": ["01000000002", "01000000003"],
                "from": "01033688026",
                "kakaoOptions": {
                    "pfId": "KA01PF210731082631285ecaWbc5i60e",
                    "templateId": templateId,
                    # 변수: 값 형식으로 모든 변수에 대한 변수값 입력
                    # "variables": {},  # 변수가 없는 경우에도 입력
                    "variables": args,
                },
            },
        ]
    }

    sendMany(data)


def send_sms(phonenum, authnum):
    phonenum = re.sub(r"[^0-9]", "", phonenum)
    data = {
        "message": {
            "to": phonenum,
            "from": "01033688026",
            "text": f"인증번호 {authnum}\n까다롭게 선택하다: 피키팜 Picky Farm",
        }
    }
    sendOne(data)


data = {
    "messages": [
        # 변수가 있는 경우
        {
            "to": "01026080265",
            # array 사용으로 동일한 내용을 여러 수신번호에 전송 가능
            # "to": ["01000000002", "01000000003"],
            "from": "01033688026",
            "kakaoOptions": {
                "pfId": "KA01PF210731082631285ecaWbc5i60e",
                "templateId": "KA01TP2107310829300073JUsV4IeXxB",
                # 변수: 값 형식으로 모든 변수에 대한 변수값 입력
                # "variables": {},  # 변수가 없는 경우에도 입력
                "variables": {
                    # "#{변수1}": "변수1의 값",
                    # "#{변수2}": "변수2의 값",
                    # "#{버튼링크1}": "버튼링크1의 값",
                    # "#{버튼링크2}": "버튼링크2의 값",
                    # "#{강조문구}": "강조문구의 값",
                },
            },
        },
    ]
}

# 발송 테스트
def message_test(request):
    print(data)
    res = sendMany(data)
    print(res)
    print(json.dumps(res.json(), indent=2, ensure_ascii=False))
    return HttpResponse("문자 발송 테스트", status=400)
