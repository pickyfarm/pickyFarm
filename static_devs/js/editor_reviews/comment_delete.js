const commentDelete = (pk) => {
    $.ajax({
        url: '/editors_pick/' + reviewPK + `/comment/delete/${pk}`,
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
};

const recommentDelete = (pk) => {
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
};
