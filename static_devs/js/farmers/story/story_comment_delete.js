const storyCommentDelete = (pk) => {
    showModalMessage('댓글을 삭제하시겠습니까?', () => {
        $.ajax({
            url: `../../../../comment/farmer_story/${storyPK}/comment/delete/${pk}/`,
            dataType: 'json',
            data: {},
            success: (data) => {
                const status = data['status'];

                if (status) {
                    alert('댓글이 삭제되었습니다.');
                    location.reload();
                }
            },
        });
    });
};

const storyRecommentDelete = (pk) => {
    showModalMessage('답글을 삭제하시겠습니까?', () => {
        $.ajax({
            type: 'POST',
            url: recommentDeleteURL,
            dataType: 'json',
            data: {
                pk: pk,
                csrfmiddlewaretoken: CSRFToken,
            },
            success: (data) => {
                if (data.status) {
                    alert('답글이 삭제되었습니다.');
                    location.reload();
                }
            },
        });
    });
};
