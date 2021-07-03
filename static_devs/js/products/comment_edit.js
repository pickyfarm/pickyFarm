const recommentEditForm = `
    <div class="comment-edit-form-container recomment-edit-form-container mx-auto">
        <form class="flex flex-col comment-edit-form recomment-edit-form w-full">
            <input type="text" class="comment-edit-form-input recomment-edit-form-input">
            <div class="flex items-center justify-between">
                <div></div>
                <button type="submit" class="comment-edit-submit-button">수정하기</button>
                <p class="comment-edit-cancel recomment-edit-cancel button">취소</p>
            </div>
        </form>
    </div>
    `;

const recommentEdit = (targetComment, pk) => {
    console.log(targetComment.closest('.recomment-text-options-wrap').previousElementSibling)
    const comment = targetComment.closest('.recomment-text-options-wrap')
        .previousElementSibling.innerHTML;

    targetForm = targetComment.closest('.recomment-text');
    targetForm.innerHTML = recommentEditForm;

    targetInput = targetForm.querySelector('.recomment-edit-form-input');
    targetInput.value = comment;
    targetInput.focus();

    document
        .querySelector('.recomment-edit-cancel')
        .addEventListener('click', () => {
            showModalMessage('수정을 취소하시겠습니까?', () => {
                location.reload();
            });
        });

    document
        .querySelector('.recomment-edit-form')
        .addEventListener('submit', (e) => {
            e.preventDefault();
            recommentEditSubmit(pk);
        });
};

const recommentEditSubmit = (pk) => {
    const text = document.querySelector('.recomment-edit-form-input').value;

    $.ajax({
        type: 'POST',
        url: recommentEditURL,
        dataType: 'json',
        data: {
            pk: pk,
            text: text,
            csrfmiddlewaretoken: csrftoken,
        },
        success: (data) => {
            if (data.status) {
                alert('답글을 수정하였습니다.');
                location.reload();
            }
        },
    });
};
