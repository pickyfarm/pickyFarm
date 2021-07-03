const commentLoad = (pk) => {
    const numberOfComments = document.querySelectorAll('.comment').length;

    $.ajax({
        type: 'POST',
        url: commentLoadURL,
        dataType: 'json',
        data: {
            numberOfComments: numberOfComments,
            pk: reviewPK,
            csrfmiddlewaretoken: CSRFToken,
        },
        success: (data) => {
            data.comment_list.forEach((element) => {
                document
                    .querySelector('#comments')
                    .insertAdjacentHTML(
                        'beforeend',
                        comment(
                            element,
                            currentUserNickname,
                            currentUserProfileImageURL
                        )
                    );

                shootToastMessage('댓글을 불러왔습니다.');
            });
        },
    });
};
