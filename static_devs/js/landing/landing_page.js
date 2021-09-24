// top menu
const signupButton = document.querySelector('a#header-signup');
const serviceCenterButton = document.querySelector('a#header-service-center');
const myPageButton = document.querySelector('a#header-mypage');
const cartButton = document.querySelector('a#header-cart');
// main menu
const storeButton = document.querySelector('a#header-list--store');
const editorPickButton = document.querySelector('a#header-list--editors-pick');
const farmerPageButton = document.querySelector('a#header-list--farmers-page');

function alertBasicAnnounce(e) {
    e.preventDefault();
    alert('10월 중순 오픈 예정입니다! 카톡 친추를 통해 알림을 받아보세요!');
}
// 회원가입
if (signupButton !== null) {
    signupButton.addEventListener('click', function (e) {
        alertBasicAnnounce(e);
    });
}
// 고객센터
serviceCenterButton.addEventListener('click', function (e) {
    alertBasicAnnounce(e);
});
// mypage
myPageButton.addEventListener('click', function (e) {
    alertBasicAnnounce(e);
});

// 장바구니
cartButton.addEventListener('click', function (e) {
    alertBasicAnnounce(e);
});

// Editor's Pick
editorPickButton.addEventListener('click', function (e) {
    alertBasicAnnounce(e);
});

// Farmer's Page
farmerPageButton.addEventListener('click', function (e) {
    alertBasicAnnounce(e);
});

// Store
storeButton.addEventListener('click', function (e) {
    const user_pk = storeButton.getAttribute('name');
    if (user_pk !== 'None') {
        e.preventDefault();
        data = {
            user_pk: user_pk,
            csrfmiddlewaretoken: CSRF_TOKEN,
        };
        $.ajax({
            type: 'POST',
            url: landingTestURL,
            dataType: 'json',
            data: data,
            success: function (response) {
                if (response.status == 1) {
                    window.location.href = storePageURL;
                } else if (response.status == 0) {
                    alert(
                        '계정을 확인해주세요! (카드사 심사는 테스트 아이디로 로그인해주세요)'
                    );
                }
            },
            error: function (request, status, error) {
                alert(
                    '10월 중순 오픈 예정입니다! (카드사 심사는 테스트 아이디로 로그인해주세요)'
                );
            },
        });
    } else if (user_pk == 'None') {
        e.preventDefault();
        alert(
            '10월 중순 오픈 예정입니다! (카드사 심사는 테스트 아이디로 로그인해주세요)'
        );
    }
});
