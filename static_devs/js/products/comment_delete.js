const recommentDelete = (pk) => {
    showModalMessage('답글을 삭제하시겠습니까?', () => {
        $.ajax({
            type: 'POST',
            url: recommentDeleteURL,
            dataType: 'json',
            data: {
                pk: pk,
                csrfmiddlewaretoken: csrftoken,
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
