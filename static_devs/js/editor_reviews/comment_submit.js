const commentSubmit = () => {
    const text = document.querySelector('#id_text').value;

    $.ajax({
        type: 'POST',
        url: commentSubmitURL,
        dataType: 'json',
        data: {
            text: text,
            pk: reviewPK,
            user: userPK,
            csrfmiddlewaretoken: CSRFToken,
        },
        success: function (data) {
            $('#comments').prepend(commentComponent(data));
            document
                .querySelectorAll('.comment')[0]
                .querySelector('.comment-like-button-wrap')
                .addEventListener('click', (e) => {
                    commentLike(e);
                });
            $('#id_text').val('');

            shootToastMessage('댓글이 등록되었습니다.');
        },
        error: function () {
            if ($('id_text').val() == '') {
                alert('댓글을 입력하세요');
            }
        },
    });
};

const recommentSubmit = (pk) => {
    const textBox = document.querySelectorAll('.recomment-input-box');
    const targetComment = [...textBox].find(
        (elem) => parseInt(elem.getAttribute('name')) === pk
    );

    $.ajax({
        type: 'POST',
        url: `/editors_pick/${reviewPK}/comment/${pk}/recomment`,
        dataType: 'json',
        data: {
            text: targetComment.value,
            csrfmiddlewaretoken: CSRFToken,
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
