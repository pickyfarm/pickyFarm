
const wish = (pk) => {
    $.ajax({
        type: 'POST',
        url: '/user/wish/',
        dataType: 'json',
        data: {
            pk: pk,
            csrfmiddlewaretoken: csrftoken,
        },
        success: function (response) {
            if (response.status == 0) {
                shootToastMessage('이미 찜한 무난이 입니다!')
            }
            else if (response.status == 1) {
                shootToastMessage('무난이를 찜했습니다')
            }
        },
        error: function (request, status, error) {
            shootToastMessage('로그인이 필요합니다.')
        }
    })
};