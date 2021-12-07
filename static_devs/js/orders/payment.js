"use strict";

function _toConsumableArray(arr) { return _arrayWithoutHoles(arr) || _iterableToArray(arr) || _unsupportedIterableToArray(arr) || _nonIterableSpread(); }

function _nonIterableSpread() { throw new TypeError("Invalid attempt to spread non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method."); }

function _unsupportedIterableToArray(o, minLen) { if (!o) return; if (typeof o === "string") return _arrayLikeToArray(o, minLen); var n = Object.prototype.toString.call(o).slice(8, -1); if (n === "Object" && o.constructor) n = o.constructor.name; if (n === "Map" || n === "Set") return Array.from(o); if (n === "Arguments" || /^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n)) return _arrayLikeToArray(o, minLen); }

function _iterableToArray(iter) { if (typeof Symbol !== "undefined" && iter[Symbol.iterator] != null || iter["@@iterator"] != null) return Array.from(iter); }

function _arrayWithoutHoles(arr) { if (Array.isArray(arr)) return _arrayLikeToArray(arr); }

function _arrayLikeToArray(arr, len) { if (len == null || len > arr.length) len = arr.length; for (var i = 0, arr2 = new Array(len); i < len; i++) { arr2[i] = arr[i]; } return arr2; }

window.onload = function () {
  if (navigator.userAgent.match(/inapp|NAVER|KAKAOTALK|Snapchat|Line|WirtschaftsWoche|Thunderbird|Instagram|everytimeApp|WhatsApp|Electron|wadiz|AliApp|zumapp|iPhone(.*)Whale|Android(.*)Whale|kakaostory|band|twitter|DaumApps|DaumDevice\/mobile|FB_IAB|FB4A|FBAN|FBIOS|FBSS/i)) {
    alert('[안내]\n기본 브라우저 외에서의 결제 진행은 오류가 있을 수 있으니 피키팜 결제 완료 페이지를 반드시 확인하고 결제 종료해주세요! 결제 오류 문의 : 카카오톡 피키팜 Picky Farm');
  }
};

var productPrice = document.querySelector('.delivery-fee');
var totalPrice = document.getElementById('price_text_b').innerHTML;
var deliveryCatDefault = document.getElementById('delivery-cat-default');
var deliveryCatChoice = document.getElementById('delivery-cat-choice');
var deliveryCatDirect = document.getElementById('delivery-cat-direct');
var deliveryAddress = document.getElementById("delivery-address");
var deliveryAddressInput = document.getElementById('delivery-address-input-section');
var mainAddressInput = document.getElementById('id_full_address');
var subAddressInput = document.getElementById('id_detail_address');
var zipcode = document.getElementById('id_zipcode');
var deliveryCatDetailSection = document.getElementById('delivery-cat-detail-section');
deliveryCatDefault.addEventListener('click', function () {
  deliveryCatDetailSection.innerHTML = "";
  deliveryAddress.value = '{{default_address}}';
  deliveryAddressInput.style.display = 'none';
});

var updateDeliveryFee = function updateDeliveryFee(zipcode) {
  $.ajax({
    type: 'POST',
    url: '{% url "orders:payment_change-address" %}',
    data: {
      csrfmiddlewaretoken: "{{csrf_token}}",
      order_group_pk: "{{order_group_pk}}",
      zip_code: zipcode.value
    },
    success: function success(data) {
      var totalPrice = document.getElementById('price_text_b');
      var oldPrice = parseInt(productPrice.innerText);
      var oldTotalPrice = parseInt(totalPrice.innerText);
      var fee_to_add = parseInt(data['fee_to_add']);
      productPrice.innerText = fee_to_add + oldPrice;
      totalPrice.innerText = fee_to_add + oldTotalPrice;
    }
  });
};

