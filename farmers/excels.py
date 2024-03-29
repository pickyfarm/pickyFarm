from orders.models import Order_Detail
from .models import Farmer
from pathlib import Path
import pandas as pd


def convert_orders(farmerpk, phone_num_type):

    order_details = Order_Detail.objects.filter(
        product__farmer__pk=farmerpk, status="preparing"
    )  # '배송준비중' 싱태만의 order detail들 가져오기

    if len(order_details) == 0:
        raise Order_Detail.DoesNotExist
    farmer = Farmer.objects.get(pk=farmerpk)

    # order_detail 가지고 엑셀 만드는 부분 작업하면 될듯
    order_data = []

    for detail in order_details:
        order_num = detail.order_management_number
        orderer = detail.order_group.orderer_name
        receiver = detail.order_group.rev_name or detail.rev_name_gift
        phone_num = detail.order_group.rev_phone_number or detail.rev_phone_number_gift
        address = detail.order_group.rev_address or detail.rev_address_gift
        zipcode = detail.rev_address_zipcode
        product_name = detail.product.title
        quantity = detail.quantity
        message = detail.order_group.rev_message

        if phone_num_type == "hyphen":
            phone_num = f"{phone_num[:3]}-{phone_num[3:7]}-{phone_num[7:]}"

        order_data.append(
            [
                order_num,
                orderer,
                receiver,
                phone_num,
                address,
                zipcode,
                product_name,
                quantity,
                message,
            ]
        )

    df = pd.DataFrame(
        data=order_data,
        columns=["주문번호", "주문자명", "수취인명", "전화번호", "주소", "우편번호", "상품명", "수량", "배송메세지"],
    )

    filename = f"{farmer.farm_name}_주문목록.xlsx"

    df.to_excel(filename, "주문목록", index=False, encoding="utf-8")

    return filename
