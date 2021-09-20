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
    $.ajax({
        url: orderStateUpdateURL,
        type: 'POST',
        data: {
            csrfmiddlewaretoken: CSRFToken,
            pk: pk,
            state: 'preparing',
        },
        success: (res) => {
            document.querySelector(
                `.order-confirm-overlay[name='${pk}']`
            ).style.display = 'none';

            shootToastMessage(res);
        },
        complete: () => {
            location.reload();
        },
    });
};

const startDate = document.querySelector('#start-date');
const endDate = document.querySelector('#end-date');

document
    .querySelector('#recent-one-month')
    .addEventListener('click', () => setDateFilter(1));

document
    .querySelector('#recent-three-month')
    .addEventListener('click', () => setDateFilter(3));

document.querySelector('.date-filter-submit').addEventListener('click', () => {
    !(startDate.value && endDate.value) && alert('날짜를 모두 입력해주세요.');
});

startDate.addEventListener('change', (e) => {
    if (DateTime.fromISO(e.target.value) > DateTime.now()) {
        startDate.value = endDate.value = DateTime.now().toISODate();
    }
});

const setDateFilter = (month) => {
    const today = DateTime.now();
    const pastDate = today.minus({ months: month });

    startDate.value = pastDate.toISODate();
    endDate.value = today.toISODate();
};
