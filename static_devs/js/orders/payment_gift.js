const initinalFriendList = [
    {
        id: 0,
        name: '친구1',
        phoneNum: '',
        address: {
            sigungu: '',
            detail: '',
            zipCode: '00000',
        },
        quantity: 1,
        deliveryFee: 0,
        giftMessage: '',
        infoScope: '',
    },
];

const purchaseApp = new Vue({
    delimiters: ['[[', ']]'],
    el: '#payment-app',
    data: {
        friendCount: 1,
        productPrice: 10000,
        friends: initinalFriendList,
        weight: 1.0,
        totalDeliveryFee: 0,
        paymentType: '',
    },

    computed: {
        numberOfFriend: function () {
            return this.friends.length;
        },
        sumOfQuantity: function () {
            // friend들의 quantity의 합계 구함
            return this.friends.reduce(
                (prev, next) => prev + (parseInt(next.quantity) || 1),
                0
            );
        },
        sumOfDeliveryFee: function () {
            return this.friends.reduce(
                (prev, next) => prev + parseInt(next.deliveryFee) || 0,
                0
            );
        },
        sumOfProductPrice: function () {
            return this.sumOfQuantity * this.productPrice;
        },
        orderTotalPrice: function () {
            return this.sumOfDeliveryFee + this.sumOfProductPrice;
        },
    },

    methods: {
        addFriend: function () {
            this.friends.push({
                id: this.friendCount++,
                name: `친구${this.friendCount}`,
                phoneNum: '',
                address: {
                    sigungu: '',
                    detail: '',
                    zipCode: '00000',
                },
                quantity: 1,
                deliveryFee: 0,
                giftMessage: '',
                infoScope: '',
            });
        },
        deleteFriend: function (id) {
            this.friends = this.friends.filter((el) => el.id !== id);
        },
        handleSubmitButtonClick: function (e) {
            this.friends = this.friends.filter((el) => el.infoScope);
            e.preventDefault();

            bootpayHandler(this);
        },
        handleAddressFindButtonClick: function (idx) {
            // callback 형태로 다음 우편번호 API의 결과값을 내부 변수에 할당할 수 있음
            executeDaumPostcodeAPI((data) => {
                this.friends[idx].address.sigungu = data.address;
                this.friends[idx].address.zipCode = data.zipCode;

                this.friends[idx].deliveryFee = getDeliveryFeeByZipCode(
                    FARMER_ZIPCODE,
                    this.friends[idx].address.zipCode,
                    0
                );
            });
        },
    },
});

function executeDaumPostcodeAPI(cb) {
    const addressInfo = {
        address: '',
        zipCode: '',
    };

    new daum.Postcode({
        oncomplete: function (data) {
            // 팝업에서 검색결과 항목을 클릭했을때 실행할 코드를 작성하는 부분.

            // 도로명 주소의 노출 규칙에 따라 주소를 표시한다.
            // 내려오는 변수가 값이 없는 경우엔 공백('')값을 가지므로, 이를 참고하여 분기 한다.
            var roadAddr = data.roadAddress; // 도로명 주소 변수
            var extraRoadAddr = ''; // 참고 항목 변수

            // 법정동명이 있을 경우 추가한다. (법정리는 제외)
            // 법정동의 경우 마지막 문자가 "동/로/가"로 끝난다.
            if (data.bname !== '' && /[동|로|가]$/g.test(data.bname)) {
                extraRoadAddr += data.bname;
            }
            // 건물명이 있고, 공동주택일 경우 추가한다.
            if (data.buildingName !== '' && data.apartment === 'Y') {
                extraRoadAddr +=
                    extraRoadAddr !== ''
                        ? ', ' + data.buildingName
                        : data.buildingName;
            }
            // 표시할 참고항목이 있을 경우, 괄호까지 추가한 최종 문자열을 만든다.
            if (extraRoadAddr !== '') {
                extraRoadAddr = ' (' + extraRoadAddr + ')';
            }

            // 우편번호와 주소 정보를 해당 필드에 넣는다.
            addressInfo.zipCode = data.zonecode;
            addressInfo.address = roadAddr;

            cb(addressInfo);
        },
    }).open();
}

function getDeliveryFeeByZipCode(
    farmerZipCode,
    consumerZipcode,
    productPK,
    quantity
) {
    /* 서버에 AJAX 보내서 계산된 배송비 업데이트 할 것 */
    let deliveryFee = 0;
    $.ajax({
        type: 'POST',
        url: CALCULATE_DELIVERY_FEE_URL,
        data: {
            farmerZipCode,
            consumerZipcode,
            productPK,
            quantity,
        },
        dataType: 'json',
        success: (res) => {
            deliveryFee = parseInt(res['delivery_fee']);
        },
    });

    return deliveryFee;
}

