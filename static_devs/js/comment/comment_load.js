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
                recommentLoad(element.pk);
            });
        },
        complete: () => {
            Array.from(document.querySelectorAll('.comment-like-button-wrap'))
                .slice(numberOfComments)
                .forEach((elem) => {
                    elem.addEventListener('click', (e) => {
                        commentLikeHandler(e, 'comment');
                    });
                });
            shootToastMessage('댓글을 불러왔습니다.');
        },
    });
};

const recommentLoad = (pk) => {
    const numberOfComments = document.querySelectorAll(
        `div[class="recomment-wrap flex flex-col"][name="${pk}"] .recomment`
    ).length;

    $.ajax({
        type: 'POST',
        url: recommentLoadURL,
        dataType: 'json',
        data: {
            numberOfComments: numberOfComments,
            pk: pk,
            csrfmiddlewaretoken: CSRFToken,
        },
        success: (data) => {
            data.comment_list.forEach((element) => {
                document
                    .querySelector(
                        `div[class="recomment-wrap"][name="${pk}"] .recomment-load-button`
                    )
                    .insertAdjacentHTML(
                        'beforebegin',
                        recommentComponent(
                            element,
                            currentUserNickname,
                            currentUserProfileImageURL
                        )
                    );
            });
        },
        complete: () => {
            Array.from(
                document.querySelectorAll(
                    `div[class="recomment-wrap"][name="${pk}"] .recomment-like-button-wrap`
                )
            )
                .slice(numberOfComments)
                .forEach((elem) => {
                    elem.addEventListener('click', (e) => {
                        commentLikeHandler(e, 'recomment');
                    });
                });
            shootToastMessage('답글을 불러왔습니다.');
        },
    });
};
