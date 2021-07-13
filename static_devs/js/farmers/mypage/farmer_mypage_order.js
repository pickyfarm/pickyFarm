document.querySelectorAll('.order-confirm').forEach((elem) => {
    elem.addEventListener('click', (e) => {
        // AJAX Handler when farmer accepts new order
        orderConfirm(
            e.target.closest('.order-confirm-overlay').getAttribute('name')
        );
    });
});

document.querySelectorAll('.order-cancel').forEach((elem) => {
    elem.addEventListener('click', (e) => {
        // AJAX Handler when farmer declines new order
        orderCancel(
            e.target.closest('.order-confirm-overlay').getAttribute('name')
        );
    });
});

const orderConfirm = (pk) => {
    document.querySelector(
        `.order-confirm-overlay[name='${pk}']`
    ).style.display = 'none';

    shootToastMessage('주문을 수락하였습니다.');
};

const orderCancel = (pk) => {
    document.querySelector(`.order-confirm-overlay[name='${pk}']`).innerHTML =
        '<div class="order-cancelled">취소한 주문건 입니다.</div>';

    shootToastMessage('주문을 취소하였습니다.');
};
