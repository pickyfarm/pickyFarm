const recommentSubmit = (pk) => {
    const textBox = document.querySelectorAll('.recomment-input-box');
    const targetComment = [...textBox].find(
        (elem) => parseInt(elem.getAttribute('name')) === pk
    );

    $.ajax({
        type: 'POST',
        url: `/comment/product/${productPK}/comment/${pk}/recomment/`,
        dataType: 'json',
        data: {
            text: targetComment.value,
            csrfmiddlewaretoken: csrftoken,
        },

        success: function (data) {
            targetComment.parentElement.nextElementSibling.insertAdjacentHTML(
                'afterend',
                recommentComponent(data)
            );
            targetComment.value = '';

            const t = document
                .querySelector(
                    `div[class="recomment relative"][name="${data.pk}"] .recomment-like-button-wrap`
                )
                .addEventListener('click', (e) => recommentLike(e));

            shootToastMessage('답글이 등록되었습니다.');
        },
    });
};
