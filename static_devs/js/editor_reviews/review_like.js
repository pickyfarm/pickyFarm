const editorReviewLike = (pk) => {
    $.ajax({
        type: 'POST',
        url: reviewLikeURL,
        dataType: 'json',
        data: {
            pk: pk,
            csrfmiddlewaretoken: csrftoken,
        },
        success: (data) => {
            data.status
                ? shootToastMessage('댓글에 좋아요를 눌렀습니다')
                : shootToastMessage('댓글에 좋아요를 취소하였습니다');
        },
        error: (data) => {
            shootToastMessage(data.responseText, 2, 'error');
        },
    });
};
