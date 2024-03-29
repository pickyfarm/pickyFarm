'use strict';

function _toArray(arr) {
    return (
        _arrayWithHoles(arr) ||
        _iterableToArray(arr) ||
        _unsupportedIterableToArray(arr) ||
        _nonIterableRest()
    );
}

function _nonIterableRest() {
    throw new TypeError(
        'Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.'
    );
}

function _unsupportedIterableToArray(o, minLen) {
    if (!o) return;
    if (typeof o === 'string') return _arrayLikeToArray(o, minLen);
    var n = Object.prototype.toString.call(o).slice(8, -1);
    if (n === 'Object' && o.constructor) n = o.constructor.name;
    if (n === 'Map' || n === 'Set') return Array.from(o);
    if (n === 'Arguments' || /^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n))
        return _arrayLikeToArray(o, minLen);
}

function _arrayLikeToArray(arr, len) {
    if (len == null || len > arr.length) len = arr.length;
    for (var i = 0, arr2 = new Array(len); i < len; i++) {
        arr2[i] = arr[i];
    }
    return arr2;
}

function _iterableToArray(iter) {
    if (
        (typeof Symbol !== 'undefined' && iter[Symbol.iterator] != null) ||
        iter['@@iterator'] != null
    )
        return Array.from(iter);
}

function _arrayWithHoles(arr) {
    if (Array.isArray(arr)) return arr;
}

var plusBtn = document.getElementById('quantity-plus-button');
var minusBtn = document.getElementById('quantity-minus-button');
var totalPrice = document.getElementById('total-price');
var quantityNum = document.getElementById('product-quantity');

function calculateTotalPrice() {
    return (parseInt(quantityNum.value) * pricePerOne).toLocaleString('en-US');
}

if (isSoldOut != 'False') {
    plusBtn.addEventListener('click', function () {
        var num = parseInt(quantityNum.value);
        num += 1;
        quantityNum.value = num;
        totalPrice.innerText = calculateTotalPrice();
    });
    minusBtn.addEventListener('click', function () {
        var num = parseInt(quantityNum.value);
        if (num <= 1) num = 1;
        else {
            num -= 1;
            quantityNum.value = num;
            totalPrice.innerText = calculateTotalPrice();
        }
    });
}

// 상품 사진 조정
var main_image = document.getElementById('product-main-image');
var sub_images = document.querySelectorAll('.product-subimage');
sub_images?.forEach(function (item) {
    item.addEventListener('click', function () {
        var tmp_url = main_image.getAttribute('src');
        main_image.setAttribute('src', item.getAttribute('src'));
        item.setAttribute('src', tmp_url);
    });
});
// product review image slider

var review_imgs = document.querySelectorAll('#review_imgs');
review_imgs.forEach(function (img) {
    return img.classList.add('review_img_slick');
});
$('.review_img_slick').slick({
    infinite: false,
    slidesToShow: 3,
    slidesToScroll: 3,
});
// 찜하기
// var wishBtn = document.getElementById('wish');
// var product_pk = document
//     .getElementById('product_content')
//     .getAttribute('name');
// wishBtn.addEventListener('click', function () {
//     wish(product_pk);
// });

// 구독하기

subBtn.addEventListener('click', function () {
    var data = {
        farmer_pk: FARMER_PK,
        csrfmiddlewaretoken: csrftoken,
    };
    $.ajax({
        type: 'POST',
        url: subURL,
        dataType: 'json',
        data: data,
        success: function success(response) {
            if (response.status == -1)
                shootToastMessage(
                    '구독하지 못했습니다. 다시 시도해주세요',
                    '2'
                );
            else if (response.status == 0)
                shootToastMessage('이미 구독한 농가입니다!', '2');
            else shootToastMessage('농가를 구독하였습니다!', '2');
        },
        error: function error(request, status, _error) {
            shootToastMessage('로그인이 필요합니다', '2');
        },
    });
}); //장바구니 담기

var cartInBtn = document.getElementById('cart');
if (cartInBtn != null) {
    cartInBtn.addEventListener('click', function () {
        cartIn(this.getAttribute('name'));
    });
}

// 선물하기
if (giftButton != null) {
    giftButton.addEventListener('click', function () {
        const productData = {
            quantity: quantityNum.value,
            product_pk: PRODUCT_PK,
            csrfmiddlewaretoken: csrftoken,
        };

        const form = document.createElement('form');
        form.setAttribute('method', 'post');
        form.setAttribute('action', giftURL);

        for (const key in productData) {
            const hiddenField = document.createElement('input');
            hiddenField.setAttribute('type', 'hidden');
            hiddenField.setAttribute('name', key);
            hiddenField.setAttribute('value', productData[key]);

            form.appendChild(hiddenField);
        }

        console.log(form);

        document.body.appendChild(form);
        form.submit();
    });
}

