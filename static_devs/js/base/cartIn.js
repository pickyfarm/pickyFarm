const cartIn = (pk) => {
    $.ajax({
        type: 'POST',
        url: '/user/cartIn/',
        data: {
            pk: pk,
            csrfmiddlewaretoken: csrftoken,
        },
        dataType: 'json',
        success: function (response) {
            shootToastMessage(response.message, 2);
        },
        error: function (request, status, error) {
            shootToastMessage('로그인이 필요합니다.', 2, 'error');
        },
    });
};