function bootpayHandler(instance) {
    /* 부트페이 요청 처리 함수 */

    const {
        friends,
        sumOfDeliveryFee,
        sumOfProductPrice,
        sumOfQuantity,
        paymentType,
    } = instance; // vue instance로 부터 받아온 결제 관련 정보

    const itemInfo = {
        item_name: ORDER_GROUP_NAME,
        qty: sumOfQuantity,
        unique: PRODUCT_PK,
        price: PRODUCT_PRICE,
        cat1: PRODUCT_CATEGORY,
    };

    const userInfo = {
        username: CONSUMER_NAME,
        email: CONSUMER_EMAIL,
        phone: CONSUMER_PHONE_NUM,
    };

    const purchaseData = {
        orderGroupPk: ORDER_GROUP_PK,
        totalProductPrice: sumOfProductPrice,
        totalDeliveryFee: sumOfDeliveryFee,
        totalQuantity: sumOfQuantity,
        friends,
    };

    /* 부트페이 요청 코드부 */
    Bootpay.request({
        price: instance.orderTotalPrice,
        application_id: '60dad0c05b29480021dc523d',
        name: ORDER_GROUP_NAME,
        pg: 'inicis',
        method: paymentType,
        show_agree_window: 0,
        items: [itemInfo],
        user_info: userInfo,
        order_id: ORDER_MANAGEMENT_NUMBER,
        extra: {
            escrow: false,
        },
    })
        .error(function (data) {
            //결제 진행시 에러가 발생하면 수행됩니다.
            window.location.href = '/order/payment/fail?errorType=error_server';
        })
        .cancel(function (data) {
            alert('결제가 취소되었습니다. 다시 결제하시기 바랍니다.');
        })
        .confirm(function (data) {
            $.ajax({
                type: 'POST',
                url: PAYMENT_UPDATE_URL,
                data: purchaseData,
                dataType: 'json',
                success: (res) => {
                    const valid = res.valid;

                    if (valid) {
                        Bootpay.transactionConfirm(data);
                    } else {
                        if (response.error_type == 'error_stock') {
                            response.invalid_products.forEach(function (item) {
                                data.params['errorMsg'] += item;
                            });

                            data.params['errorMsg'] += ' 재고가 부족합니다';
                        } else {
                            data.params['errorMsg'] +=
                                '클라이언트에서의 총 결제액이 서버와 일치하지 않습니다';
                        }

                        BootPay.removePaymentWindow(); // 조건이 맞지 않으면 결제 창을 닫고 결제를 승인하지 않는다.

                        window.location.href =
                            '/order/payment/fail?errorType=error_stock&orderGroupPk='
                                .concat(
                                    data.params['orderGroupPk'],
                                    '&errorMsg='
                                )
                                .concat(data.params['errorMsg']);
                    }
                },
            });
        })
        .close(function (data) {
            // 결제창이 닫힐때 수행됩니다. (성공,실패,취소에 상관없이 모두 수행됨)
        })
        .done(function (data) {
            //결제가 정상적으로 완료되면 수행됩니다
            //비즈니스 로직을 수행하기 전에 결제 유효성 검증을 하시길 추천합니다.

            // payment_valid_gift view에 form submit의 형태로 검증 데이터 전송
            const paymentValidForm = document.createElement('form');
            paymentValidForm.setAttribute('method', 'POST');
            paymentValidForm.setAttribute('action', PAYMENT_VALID_URL);

            // payment_valid_gift view에는 order_group.pk, receipt_id를 전달한다
            const orderGroupPKHiddenInput = document
                .createElement('input')
                .setAttribute('name', 'orderGroupPk');
            orderGroupPKHiddenInput.setAttribute('type', 'hidden');
            orderGroupPKHiddenInput.setAttribute('value', ORDER_GROUP_PK);

            const receiptIDHiddenInput = document
                .createElement('input')
                .setAttribute('name', 'receiptID');
            receiptIDHiddenInput.setAttribute('type', 'hidden');
            receiptIDHiddenInput.setAttribute('value', data.receipt_id);

            // XSS 방지용 csrf token
            const csrfHiddenInput = document
                .createElement('input')
                .setAttribute('name', 'csrfmiddlewaretoken');
            csrfHiddenInput.setAttribute('type', 'hidden');
            csrfHiddenInput.setAttribute('value', CSRF_TOKEN);

            // 만약 동작 안하면 appendChild() 시도
            paymentValidForm.append(
                orderGroupPKHiddenInput,
                receiptIDHiddenInput,
                csrfHiddenInput
            );

            paymentValidForm.submit();
        });
}