deliveryCatChoice.addEventListener('click', function () {
  add_html = "<div id=\"delivery-cat-detail-index-section\" class=\"flex flex-row\">\n                    <div id=\"delivery-cat-detail-index-title-section\" class=\"flex flex-row\">\n                        <div class=\"\">\uBC30\uC1A1 \uBC1B\uC73C\uC2E4 \uC8FC\uC18C\uB97C \uC120\uD0DD\uD574\uC8FC\uC138\uC694</div>\n                    </div>\n                </div>\n                {% for addr in  addresses%}\n                        <div id=\"delivery-address-choice\" class=\"transition_element text-center\" data-zipcode=\"{{addr.zipcode}}\">{{addr.full_address}} {{addr.detail_address}}</div>\n                {% endfor %}";
  deliveryCatDetailSection.innerHTML = add_html;
  var choice = document.querySelectorAll('#delivery-address-choice');
  choice.forEach(function (item) {
    return item.addEventListener('click', function () {
      deliveryAddress.value = item.innerHTML;
      updateDeliveryFee(item.dataset.zipcode);
    });
  });
  deliveryAddressInput.style.display = 'none';
});
deliveryCatDirect.addEventListener('click', function () {
  deliveryAddress.value = '';
  deliveryAddressInput.style.display = 'block';
  deliveryCatDetailSection.innerHTML = "";
});
subAddressInput.addEventListener('focus', function () {
  return updateDeliveryFee(zipcode);
});
subAddressInput.addEventListener('input', function (e) {
  deliveryAddress.value = "".concat(mainAddressInput.value, " ").concat(e.target.value);
});
var goBtn = document.getElementById('go-btn');
console.log(goBtn);
console.log(window.location.origin);
goBtn.addEventListener('click', function () {
  var revName = document.getElementById('id_rev_name').value;
  var revPhoneNumber = document.getElementById('id_rev_phone_number').value;
  var revLocAt = document.querySelector("input[name='rev_loc_at']:checked").value;
  var paymentType = document.querySelector("input[name='payment_type']:checked").value;
  var revMessage = document.getElementById('id_rev_message').value;
  var toFarmMessage = document.getElementById('id_to_farm_message').value;
  var items = document.querySelectorAll('#product');
  console.log(items);
  console.log(toFarmMessage);
  console.log(revName);
  console.log(revLocAt);

  if (revName == "") {
    alert("주문자 이름을 입력해주세요");
    return;
  }

  if (revPhoneNumber == "") {
    alert("휴대폰 번호를 입력해주세요");
    return;
  }

  var personalInfoAgree = document.getElementById("personal-info-agree");

  if (personalInfoAgree.checked == false) {
    alert("개인 정보 수집 이용에 동의해주세요");
    return;
  }

  var finalAgree = document.getElementById("final-agree");

  if (finalAgree.checked == false) {
    alert("결제 정보 확인 및 구매 진행에 동의해주세요");
    return;
  } //배송지 관련 로직//
  //배송지 카테고리 selectors
  //배송지 폼


  var deliveryAddress = document.getElementById("delivery-address");
  revAddress = deliveryAddress.value;

  if (revAddress == "") {
    alert("배송지를 입력 혹은 선택해주세요");
    return;
  }

  data = {
    'rev_name': revName,
    'rev_phone_number': revPhoneNumber,
    'rev_address': revAddress,
    'rev_loc_at': revLocAt,
    'rev_message': revMessage,
    'to_farm_message': toFarmMessage,
    'payment_type': paymentType
  };
  var itemsList = [];
  items.forEach(function (item) {
    var unique = item.getAttribute('name');
    var itemName = item.querySelector('#title').innerHTML;
    var qty = item.querySelector('#orders-num').innerHTML;
    var price = item.querySelector('#sell-price').innerHTML;
    var cat1 = "과일 임시";
    itemsList = [].concat(_toConsumableArray(itemsList), [{
      item_name: itemName,
      //상품명
      qty: qty,
      //수량
      unique: unique,
      //해당 상품을 구분짓는 primary key
      price: price,
      //상품 단가
      cat1: cat1 // 대표 상품의 카테고리 상, 50글자 이내

    }]);
  });
  console.log(itemsList);
  BootPay.request({
    price: parseInt(totalPrice),
    //실제 결제되는 가격
    application_id: "60dad0c05b29480021dc523d",
    name: '{{order_group_name}}',
    //결제창에서 보여질 이름
    pg: 'inicis',
    method: paymentType,
    //결제수단, 입력하지 않으면 결제수단 선택부터 화면이 시작합니다.
    show_agree_window: 0,
    // 부트페이 정보 동의 창 보이기 여부
    items: itemsList,
    user_info: {
      username: revName,
      addr: revAddress,
      phone: revPhoneNumber
    },
    order_id: '{{order_group_management_number}}',
    //고유 주문번호로, 생성하신 값을 보내주셔야 합니다.
    params: {
      orderName: '{{order_group_name}}',
      errorMsg: '',
      orderGroupPk: '{{order_group_pk}}'
    },
    extra: {
      escrow: paymentType == 'vbank' ? true : false
    } // account_expire_at: '2020-10-25', // 가상계좌 입금기간 제한 ( yyyy-mm-dd 포멧으로 입력해주세요. 가상계좌만 적용됩니다. )
    // extra: {
    //     start_at: '2019-05-10', // 정기 결제 시작일 - 시작일을 지정하지 않으면 그 날 당일로부터 결제가 가능한 Billing key 지급
    //     end_at: '2022-05-10', // 정기결제 만료일 -  기간 없음 - 무제한
    //     vbank_result: 1, // 가상계좌 사용시 사용, 가상계좌 결과창을 볼지(1), 말지(0), 미설정시 봄(1)
    //     quota: '0,2,3', // 결제금액이 5만원 이상시 할부개월 허용범위를 설정할 수 있음, [0(일시불), 2개월, 3개월] 허용, 미설정시 12개월까지 허용,
    //     theme: 'purple', // [ red, purple(기본), custom ]
    //     custom_background: '#00a086', // [ theme가 custom 일 때 background 색상 지정 가능 ]
    //     custom_font_color: '#ffffff' // [ theme가 custom 일 때 font color 색상 지정 가능 ]
    // }

  }).error(function (data) {
    //결제 진행시 에러가 발생하면 수행됩니다.
    window.location.href = "/order/payment/fail?errorType=error_server";
    console.log(data);
  }).cancel(function (data) {
    //결제가 취소되면 수행됩니다.
    console.log(data);
  }).ready(function (data) {
    // 가상계좌 입금 계좌번호가 발급되면 호출되는 함수입니다.
    sendData = {
      'rev_name': revName,
      'rev_phone_number': revPhoneNumber,
      'rev_address': revAddress,
      'rev_loc_at': revLocAt,
      'rev_message': revMessage,
      'to_farm_message': toFarmMessage,
      'payment_type': paymentType,
      'total_price': totalPrice,
      'order_group_pk': data['params']['orderGroupPk'],
      'order_group_name': data['params']['orderName'],
      'v_bank': data['bankname'],
      'v_bank_account': data['account'],
      'v_bank_account_holder': data['accounthodler'],
      'v_bank_expire_date': data['expiredate'],
      'receipt_id': data['receipt_id']
    };
    console.log(data['bankname']);
    console.log(data['account']);
    console.log(data['accounthodler']);
    console.log(data['expiredate']);
    var form = document.createElement("form");
    form.setAttribute("method", "post");
    form.setAttribute("action", "{% url 'orders:vbank_progess' %}");

    for (var key in sendData) {
      var hiddenField = document.createElement('input');
      hiddenField.setAttribute('type', 'hidden');
      hiddenField.setAttribute('name', key);
      hiddenField.setAttribute('value', sendData[key]);
      form.appendChild(hiddenField);
    }

    var csrfHiddenField = document.createElement('input');
    csrfHiddenField.setAttribute('type', 'hidden');
    csrfHiddenField.setAttribute('name', 'csrfmiddlewaretoken');
    csrfHiddenField.setAttribute('value', csrftoken);
    form.appendChild(csrfHiddenField);
    document.body.appendChild(form);
    form.submit();
  }).confirm(function (data) {
    //결제가 실행되기 전에 수행되며, 주로 재고를 확인하는 로직이 들어갑니다.
    //주의 - 카드 수기결제일 경우 이 부분이 실행되지 않습니다.
    sendData = {
      'rev_name': revName,
      'rev_phone_number': revPhoneNumber,
      'rev_address': revAddress,
      'rev_loc_at': revLocAt,
      'rev_message': revMessage,
      'to_farm_message': toFarmMessage,
      'payment_type': paymentType,
      'total_price': totalPrice
    };
    console.log(data);
    console.log(sendData);
    $.ajax({
      type: "POST",
      url: "{% url 'orders:payment_update' order_group_pk %}",
      data: sendData,
      dataType: "json",
      success: function success(response) {
        var enable = response.valid;

        if (enable) {
          BootPay.transactionConfirm(data); // 조건이 맞으면 승인 처리를 한다.
        } else {
          if (response.error_type == "error_stock") {
            response.invalid_products.forEach(function (item) {
              data.params['errorMsg'] += item;
            });
            data.params['errorMsg'] += " 재고가 부족합니다";
          } else {
            data.params['errorMsg'] += "클라이언트에서의 총 결제액이 서버와 일치하지 않습니다";
          }

          BootPay.removePaymentWindow(); // 조건이 맞지 않으면 결제 창을 닫고 결제를 승인하지 않는다.

          window.location.href = "/order/payment/fail?errorType=error_stock&orderGroupPk=".concat(data.params['orderGroupPk'], "&errorMsg=").concat(data.params['errorMsg']);
        }
      }
    });
  }).close(function (data) {
    // 결제창이 닫힐때 수행됩니다. (성공,실패,취소에 상관없이 모두 수행됨)
    console.log(data);
  }).done(function (data) {
    //결제가 정상적으로 완료되면 수행됩니다
    //비즈니스 로직을 수행하기 전에 결제 유효성 검증을 하시길 추천합니다.
    //data.prams['orderGroupPk']
    var form = document.createElement("form");
    form.setAttribute("method", "post");
    form.setAttribute("action", "{% url 'orders:payment_valid' %}");

    for (var key in data) {
      var hiddenField = document.createElement('input');
      hiddenField.setAttribute('type', 'hidden');
      hiddenField.setAttribute('name', key);
      hiddenField.setAttribute('value', data[key]);
      form.appendChild(hiddenField);
    }

    var hiddenFieldAdd = document.createElement('input');
    hiddenFieldAdd.setAttribute('type', 'hidden');
    hiddenFieldAdd.setAttribute('name', 'orderGroupPk');
    hiddenFieldAdd.setAttribute('value', data.params['orderGroupPk']);
    form.appendChild(hiddenFieldAdd);
    console.log(csrftoken);
    var csrfHiddenField = document.createElement('input');
    csrfHiddenField.setAttribute('type', 'hidden');
    csrfHiddenField.setAttribute('name', 'csrfmiddlewaretoken');
    csrfHiddenField.setAttribute('value', csrftoken);
    form.appendChild(csrfHiddenField);
    document.body.appendChild(form);
    form.submit();
  }); // tossPayments.requestPayment('카드', {
  // amount: totalPrice,
  // orderId: 'eN4Pv_y8K6RC3WeBdFP-s',
  // orderName: response.orderName,
  // customerName: response.customerName,
  // successUrl: window.location.origin + `/order/payment/success?amount_ready=${totalPrice}`,
  // failUrl: window.location.origin + '/order/payment/fail',
  // })
});