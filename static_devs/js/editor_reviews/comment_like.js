const commentLikeHandler = (e, type) => {
    const getCommentSelector = () => {
        switch (type) {
            case 'comment':
                return {
                    comment: '.comment',
                    count: '.comment-like-count',
                    url: commentLikeURL,
                };
            case 'recomment':
                return {
                    comment: '.recomment',
                    count: '.recomment-like-count',
                    url: recommentLikeURL,
                };
        }
    };

    const commentSelector = getCommentSelector();

    const comment = e.target.closest(commentSelector.comment);
    const pk = parseInt(comment.getAttribute('name'));

    $.ajax({
        type: 'POST',
        url: commentSelector.url,
        dataType: 'json',
        data: {
            pk: pk,
            csrfmiddlewaretoken: CSRFToken,
        },
        success: (data) => {
            comment.querySelector(commentSelector.count).innerHTML =
                data['likes'];

            data.status
                ? shootToastMessage('댓글에 좋아요를 눌렀습니다')
                : shootToastMessage('댓글에 좋아요를 취소하였습니다');
        },
        error: (request) => {
            shootToastMessage(request.responseText);
        },
    });
};

// const commentLike = (e) => {
//     const comment = e.target.closest('.comment');
//     const pk = parseInt(comment.getAttribute('name'));

//     $.ajax({
//         type: 'POST',
//         url: commentLikeURL,
//         dataType: 'json',
//         data: {
//             pk: pk,
//             csrfmiddlewaretoken: CSRFToken,
//         },
//         success: (data) => {
//             comment.querySelector('.comment-like-count').innerHTML =
//                 data['likes'];

//             data.status
//                 ? shootToastMessage('댓글에 좋아요를 눌렀습니다')
//                 : shootToastMessage('댓글에 좋아요를 취소하였습니다');
//         },
//         error: (request) => {
//             shootToastMessage(request.responseText);
//         },
//     });
// };

// const recommentLike = (e) => {
//     comment = e.target.closest('.recomment');
//     pk = parseInt(comment.getAttribute('name'));

//     $.ajax({
//         type: 'POST',
//         url: recommentLikeURL,
//         dataType: 'json',
//         data: {
//             pk: pk,
//             csrfmiddlewaretoken: CSRFToken,
//         },
//         success: (data) => {
//             comment.querySelector('.recomment-like-count').innerHTML =
//                 data['likes'];

//             data.status
//                 ? shootToastMessage('답글에 좋아요를 눌렀습니다')
//                 : shootToastMessage('답글에 좋아요를 취소하였습니다');
//         },
//         error: (error) => {
//             shootToastMessage(error);
//         },
//     });
// };

document.querySelectorAll('.comment-like-button-wrap').forEach((elem) => {
    elem.addEventListener('click', (e) => commentLikeHandler(e, 'comment'));
});

document.querySelectorAll('.recomment-like-button-wrap').forEach((elem) => {
    elem.addEventListener('click', (e) => commentLikeHandler(e, 'recomment'));
});