// 품절 상품 alert
if (soldoutButton != null) {
    soldoutButton.addEventListener('click', function () {
        alert('지금은 판매하지 않는 상품입니다.');
    });
}

// 바로 구매하기
if (purchaseBtn != null) {
    purchaseBtn.addEventListener('click', function () {
        var quantity = parseInt(quantityNum.value);

        var product = {
            pk: PRODUCT_PK,
            quantity: quantity,
        };
        var products = [];
        products.push(product);
        var data = {
            orders: JSON.stringify(products),
            csrfmiddlewaretoken: csrftoken,
        };
        var form = document.createElement('form');
        form.setAttribute('method', 'post');
        form.setAttribute('action', purchaseURL);

        for (var key in data) {
            var hiddenField = document.createElement('input');
            hiddenField.setAttribute('type', 'hidden');
            hiddenField.setAttribute('name', key);
            hiddenField.setAttribute('value', data[key]);
            form.appendChild(hiddenField);
        }

        document.body.appendChild(form);
        form.submit();
    });
}

// // 댓글 작성 버튼 toggle
// var recomments = document.querySelectorAll('.recomments');
// recomments.forEach(function (recomment) {
//     return recomment.classList.add('hide');
// });
// $(document).on('click', '#more_btn', function () {
//     $(this).parent().siblings('.recomments').toggle();
//     $(this).children('.fa-caret-down').toggle();
//     $(this).children('.fa-caret-up').toggle();

//     var _document$querySelect = document.querySelectorAll('.recomment_form'),
//         _document$querySelect2 = _toArray(_document$querySelect),
//         recomment_forms = _document$querySelect2.slice(0);

//     recomment_forms.forEach(function (form) {
//         form.scrollBy(0, 10000);
//     });
// });

// QnA Pagination

var qna_page = document.querySelectorAll('#qna_paginator');
var QnaURL = "{% url 'products:qna_paginator' %}";
console.log(qna_page);
qna_page.forEach(function (item) {
    item.addEventListener('click', function () {
        var page_num = item.getAttribute('name');
        $.ajax({
            type: 'POST',
            url: QnaURL,
            dataType: 'json',
            data: {
                product_pk: product_pk,
                page_num: page_num,
                csrfmiddlewaretoken: csrftoken,
            },
            success: function success(data) {
                var qnaSection = document.getElementById('qnas-section');
                console.log(data);
                qnaSection.innerHTML = '';
                data.questions.forEach(function (item) {
                    var status = item.status;
                    var title = item.title;
                    var consumer = item.consumer;
                    var create_at = item.create_at;
                    var q_pk = item.pk;
                    console.log(
                        status + ' ' + title + ' ' + consumer + ' ' + create_at
                    );
                    var qnaLine = "<a href='/product/question/".concat(
                        q_pk,
                        '\'> <div id="q_table_bottom" class="flex flex-rows py-1">'
                    );

                    if (status == true) {
                        qnaLine +=
                            '\n                                    <div id="q_letter_answered" class="w-2/12">\uB2F5\uBCC0\uC644\uB8CC</div>\n                            <div id="q_letter_black" class="w-6/12">'
                                .concat(
                                    title,
                                    '</div>\n                            <div id="q_letter_black" class="w-2/12">'
                                )
                                .concat(
                                    consumer,
                                    '</div>\n                            <div id="q_letter_gray" class="w-2/12">'
                                )
                                .concat(
                                    create_at.date,
                                    '</div>\n                        </div>\n                        </a>'
                                );
                    } else {
                        qnaLine +=
                            '\n                                    <div id="q_letter_answered" class="w-2/12">\uB2F5\uBCC0\uB300\uAE30</div>\n                            <div id="q_letter_black" class="w-6/12">'
                                .concat(
                                    title,
                                    '</div>\n                            <div id="q_letter_black" class="w-2/12">'
                                )
                                .concat(
                                    consumer,
                                    '</div>\n                            <div id="q_letter_gray" class="w-2/12">'
                                )
                                .concat(
                                    create_at.date,
                                    '</div>\n                        </div>\n                        </a>'
                                );
                    }

                    qnaSection.insertAdjacentHTML('beforeend', qnaLine);
                });
            },
            error: function error() {
                alert('error');
            },
        });
    });
}); // 농가 구독 플로팅 모달

floatingBtn.addEventListener('click', function () {
    subscribeModalMessage(modalAjaxURL, farmerPK, function () {
        location.href = detailURL;
    });
});
