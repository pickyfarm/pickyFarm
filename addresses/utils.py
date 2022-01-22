from .zipcode import ZIPCODE_LIST
from bisect import bisect_left


def check_address_by_zipcode(zipcode):
    idx = bisect_left(ZIPCODE_LIST, zipcode)

    return True if (ZIPCODE_LIST[idx] == zipcode) else False


def calculate_jeju_delivery_fee(farm_zipcode, consumer_zipcode, product):
    additional_fee = 0
    default_fee = product.default_delivery_fee
    is_jeju_mountain = check_address_by_zipcode(consumer_zipcode)

    # 제주 농가
    if 63000 <= farm_zipcode <= 699949:
        # -> 도서산간
        if is_jeju_mountain and consumer_zipcode < 63000:
            additional_fee += product.jeju_mountain_additional_delivery_fee
        # -> 그 외
        else:
            additional_fee = 0
    # 그 외
    else:
        # -> 제주 소비자
        if is_jeju_mountain and (63000 <= consumer_zipcode <= 699949):
            additional_fee += product.jeju_mountain_additional_delivery_fee
        # -> 그 외
        else:
            additional_fee = 0
    print("default_fee", default_fee)
    total_delivery_fee = default_fee + additional_fee
    print("total_delivery_fee", total_delivery_fee)
    return total_delivery_fee
