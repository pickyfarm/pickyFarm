const commentSubmit = () => {
    const text = document.querySelector('#id_text').value;

    $.ajax({
        type: 'POST',
        url: commentSubmitURL,
        dataType: 'json',
        data: {
            text: text,
            pk: storyPK,
            user: userPK,
            like_count: comment_like_count,
            csrfmiddlewaretoken: CSRFToken,
        },
        success: function (data) {
            let comment = `
            <div class="comment" name=${data.pk}>
                <div class="comment-info flex items-center">
                    <div class="comment-author flex items-center">
                        <img src="${data.user_image}" class="comment-author--profile-image">
                        <div class="comment-author--id">${data.author}</div>
                    </div>
                    <div class="bar"></div>
                    <div class="comment-create text-center">${data.create_at}</div>
                    <div class="bar"></div>
                    <div class="comment-report flex items-center ml-auto">
                        <img src="${reportButtonImageURL}" alt="">
                        <div class="comment-report--report button">신고하기</div>
                    </div>
                </div>
                <div class="comment-content relative">
                    <div class="comment-text">
                        <div class="comment-text--text">${text}</div>
                        <div class="comment-text-options text-right flex justify-between">
                            <div onclick="expandRecommentSection(this)" class="button comment-text-options--recomment">답글 0개</div>
                            <div class="flex">
                                <div class="comment-text-options--edit button" onclick=storyCommentEdit(this,${data.pk})>수정
                                </div>
                                <div class="comment-text-options--delete button" onclick=storyCommentDelete(${data.pk})>삭제</div>
                            </div>
                        </div>
                    </div>
                    <div class="absolute comment-like-button-wrap button">
                        <div class="comment-like-button relative"
                            style="background-image: url(${likeButtonImageURL});">
                            <p class="comment-like-count absolute text-center align-text-bottom">${data.like_count}</p>
                        </div>
                    </div>
                </div>
                <div class="recomment-wrap">
                <div class="recomment-input-wrapper flex flex-col">
                    <div class="flex items-center recomment-info">
                        <div class="recomment-arrow"></div>
                        <div class="recomment-author flex items-center">
                            <img src="${currentUserProfileImageURL}" class="comment-author--profile-image">
                            <div class="comment-author--id">${currentUserNickname}</div>
                        </div>
                    </div>
                    <textarea type="text" class="recomment-input-box" name='${data.pk}'></textarea>
                    <button class="recomment-submit-button mx-auto"
                        onclick="recommentSubmit(${data.pk})">등록하기</button>
                    </div>
                </div>
            </div>`;

            $('#comments').prepend(comment);
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
        url: `../../../../comment/farmer_story/${storyPK}/comment/${pk}/recomment/`,
        dataType: 'json',
        data: {
            text: targetComment.value,
            like_count: recomment_like_count,
            csrfmiddlewaretoken: CSRFToken,
        },

        success: function (data) {
            const comment = `
            <div class="recomment relative" name="${data.pk}">
                    <div class="flex items-center recomment-info">
                        <div class="recomment-arrow"></div>
                        <div class="recomment-author flex items-center">
                            <img src="${data.user_image}" class="comment-author--profile-image">
                            <div class="comment-author--id">${data.author}</div>
                        </div>
                        <div class="bar"></div>
                        <div class="comment-create text-center recomment-create">
                            ${data.create_at}
                        </div>
                        <div class="bar"></div>
                        <div class="recomment-report flex items-center ml-auto">
                            <img src="${reportButtonImageURL}"
                                alt="">
                            <div class="comment-report--report button">신고하기</div>
                        </div>
                    </div>
                    <div class="absolute recomment-like-button-wrap button">
                        <div class="recomment-like-button relative"
                            style="background-image: url(${recommentLikeButtonImageURL});">
                            <p class="recomment-like-count absolute text-center align-text-bottom">0</p>
                        </div>
                    </div>
                    <div class="recomment-content">
                        <div class="recomment-text">
                            <div class="recomment-text--text">${data.text}</div>
                            <div class="recomment-text-options-wrap flex justify-between">
                                <div></div>
                                <div class="recomment-text-options flex">
                                    <div class="recomment-text-options--edit button comment-text-options--edit"  onclick="storyRecommentEdit(this, ${data.pk})">수정</div>
                                    <div class="recomment-text-options--delete button comment-text-options--delete" onclick="storyRecommentDelete(${data.pk})">삭제</div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="horizon-bar mx-auto"></div>
            `;

            targetComment.parentNode.parentNode.insertAdjacentHTML(
                'beforeend',
                comment
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
