const commentComponent = (props) => {
    return `
    <div class="comment" name=${props.pk}>
        <div class="comment-info flex items-center">
            <div class="comment-author flex items-center">
                <img src="${
                    props.profile_image
                }" class="comment-author--profile-image">
                <div class="comment-author--id">${props.author}</div>
            </div>
            <div class="bar"></div>
            <div class="comment-create text-center">${props.create_at}</div>
            <div class="bar"></div>
            <div class="comment-report flex items-center ml-auto">
                <img src="${reportButtonImageURL}" alt="">
                <div class="comment-report--report button">신고하기</div>
            </div>
        </div>
        <div class="comment-content relative">
            <div class="comment-text">
                <div class="comment-text--text">${props.text}</div>
                <div class="comment-text-options text-right flex justify-between">
                    <div onclick="expandRecommentSection(this)" class="button comment-text-options--recomment">답글 ${
                        props.recomment_count ? props.recomment_count : 0
                    }개</div>
                    <div class="flex">
                        <div class="comment-text-options--edit button" onclick=commentEdit(this,${
                            props.pk
                        })>수정
                        </div>
                        <div class="comment-text-options--delete button" onclick=commentDelete(${
                            props.pk
                        })>삭제</div>
                    </div>
                </div>
            </div>
            <div class="absolute comment-like-button-wrap button">
                <div class="comment-like-button relative"
                    style="background-image: url(${likeButtonImageURL});">
                    <p class="comment-like-count absolute text-center align-text-bottom">${
                        props.like_count
                    }</p>
                </div>
            </div>
        </div>
        <div class="recomment-wrap" name="${props.pk}">
            <div class="recomment-input-wrapper flex flex-col">
                <div class="flex items-center recomment-info">
                    <div class="recomment-arrow"></div>
                    <div class="recomment-author flex items-center">
                        <img src="${currentUserProfileImageURL}" class="comment-author--profile-image">
                        <div class="comment-author--id">${currentUserNickname}</div>
                    </div>
                </div>
                <textarea type="text" class="recomment-input-box" name='${
                    props.pk
                }'></textarea>
                <button class="recomment-submit-button mx-auto"
                    onclick="recommentSubmit(${props.pk})">등록하기</button>
            </div>
            <div class="horizon-bar mx-auto"></div>
            <button onclick="recommentLoad(${
                props.pk
            })" class="recomment-load-button">불러오기</button>
        </div>
    </div>`;
};

const recommentComponent = (props) => {
    return `
    <div class="recomment relative" name="${props.pk}">
        <div class="flex items-center recomment-info">
            <div class="recomment-arrow"></div>
            <div class="recomment-author flex items-center">
                <img src="${props.profile_image}" class="comment-author--profile-image">
                <div class="comment-author--id">${props.author}</div>
            </div>
            <div class="bar"></div>
            <div class="comment-create text-center recomment-create">
                ${props.create_at}
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
                <p class="recomment-like-count absolute text-center align-text-bottom">${props.like_count}</p>
            </div>
        </div>
        <div class="recomment-content">
            <div class="recomment-text">
                <div class="recomment-text--text">${props.text}</div>
                <div class="recomment-text-options-wrap flex justify-between">
                    <div></div>
                    <div class="recomment-text-options flex">
                        <div class="recomment-text-options--edit button comment-text-options--edit"  onclick="recommentEdit(this, ${props.pk})">수정</div>
                        <div class="recomment-text-options--delete button comment-text-options--delete" onclick="recommentDelete(${props.pk})">삭제</div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <div class="horizon-bar mx-auto"></div>`;
};
