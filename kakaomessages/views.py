from django.shortcuts import render
import json
import sys

from .message import *
from django.http import HttpResponse


data = {
    "messages": [
        # 변수가 있는 경우
        {
            "to": "01026080265",
            "from": "029302266",
            "kakaoOptions": {
                "pfId": "KA01PF200323182344986oTFz9CIabcx",
                "templateId": "KA01TP200323182345741y9yF20aabcx",
                # 변수: 값 형식으로 모든 변수에 대한 변수값 입력
                "variables": {
                    "#{변수1}": "변수1의 값",
                    "#{변수2}": "변수2의 값",
                    "#{버튼링크1}": "버튼링크1의 값",
                    "#{버튼링크2}": "버튼링크2의 값",
                    "#{강조문구}": "강조문구의 값",
                },
            },
        },
        # # 변수가 없는 경우
        # {
        #     "to": "01026080265",
        #     "from": "029302266",
        #     "kakaoOptions": {
        #         "pfId": "KA01PF200323182344986oTFz9CIabcx",
        #         "templateId": "KA01TP200323182345741y9yF20aabcx",
        #         "variables": {},  # 변수가 없는 경우에도 입력
        #     },
        # },
        # {
        #     "to": ["01000000002", "01000000003"],  # array 사용으로 동일한 내용을 여러 수신번호에 전송 가능
        #     "from": "029302266",
        #     "kakaoOptions": {
        #         "pfId": "KA01PF200323182344986oTFz9CIabcx",
        #         "templateId": "KA01TP200323182345741y9yF20aabcx",
        #         "variables": {
        #             "#{변수1}": "변수1의 값",
        #             "#{변수2}": "변수2의 값",
        #             "#{버튼링크1}": "버튼링크1의 값",
        #             "#{버튼링크2}": "버튼링크2의 값",
        #             "#{강조문구}": "강조문구의 값",
        #         },
        #     },
        # }
        # # ...
        # # 1만건까지 추가 가능
    ]
}


def message_test(request):
    print(data)
    res = sendMany(data)
    print(res)
    print(json.dumps(res.json(), indent=2, ensure_ascii=False))
    return HttpResponse("알림톡 발송 테스트", status=400)
