from orders.models import Order_Detail
import pandas as pd


def convert_orders(farmerpk):
    order_details = Order_Detail.objects.filter(
        product__farmer__pk=farmerpk, status="preparing"
    )  # '배송준비중' 싱태만의 order detail들 가져오기

    # order_detail 가지고 엑셀 만드는 부분 작업하면 될듯
    order_data = []

    for detail in order_details:
        order_num = detail.order_management_number
        orderer = detail.order_group.consumer.user.nickname
        receiver = detail.order_group.rev_name
        phone_num = detail.order_group.rev_phone_number
        address = detail.order_group.rev_address
        product_name = detail.product.title
        quantity = detail.quantity
        message = detail.order_group.rev_message

        order_data.append(
            [
                order_num,
                orderer,
                receiver,
                phone_num,
                address,
                product_name,
                quantity,
                message,
            ]
        )

    df = pd.DataFrame(
        data=order_data,
        columns=["주문번호", "주문자명", "수취인명", "전화번호", "주소", "상품명", "수량", "배송메세지"],
    )

    path = ""

    df.to_excel(path, "주문정보", index=False)
