from turtle import title
from django.db import models
from core.models import CompressedImageField
from core import url_encryption
from django.utils import timezone
from kakaomessages.views import send_kakao_message
from kakaomessages.template import templateIdList
import os
from datetime import datetime
from .BootpayApi import BootpayApi

# Create your models here.


class Order_Group(models.Model):

    STATUS = (
        ("wait", "결제대기"),
        ("wait_vbank", "결제대기(가상계좌)"),
        ("payment_complete", "결제완료"),
        ("cancel", "결제취소"),
        ("error_stock", "결제오류(재고부족)"),
        ("error_valid", "결제오류(검증)"),
        ("error_server", "결제오류(서버)"),
        ("error_price_match", "결제오류(총가격 불일치)"),
    )

    CONSUMER_TYPE = (("user", "회원"), ("non_user", "비회원"))
    ORDER_TYPE = (("normal", "일반결제"), ("gift", "선물하기"))

    # 선물하기 여부 구분 필드
    order_type = models.CharField(
        max_length=6, choices=ORDER_TYPE, default="normal", help_text="결제 유형"
    )

    status = models.CharField(max_length=20, choices=STATUS, default="wait", help_text="상태")

    order_management_number = models.CharField(
        max_length=1000, null=True, blank=True, help_text="주문관리번호"
    )
    receipt_number = models.CharField(max_length=60, null=True, blank=True)

    rev_address = models.TextField(null=True, blank=True)
    rev_name = models.CharField(max_length=50, null=True, blank=True, help_text="받는이 이름")
    rev_phone_number = models.CharField(max_length=30, null=True, blank=True, help_text="받는이 전화번호")

    rev_loc_at = models.CharField(max_length=20, null=True, blank=True, help_text="받으실 장소")
    rev_loc_detail = models.TextField(null=True, blank=True)
    rev_message = models.TextField(null=True, blank=True, help_text="배송지 특이사항")

    to_farm_message = models.TextField(null=True, blank=True, help_text="농가 전달 메시지")

    payment_type = models.CharField(max_length=20, null=True, blank=True)
    v_bank = models.CharField(max_length=200, null=True, blank=True, help_text="가상계좌 은행명")
    v_bank_account = models.CharField(max_length=500, null=True, blank=True, help_text="가상계좌 번호")
    v_bank_account_holder = models.CharField(
        max_length=500, null=True, blank=True, help_text="가삼계좌 예금주"
    )
    v_bank_expire_date = models.DateTimeField(null=True, blank=True, help_text="가상계좌 입금 마감기한")

    # 22.1.9 기윤 - 비회원 구매 도입을 위한 필드 추가
    consumer_type = models.CharField(
        max_length=20, choices=CONSUMER_TYPE, default="user", help_text="구매 회원 타입"
    )
    orderer_name = models.CharField(max_length=20, help_text="주문자 이름", null=True, blank=True)
    orderer_phone_number = models.CharField(
        max_length=30, help_text="주문자 전화번호", null=True, blank=True
    )

    total_price = models.IntegerField(null=True, blank=True)
    total_quantity = models.IntegerField(null=True, blank=True)

    is_jeju_mountain = models.BooleanField(default=False)

    order_at = models.DateTimeField(null=True, blank=True)

    update_at = models.DateTimeField(auto_now=True)
    create_at = models.DateTimeField(auto_now_add=True)

    consumer = models.ForeignKey(
        "users.Consumer",
        related_name="order_groups",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    # 22.1.9 기윤 비회원 구매 도입을 위한 null=True / blank=True 추가

    def __str__(self):
        if self.order_at is None:
            order_at = ""
        else:
            datatime_format = "%Y-%m-%dT%H:%M:%S.%fZ"
            order_at = str(timezone.localtime(self.order_at))
            order_at += " 주문"
        title = f"수취인 : {self.rev_name} / 결제자 : {self.orderer_name} / {order_at}"
        return title

    def encrypt_odmn(self):
        return url_encryption.encode_string_to_url(self.order_management_number)

    def update(self, fields):
        for (key, value) in fields.items():
            setattr(self, key, value)

        self.save()

    def set_order_state(self, status):
        """order 모델 상태 일괄 변경 메서드"""
        """ order_group 상태를 바꾸면서 참조하는 모든 order_detail의 상태도 변경한다 """

        # [Process 1] order_group에 연결되는 모든 order_detail 불러온다.
        details = self.order_details.all()

        # [Process 2] order_detail들을 입력받는 상태로 변경한다.
        for detail in details:
            detail.status = status
            detail.save()

        # [Process 2-1] order_group 또한 상태 변경한다.
        self.status = status
        self.save()

    def create_order_group_management_number(self):

        """order_group 주문 관리 번호 생성"""
        now = timezone.localtime()
        year = now.year % 100

        month = now.month

        if month < 10:
            month = "0" + str(month)
        else:
            month = str(month)

        day = now.day

        if day < 10:
            day = "0" + str(day)
        else:
            day = str(day)

        self.order_management_number = str(year) + month + day + "_PF" + str(self.pk)

    def set_init_order_group_info(self, order_type, consumer_type, user):
        """결제하기 초기 생성 order_group 세팅"""
        """order group 생성 및 save() 후에 결제 타입, 결제자정보, 주문관리번호 생성 """
        """order_type = ["normal", "gift"] / consummer_type = ["user", "non_user"] """
        self.order_type = order_type
        self.consumer_type = consumer_type
        self.orderer_name = user.account_name
        self.orderer_phone_number = user.phone_number

        # order_pk 기반 주문관리번호 생성 - db에 pk생성 후 (save())후 메소드 호출해야함
        self.order_management_number = self.create_order_group_management_number()


class Order_Detail(models.Model):

    STATUS = (
        ("wait", "결제대기"),
        ("payment_complete_no_address", "결제완료(주소미입력)"),
        ("payment_complete", "결제완료"),
        ("preparing", "배송 준비 중"),
        ("shipping", "배송 중"),
        ("delivery_complete", "배송완료"),
        ("cancel", "주문취소"),
        ("re_recept", "환불 접수"),
        ("ex_recept", "교환 접수"),
        ("re_ex_approve", "환불/교환 승인"),
        ("re_ex_deny", "환불/교환 거절"),
        ("error_stock", "결제오류(재고부족)"),
        ("error_valid", "결제오류(검증)"),
        ("error_server", "결제오류(서버)"),
        ("error_price_match", "결제오류(총가격 불일치)"),
    )

    PAYMENT_STATUS = (
        ("none", "결제 이전"),
        ("incoming", "정산예정"),
        ("progress", "정산 진행"),
        ("done", "정산 완료"),
    )

    COMPANY = (
        ("CJ", "CJ대한통운"),
        ("POST", "우체국택배"),
        ("LOGEN", "로젠택배"),
        ("KG", "KG로지스"),
        ("ILYANG", "일양로지스"),
        ("HYUNDAI", "현대택배"),
        ("GTX", "GTX로지스"),
        ("FedEx", "FedEx"),
        ("HANJIN", "한진택배"),
        ("KYUNG", "경동택배"),
        ("LOTTE", "롯데택배"),
        ("HAPDONG", "합동택배"),
    )

    status = models.CharField(max_length=27, choices=STATUS, default="wait", help_text="주문 상태")
    payment_status = models.CharField(
        max_length=10, choices=PAYMENT_STATUS, default="none", help_text="정산 상태"
    )
    order_management_number = models.CharField(
        max_length=1000, null=True, blank=True, help_text="주문관리번호"
    )

    delivery_service_company = models.CharField(
        max_length=100, choices=COMPANY, null=True, blank=True, help_text="택배회사"
    )
    invoice_number = models.CharField(max_length=30, null=True, blank=True, help_text="운송장 번호")

    quantity = models.IntegerField(help_text="수량")

    total_price = models.IntegerField(help_text="총금액")
    commision_rate = models.FloatField(help_text="수수료율", default=18.0)

    cancel_reason = models.CharField(max_length=30, null=True, blank=True, help_text="주문 취소 사유")

    update_at = models.DateTimeField(auto_now=True)
    create_at = models.DateTimeField(auto_now_add=True)

    # 선물하기 -> 선물 받는사람 정보 필드
    rev_name_gift = models.CharField(max_length=50, null=True, blank=True, help_text="선물 받는사람 이름")
    rev_address_gift = models.TextField(null=True, blank=True, help_text="선물 받는사람 주소")
    rev_phone_number_gift = models.CharField(
        max_length=30, null=True, blank=True, help_text="선물 받는사람 전화번호"
    )
    gift_message = models.TextField(
        max_length=600, null=True, blank=True, help_text="선물 받는 사람에게 전달할 메세지"
    )

    product = models.ForeignKey(
        "products.Product",
        related_name="order_details",
        on_delete=models.CASCADE,
        help_text="구매 상품",
    )
    order_group = models.ForeignKey(
        Order_Group,
        related_name="order_details",
        on_delete=models.SET_NULL,
        null=True,
        help_text="주문 정보 그룹",
    )

    def __str__(self):
        name = []
        name.append(str(self.product.title))
        name.append(str(self.quantity))
        name.append(str(self.status))
        return "-".join(name)

    def encrypt_odmn(self):
        return url_encryption.encode_string_to_url(self.order_management_number)

    def save(self, *args, **kwargs):
        if self.status == "cancel":
            self.payment_status = "none"

        super(Order_Detail, self).save(*args, **kwargs)

    def create_order_detail_management_number(self, farmer_id):

        """order_detail 주문 관리 정보 생성"""

        now = timezone.localtime()
        year = now.year % 100

        month = now.month
        if month < 10:
            month = "0" + str(month)
        else:
            month = str(month)

        day = now.day

        if day < 10:
            day = "0" + str(day)
        else:
            day = str(day)

        self.order_management_number = (
            str(year) + month + day + "_" + str(self.pk) + "_" + farmer_id
        )

    def is_sufficient_stock(self):
        return self.product.is_sufficient_stock(self.quantity)

    def order_cancel(self, cancel_reason, gift):

        """주문 취소 및 금액 환불 진행"""
        """일반 결제 / 선물 하기 여부 구분"""

        self.cancel_reason = cancel_reason

        REST_API_KEY = os.environ.get("BOOTPAY_REST_KEY")
        PRIVATE_KEY = os.environ.get("BOOTPAY_PRIVATE_KEY")

        bootpay = BootpayApi(application_id=REST_API_KEY, private_key=PRIVATE_KEY)
        result = bootpay.get_access_token()

        if result["status"] == 200:
            cancel_result = bootpay.cancel(
                self.order_group.receipt_number,
                self.total_price,
                self.order_group.rev_name,
                cancel_reason,
            )

            if cancel_result["status"] == 200:
                self.status = "cancel"
                self.order_group.status = "cancel"
                product = self.product
                product.stock += self.quantity
                product.save()
                self.save()

                # 선물하기인 경우
                # 결제자에게 주문 취소 알림톡 전송
                if gift is True:
                    args_kakao = {
                        "#{account_name}": self.order_group.orderer_name,
                        "#{rev_name_gift}": self.rev_name_gift,
                        "#{product_title}": self.product.title,
                        "#{cancel_reason}": cancel_reason,
                    }

                    send_kakao_message(
                        self.product.order_group.orderer_phone_number,
                        templateIdList["gift_auto_cancel"],
                        args_kakao,
                    )

                # 선물하기 아닌 일반 결제인 경우
                # 농가에게 주문 취소 알림톡 전송
                else:

                    args_kakao = {
                        "#{cancel_reason}": self.cancel_reason,
                        "#{order_detail_title}": self.product.title,
                        "#{order_detail_number}": self.order_management_number,
                        "#{option_name}": self.product.option_name,
                        "#{quantity}": self.quantity,
                        "#{rev_name}": self.order_group.orderer_name,
                        "#{rev_phone_number}": self.order_group.rev_phone_number,
                    }

                    send_kakao_message(
                        self.product.farmer.user.phone_number,
                        templateIdList["order_cancel_by_user"],
                        args_kakao,
                    )
            else:
                raise Exception(
                    f"주문 취소 bootpay cancel result Http Response Error / 주문관리번호 : {self.order_management_number}"
                )
        else:
            raise Exception(
                f"주문 취소 bootpay get access token Http Response Error / 주문관리번호 : {self.order_management_number}"
            )

    def send_kakao_msg_payment_complete_for_consumer(self, phone_number_consumer, is_user, is_gift):
        """소비자에게 결제 완료 메시지 전송"""
        """회원/비회원 - 일반결제/선물하기 구분"""

        kakao_msg_quantity = (str)(self.quantity) + "개"

        farmer = self.product.farmer

        args_consumer = {
            "#{farm_name}": farmer.farm_name,
            "#{order_detail_number}": self.order_management_number,
            "#{order_detail_title}": self.product.title,
            "#{farmer_nickname}": farmer.user.nickname,
            "#{option_name}": self.product.option_name,
            "#{quantity}": kakao_msg_quantity,
            "#{link_1}": f"www.pickyfarm.com/farmer/farmer_detail/{farmer.pk}",
        }

        # 회원인 경우
        if is_user == True:
            args_consumer[
                "#{link_2}"
            ] = "https://www.pickyfarm.com/user/mypage/orders"  # 회원용 구매확인 링크
        # 비회원인 경우
        else:
            url_encoded_order_group_number = url_encryption.encode_string_to_url(
                self.order_group.order_management_number
            )
            args_consumer[
                "#{link_2}"
            ] = f"https://www.pickyfarm.com/user/mypage/orders/list?odmn={url_encoded_order_group_number}"  # 비회원용 구매확인 링크

        # 선물하기 결제인 경우
        if is_gift == True:
            # 주소 입력된 선물하기 주문인 경우
            if self.status == "payment_complete":
                send_kakao_message(
                    phone_number_consumer,
                    templateIdList["payment_complete_gift_address"],
                    args_consumer,
                )
                print(f"[KAKAO] 선물하기 결제완료 : 주소 입력된 선물하기 주문인 경우 / parameter : {args_consumer}")
            # 주소 미입력된 선물하기 주문인 경우
            elif self.status == "payment_complete_no_address":
                send_kakao_message(
                    phone_number_consumer,
                    templateIdList["payment_complete_gift_no_address"],
                    args_consumer,
                )
                print(f"[KAKAO] 선물하기 결제완료 : 주소 미입력된 선물하기 주문인 경우 / parameter : {args_consumer}")

        else:
            send_kakao_message(
                phone_number_consumer,
                templateIdList["payment_complete"],
                args_consumer,
            )

    def send_kakao_msg_order_for_farmer(self):
        """농가에게 주문 접수 알림톡 전송"""
        url_encoded_order_detail_number = url_encryption.encode_string_to_url(
            self.order_management_number
        )

        kakao_msg_quantity = (str)(self.quantity) + "개"

        args_farmer = {
            "#{order_detail_title}": self.product.title,
            "#{order_detail_number}": self.order_management_number,
            "#{option_name}": self.product.option_name,
            "#{quantity}": kakao_msg_quantity,
            "#{rev_name}": self.order_group.orderer_name,
            "#{rev_phone_number}": self.order_group.orderer_phone_number,
            "#{rev_address}": self.order_group.rev_address,
            "#{rev_loc_at}": self.order_group.rev_loc_at,
            "#{rev_detail}": self.order_group.rev_message,
            "#{rev_message}": self.order_group.to_farm_message,
            "#{link_1}": f"www.pickyfarm.com/farmer/mypage/orders/check?odmn={url_encoded_order_detail_number}",
            "#{link_2}": f"www.pickyfarm.com/farmer/mypage/orders/cancel?odmn={url_encoded_order_detail_number}",
            "#{link_3}": f"www.pickyfarm.com/farmer/mypage/orders/invoice?odmn={url_encoded_order_detail_number}",
        }

        send_kakao_message(
            self.product.farmer.user.phone_number,
            templateIdList["order_recept"],
            args_farmer,
        )

    def send_kakao_msg_gift_for_receiver(self):
        """선물하기 수령인 선물 알림톡 전송"""
        """주소 입력 / 미입력 구분"""

        farmer = self.product.farmer

        args_receiver = {
            "#{account_name}": self.order_group.orderer_name,
            "#{rev_name_gift}": self.rev_name_gift,
            "#{gift_message}": self.gift_message,
            "#{product_title}": self.product.title,
            "#{farm_name}": farmer.farm_name,
        }

        # 주소 입력된 선물하기 주문인 경우
        if self.status == "payment_complete":
            args_receiver["#{rev_address_gift}"] = self.rev_address_gift
            args_receiver[
                "#{link1}"
            ] = f"https://www.pickyfarm.com/order/payment/gift/popup/order?odmn={self.encrypt_odmn}"
            args_receiver[
                "#{link2}"
            ] = f"https://www.pickyfarm.com/farmer/farmer_detail/{farmer.pk}"
            # send_kakao_message(
            #     self.rev_phone_number_gift,
            #     templateIdList["gift_notice_address"],
            #     args_receiver,
            # )
            print(f"[KAKAO] 선물하기 선물 알림톡 : 주소 입력된 선물하기 주문인 경우 / parameter : {args_receiver}")
        # 주소 미입력된 선물하기 주문인 경우
        elif self.status == "payment_complete_no_address":
            args_receiver[
                "#{link}"
            ] = f"https://www.pickyfarm.com/order/payment/gift/popup/address?odmn={self.encrypt_odmn()}"
            # send_kakao_message(
            #     self.rev_phone_number_gift,
            #     templateIdList["gift_notice_no_address"],
            #     args_receiver,
            # )
            print(f"[KAKAO] 선물하기 선물 알림톡 : 주소 미입력된 선물하기 주문인 경우 / parameter : {args_receiver}")


class RefundExchange(models.Model):
    TYPE = (
        ("refund", "환불"),
        ("exchange", "교환"),
    )
    STATUS = (
        ("recept", "환불/교환 접수"),
        ("approve", "환불/교환 승인"),
        ("deny", "환불/교환 거절"),
    )
    claim_type = models.CharField(max_length=20, choices=TYPE)
    claim_status = models.CharField(max_length=20, choices=STATUS)

    order_detail = models.ForeignKey(
        "Order_Detail", on_delete=models.PROTECT, related_name="refund_exchanges"
    )
    reason = models.TextField()
    image = CompressedImageField(upload_to="RefundExchange/%Y/%m/%d/", null=True, blank=True)

    farmer_answer = models.TextField(null=True, blank=True)

    rev_address = models.TextField(null=True, blank=True)
    rev_loc_at = models.CharField(max_length=20, null=True, blank=True)
    rev_loc_detail = models.TextField(null=True, blank=True)
    rev_message = models.TextField(null=True, blank=True)

    refund_exchange_delivery_fee = models.IntegerField(null=True, blank=True)

    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
