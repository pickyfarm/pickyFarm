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
                        commentComponent(
                            element,
                            currentUserNickname,
                            currentUserProfileImageURL
                        )
                    );
            });
        },
        complete: () => {
            Array.from(document.querySelectorAll('.comment'))
                .slice(numberOfComments)
                .forEach((elem) => {
                    elem.addEventListener('click', (e) => {
                        commentLike(e);
                    });
                });
            shootToastMessage('댓글을 불러왔습니다.');
        },
    });
};
