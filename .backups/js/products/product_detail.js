let plusBtn = document.getElementById('plus_btn')
let minusBtn = document.getElementById('minus_btn')
let totalPrice = document.getElementById('total_price')
let quantityNum = document.getElementById('quantity_number')
let pricePerOne = parseInt(totalPrice.innerHTML)

function addCalTotalPrice(price, quantity) {
    let nowTotalPrice = totalPrice.innerHTML
    nowTotalPrice = parseInt(nowTotalPrice)

    let newTotalOrderPrice = nowTotalPrice + price * quantity
    totalPrice.innerHTML = String(newTotalOrderPrice)
}

function subCalTotalPrice(price, quantity) {
    let nowTotalPrice = totalPrice.innerHTML
    nowTotalPrice = parseInt(nowTotalPrice)

    let newTotalOrderPrice = nowTotalPrice - price * quantity
    if (newTotalOrderPrice < 0)
        newTotalOrderPrice = 0
    totalPrice.innerHTML = String(newTotalOrderPrice)
}

plusBtn.addEventListener('click', function () {
    let num = parseInt(quantityNum.innerHTML)
    num += 1
    quantityNum.innerHTML = num
    addCalTotalPrice(pricePerOne, 1)
})

minusBtn.addEventListener('click', function () {
    let num = parseInt(quantityNum.innerHTML)
    if (num <= 1)
        num = 1
    else {
        num -= 1
        quantityNum.innerHTML = num
        subCalTotalPrice(pricePerOne, 1)
    }

})

// 상품 사진 조정 
let main_image = document.getElementById('main_image')
let sub_images = document.querySelectorAll('#images')

sub_images.forEach(item => {
    item.addEventListener('click', function () {
        let tmp_url = main_image.getAttribute('src')
        main_image.setAttribute('src', item.getAttribute('src'))
        item.setAttribute('src', tmp_url)
    })
})

// product review image slider
let review_imgs = document.querySelectorAll('#review_imgs');
review_imgs.forEach(img => img.classList.add('review_img_slick'))

$('.review_img_slick').slick({
    infinite: false,
    slidesToShow: 3,
    slidesToScroll: 3
});

// 찜하기
let wishBtn = document.getElementById('wish')
let product_pk = document.getElementById('product_content').getAttribute('name')

wishBtn.addEventListener('click', function () {
    wish(product_pk)
})

// 구독하기
subBtn.addEventListener('click', function () {
    let farmerPk = subBtn.getAttribute('name')
    data = {
        'farmer_pk': farmerPk,
        "csrfmiddlewaretoken": csrftoken,
    }
    $.ajax({
        type: 'POST',
        url: subURL,
        dataType: 'json',
        data: data,
        success: function (response) {
            if (response.status == -1)
                shootToastMessage("구독하지 못했습니다. 다시 시도해주세요", '2')
            else if (response.status == 0)
                shootToastMessage("이미 구독한 농가입니다!", '2')
            else
                shootToastMessage("농가를 구독하였습니다!", '2')
        },
        error: function (request, status, error) {
            shootToastMessage("로그인이 필요합니다", '2')
        }
    })
})


//장바구니 담기
let cartInBtn = document.getElementById("cart")
cartInBtn.addEventListener('click', function () {
    cartIn(this.getAttribute('name'))
})

// 바로 구매하기
purchaseBtn.addEventListener('click', function () {
    let pk = this.getAttribute("name")
    let quantity = parseInt(document.getElementById("quantity_number").innerHTML)
    console.log(pk)
    console.log(quantity)
    product = {
        'pk': pk,
        'quantity': quantity
    }
    let products = [];
    products.push(product)

    data = {
        "orders": JSON.stringify(products),
        "csrfmiddlewaretoken": csrftoken,
    }

    let form = document.createElement("form")
    form.setAttribute("method", "post")
    form.setAttribute("action", purchaseURL)

    for (let key in data) {
        let hiddenField = document.createElement('input')
        hiddenField.setAttribute('type', 'hidden')
        hiddenField.setAttribute('name', key)
        hiddenField.setAttribute('value', data[key])

        form.appendChild(hiddenField)
    }
    document.body.appendChild(form)
    form.submit()
})





// 댓글 작성 버튼 toggle
let recomments = document.querySelectorAll('.recomments')
recomments.forEach(recomment => recomment.classList.add("hide"))
$(document).on('click', '#more_btn', function () {
    $(this).parent().siblings('.recomments').toggle();
    $(this).children('.fa-caret-down').toggle();
    $(this).children('.fa-caret-up').toggle();
    const [...recomment_forms] = document.querySelectorAll('.recomment_form')
    recomment_forms.forEach((form) => {
        form.scrollBy(0, 10000)
    });
});

// QnA Pagination
let qna_page = document.querySelectorAll('#qna_paginator')
const QnaURL = "{% url 'products:qna_paginator' %}"
console.log(qna_page)
qna_page.forEach(item => {
    item.addEventListener('click', function () {
        let page_num = item.getAttribute('name')
        $.ajax({
            type: 'POST',
            url: QnaURL,
            dataType: 'json',
            data: {
                'product_pk': product_pk,
                'page_num': page_num,
                "csrfmiddlewaretoken": csrftoken,
            },
            success: function (data) {
                let qnaSection = document.getElementById('qnas-section')
                console.log(data)
                qnaSection.innerHTML = ''
                data.questions.forEach(item => {
                    let status = item.status
                    let title = item.title
                    let consumer = item.consumer
                    let create_at = item.create_at
                    let q_pk = item.pk
                    console.log(status + ' ' + title + ' ' + consumer + ' ' + create_at)
                    let qnaLine = `<a href='/product/question/${q_pk}'> <div id="q_table_bottom" class="flex flex-rows py-1">`;

                    if (status == true) {
                        qnaLine += `
                                    <div id="q_letter_answered" class="w-2/12">답변완료</div>
                            <div id="q_letter_black" class="w-6/12">${title}</div>
                            <div id="q_letter_black" class="w-2/12">${consumer}</div>
                            <div id="q_letter_gray" class="w-2/12">${create_at.date}</div>
                        </div>
                        </a>`
                    }
                    else {
                        qnaLine += `
                                    <div id="q_letter_answered" class="w-2/12">답변대기</div>
                            <div id="q_letter_black" class="w-6/12">${title}</div>
                            <div id="q_letter_black" class="w-2/12">${consumer}</div>
                            <div id="q_letter_gray" class="w-2/12">${create_at.date}</div>
                        </div>
                        </a>`
                    }
                    qnaSection.insertAdjacentHTML('beforeend', qnaLine)
                })
            },
            error: function () {
                alert("error")
            }
        })
    })
})

// 농가 구독 플로팅 모달
floatingBtn.addEventListener('click', function () {
    subscribeModalMessage(modalAjaxURL, farmerPK, () => { location.href = detailURL })
})